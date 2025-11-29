.PHONY: lint build compile

TOOL_NAME = riscv

build:
	docker build -t $(TOOL_NAME) -f docker/Dockerfile.riscv .

compile:
	docker run --rm -v "${PWD}":/work -w /work $(TOOL_NAME) \
		riscv32-unknown-elf-gcc \
			$(SRC) \
			-march=rv32ia \
			-mabi=ilp32 \
			-mno-relax \
			--static \
			--no-pie \
			-o output.o

lint:
	docker run --rm -v "${PWD}":/work -w /work $(TOOL_NAME) \
		riscv32-unknown-elf-ld \
			-static \
			-nostdlib \
			-no-pie \
			-o output.elf \
			$(SRC)
