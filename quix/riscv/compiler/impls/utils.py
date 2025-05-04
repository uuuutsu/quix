from quix.bootstrap.dtypes.const import DynamicUInt


def is_signed(value: DynamicUInt) -> bool:
    return (int(value) & (1 << 31)) > 0
