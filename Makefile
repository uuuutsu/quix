.PHONY: lint build

TOOL_NAME = riscv

build:
	docker build -t $(TOOL_NAME) -f docker/Dockerfile.riscv .

assemble:
	docker run --rm -v "${PWD}":/work -w /work $(TOOL_NAME) \
		riscv32-unknown-linux-gnu-gcc \
			-c $(SRC) \
			-march=rv32i \
			-mabi=ilp32 \
			-mno-relax \
			-o output.o

lint:
	docker run --rm -v "${PWD}":/work -w /work $(TOOL_NAME) \
		riscv32-unknown-linux-gnu-ld \
			-static \
			-nostdlib \
			-no-pie \
			-o output.elf \
			$(SRC)
