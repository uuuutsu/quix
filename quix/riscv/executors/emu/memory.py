class EmuMemory:
    __slots__ = "memory"

    def __init__(self) -> None:
        self.memory: dict[int, int] = {}

    def __setitem__(self, address: int, data: int | bytes) -> None:
        if isinstance(data, bytes):
            for i, b in enumerate(data):
                self.memory[address + i] = b
            return

        if data < 0:
            data += 1 << 32

        for i, b in enumerate(data.to_bytes(4, byteorder="little", signed=False)):
            self.memory[address + i] = b

    def __getitem__(self, address: int) -> int:
        return self.memory.get(address, 0)

    def get_word(self, base_addr: int) -> int:
        word = 0
        for offset in range(4):
            word += self[offset + base_addr] << (offset * 8)

        if word & (1 << 31):
            return word - (1 << 32)

        return word
