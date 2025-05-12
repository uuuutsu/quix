from quix.bootstrap.dtypes.const import UDynamic


def is_signed(value: UDynamic) -> bool:
    return (int(value) & (1 << 31)) > 0
