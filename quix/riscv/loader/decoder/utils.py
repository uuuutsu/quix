def get_bit_section(number: int, start: int, end: int) -> int:
    aligned = number >> end
    mask = (1 << (start - end + 1)) - 1
    return aligned & mask
