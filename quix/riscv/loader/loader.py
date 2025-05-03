from io import BytesIO

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import Section

from quix.riscv.opcodes.base import RISCVOpcode

from .decoder import decode
from .state import State


def _get_name_data_mapping(elf: ELFFile) -> dict[str, Section]:
    sections = {}
    for sec in elf.iter_sections():  # type: ignore
        sections[sec.name] = sec
    return sections


def _decode_riscv_code(text: Section) -> dict[int, RISCVOpcode]:
    idx = text.header["sh_addr"]
    data = BytesIO(text.data())  # type: ignore
    code = {}

    while instr := data.read(4):
        int_instr = int.from_bytes(instr, byteorder="little", signed=False)
        code[idx] = decode(int_instr)
        # print(f"{int_instr:#034b}", code[idx])
        idx += 4

    return code


class ELFLoader:
    __slots__ = ()

    def load(self, data: BytesIO) -> State:
        elf = ELFFile(data)  # type: ignore

        entry = elf.header["e_entry"]
        sections = _get_name_data_mapping(elf)
        code = _decode_riscv_code(sections.pop(".text"))

        return State(code, entry, sections)
