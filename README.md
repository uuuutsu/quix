# Quix

A multi-stage compiler that transforms RISC-V ELF binaries into Brainfuck.

```
┌─────────────┐    ┌───────────────┐    ┌────────────┐    ┌─────────────┐    ┌─────────────┐
│  ELF Binary │ -> │ RISC-V Instrs │ -> │ Macrocodes │ -> │ Core Opcodes│ -> │ Brainfuck   │
└─────────────┘    └───────────────┘    └────────────┘    └─────────────┘    └─────────────┘
```

## Why?

Brainfuck has only 8 commands and operates on a tape of memory cells. Running a real instruction set on it is an exercise in compiler design, abstraction layers, and memory optimization. Quix demonstrates how to bridge a conventional ISA with an esoteric target through well-designed intermediate representations.

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/quix.git
cd quix

# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

### Requirements

- Python 3.12
- Dependencies: `pyelftools`, `mip`, `numpy`, `typer`, `rich`

### Usage

```bash
# Build a RISC-V ELF binary to Brainfuck
quix build <path-to-elf>

# Execute compiled Brainfuck
quix execute <path-to-bf>
```

## The Compilation Pipeline

Quix transforms code through five distinct stages, each with its own level of abstraction.

### Stage 1: ELF Loading

First, we parse the ELF binary and extract RISC-V instructions.

```
                    ┌──────────────┐
  Binary File  -->  │  ELF Loader  │  -->  Instruction Map
                    └──────────────┘
                           │
                           v
                    dict[address, opcode]
                    {
                      0x1000: add(x1, x2, x3),
                      0x1004: lw(x4, 0(x5)),
                      0x1008: beq(x1, x2, 16),
                      ...
                    }
```

The loader extracts the `.text` section and decodes each 32-bit instruction into a structured opcode. All RISC-V formats are supported: R, I, S, B, U, and J-type instructions.

**Key files:** `quix/riscv/loader/loader.py`, `quix/riscv/loader/decoder/`

### Stage 2: RISC-V Compilation

Each RISC-V instruction is translated into macrocodes through custom handlers.

```
    RISC-V Instruction              Macrocode Expansion
    ──────────────────              ───────────────────
    add x1, x2, x3         -->      add_wide(x2, x3, x1)

    lw x1, 100(x2)         -->      add_wide(100, x2, tmp)
                                    load_array(memory, x1, tmp)

    beq x1, x2, label      -->      call_eq_wide(x1, x2,
                                        add_wide(pc, offset, pc),
                                        nop)
```

The compiler maintains the execution context:
- **32 registers** (`x0`-`x31`): Each is a `Wide` of 4 bytes
- **Program counter**: A 4-byte `Wide`
- **Memory**: An `Array` of 84,000 cells
- **Exit flag**: A single `Unit`

**Key files:** `quix/riscv/compiler/compiler.py`, `quix/riscv/compiler/instrs/`

### Stage 3: Macrocode Reduction

Macrocodes are high-level operations that recursively expand into primitive core opcodes.

```
    Macrocode                          Core Opcodes
    ─────────                          ────────────
    add_unit(a, b, result)    -->      clear(result)
                                       copy(a, {result: 1})
                                       copy(b, {result: 1})

    mul_unit(a, b, product)   -->      [dozens of core opcodes
                                        implementing multiplication
                                        through repeated addition]
```

This is where Quix builds complex behavior from simple primitives. A single `div_wide` operation might expand into hundreds of core opcodes handling multi-byte division with remainder.

**Key files:** `quix/bootstrap/macrocodes/`, `quix/bootstrap/reduce_program.py`

### Stage 4: Memory Scheduling

Before generating Brainfuck, we need to assign each variable to a physical memory cell.

```
    Variable Lifetimes:              Memory Layout:

    x: ████████░░░░░░░░              Cell 0: x
    y: ░░░░████████░░░░              Cell 1: y -> z (reused)
    z: ░░░░░░░░░░░░████              Cell 2: tmp
    tmp: ░░██░░██░░██░░

    Time: 0  2  4  6  8  10  12  14
```

The scheduler analyzes variable lifetimes and allocates cells, reusing memory when lifetimes don't overlap. This minimizes the total tape size—critical for Brainfuck performance.

**Key files:** `quix/memoptix/schedule.py`, `quix/memoptix/scheduler/`

### Stage 5: Brainfuck Generation

Finally, core opcodes become Brainfuck commands through the visitor pattern.

```
    Core Opcode                  Brainfuck
    ───────────                  ─────────
    add(cell_3, 5)      -->      >>>+++++

    start_loop(cell_2)  -->      >>[
    add(cell_2, -1)              -
    end_loop()                   ]

    output(cell_0)      -->      <<.
```

The visitor tracks the current tape position and generates `<`/`>` sequences to navigate between cells, then emits the appropriate operation.

**Key files:** `quix/core/compiler/visitor.py`, `quix/core/compiler/pointer.py`

## Architecture Overview

```
quix/
├── riscv/                    # RISC-V handling
│   ├── loader/               # ELF parsing and instruction decoding
│   │   ├── loader.py         # Main ELF loader
│   │   ├── decoder/          # Instruction decoders (R, I, S, B, U, J formats)
│   │   └── opcodes/          # RISC-V opcode definitions
│   └── compiler/             # RISC-V to macrocode translation
│       ├── compiler.py       # Main compiler loop
│       └── instrs/           # Per-instruction handlers (40+ files)
│
├── bootstrap/                # High-level abstractions
│   ├── dtypes/               # Data types (Unit, Wide, Array, Const)
│   ├── macrocodes/           # Macrocode definitions (50+ operations)
│   ├── program.py            # SmartProgram builder
│   └── reduce_program.py     # Macrocode expansion
│
├── core/                     # Low-level primitives
│   ├── opcodes/              # The 6 core opcodes
│   └── compiler/             # Brainfuck generation
│       ├── visitor.py        # Core-to-BF visitor
│       ├── pointer.py        # Tape pointer management
│       └── layout.py         # Memory cell layout
│
├── memoptix/                 # Memory optimization
│   ├── schedule.py           # Main scheduler
│   ├── compile.py            # Lifetime analysis
│   └── scheduler/            # Constraint solving
│
├── compiler/                 # Pipeline orchestration
│   ├── compile.py            # Main compile function
│   └── artifact/             # Output artifact format
│
└── cli/                      # Command-line interface
    └── main.py               # Entry point
```

## Core Concepts

### Data Types

Quix operates on three fundamental data types that map to Brainfuck's memory model.

**Unit** — A single 8-bit memory cell

Think of it as one slot on the Brainfuck tape. It holds a value from 0 to 255.

```python
counter = Unit("counter")  # One cell named "counter"
```

**Wide** — A tuple of independent Units

Used for multi-byte values like RISC-V's 32-bit registers. Each byte is stored in a separate cell.

```python
register = Wide.from_length("x1", 4)  # Four cells: x1[0], x1[1], x1[2], x1[3]
```

**Array** — An indexed memory structure

Allows random access by index, essential for implementing RISC-V memory operations.

```python
memory = Array("mem", length=256)  # 256-element array
# Access: memory[index] -> Unit
```

### The 6 Core Opcodes

Every program ultimately reduces to just six primitive operations:

| Opcode | BF Equivalent | Description |
|--------|---------------|-------------|
| `add(ref, value)` | `+` or `-` | Add/subtract from a cell |
| `input(ref)` | `,` | Read byte from stdin |
| `output(ref)` | `.` | Write byte to stdout |
| `start_loop(ref)` | `[` | Begin loop (skip if cell is 0) |
| `end_loop()` | `]` | End loop (repeat if cell is non-0) |
| `inject(ref, code)` | raw BF | Insert raw Brainfuck |

### Macrocodes

Macrocodes are the workhorses of Quix. They're declarative operations that expand into core opcodes.

**Unit Operations:**
- `clear_unit`, `move_unit`, `copy_unit`, `assign_unit`
- `add_unit`, `sub_unit`, `mul_unit`, `div_unit`
- `and_unit`, `or_unit`, `xor_unit`, `not_unit`
- `call_z_unit`, `call_eq_unit`, `call_ge_unit`, etc.

**Wide Operations:**
- `add_wide`, `sub_wide`, `mul_wide`, `div_wide`
- `and_wide`, `or_wide`, `xor_wide`, `not_wide`
- `call_eq_wide`, `call_ge_wide`, `call_lt_wide`, etc.
- `switch_wide` — Computed goto for control flow

**Array Operations:**
- `init_array`, `load_array`, `store_array`

**Example expansion:**

```python
# High-level: add two 4-byte values
add_wide(x1, x2, result)

# Expands to: byte-by-byte addition with carry propagation
add_unit_carry(x1[0], x2[0], result[0], carry)
add_unit_carry(x1[1], x2[1], result[1], carry)
add_unit_carry(x1[2], x2[2], result[2], carry)
add_unit_carry(x1[3], x2[3], result[3], carry)
```

## Example: Tracing an ADD Instruction

Let's follow `add x1, x2, x3` through the entire pipeline.

**Stage 1: ELF Loading**
```
Binary: 0x003100B3
        └─ Decoded: R-type, funct7=0, rs2=x3, rs1=x2, funct3=0, rd=x1, opcode=0x33
        └─ Result: add(rd=x1, rs1=x2, rs2=x3)
```

**Stage 2: RISC-V Compilation**
```python
# Handler lookup: get_instr("add") -> riscv_add
# Handler execution:
@macrocode
def riscv_add(rs1: Wide, rs2: Wide, rd: Wide) -> ToConvert:
    yield add_wide(rs1, rs2, rd)
```

**Stage 3: Macrocode Reduction**
```
add_wide(x2, x3, x1)
    │
    ├── clear_wide(x1)
    │       └── clear_unit(x1[0]), clear_unit(x1[1]), ...
    │
    └── add_unit_carry(x2[i], x3[i], x1[i], carry) for i in 0..3
            └── [loops for byte addition with carry]
```

**Stage 4: Memory Scheduling**
```
Variables: x1[0..3], x2[0..3], x3[0..3], carry, temps...
Allocated: Cell 0-3: x1, Cell 4-7: x2, Cell 8-11: x3, Cell 12: carry, ...
```

**Stage 5: Brainfuck Generation**
```brainfuck
>>>>>>>>>>>>[-]         # clear x1[0]
<<<<<<<[->>>>>>>>>+<<<<<<<]  # copy x2[0] to x1[0]
>>>>[->>>>>+<<<<<]      # copy x3[0] to x1[0]
...                     # (continues for all bytes)
```

## Caveats & Limitations

**Current limitations:**
- No floating-point support (RISC-V F/D extensions)
- No system calls or interrupts
- Memory size is fixed at compile time
- No dynamic linking

**Performance:**
- Generated Brainfuck is verbose by nature
- Complex programs produce very large BF files
- Execution is slow (it's Brainfuck, after all)

**Known TODOs:**
- CSR instructions not implemented
- Atomic operations not supported
- Compressed instructions (RVC) not decoded

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/bootstrap/macrocodes/add_wide.py

# Run with verbose output
pytest -v
```

### Project Structure for Tests

```
tests/
├── bootstrap/macrocodes/    # 60+ macrocode tests
├── core/compiler/           # BF generation tests
└── memoptix/                # Memory scheduler tests
```

### Code Quality

```bash
# Format and lint
ruff check --fix .
ruff format .

# Type checking
mypy quix/
```

### Adding a New RISC-V Instruction

1. Create a handler in `quix/riscv/compiler/instrs/`:

```python
@macrocode
def riscv_newop(rs1: Wide, imm: UDynamic, rd: Wide) -> ToConvert:
    # Implementation using macrocodes
    yield some_macrocode(rs1, rd)
```

2. The compiler will auto-discover it via the `riscv_{name}` naming convention.

## Troubleshooting

### `NameError: name 'cbclib' is not defined`

This error is linked to mismatches between `python-mip`, `cbclib` and their binaries. Try:
- Upgrading `gcc` and `gfortran`
- See the [full thread](https://github.com/coin-or/python-mip/issues/335)

## License

MIT
