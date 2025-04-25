def intervals_intersects(int1: tuple[int, int], int2: tuple[int, int]) -> bool:
    return max(int1[1], int2[1]) - min(int1[0], int2[0]) < (int1[1] - int1[0]) + (int2[1] - int2[0]) or (
        (int1[0] <= int2[0]) and (int1[1] >= int2[1])
    )
