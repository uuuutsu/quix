> Fixing `NameError: name 'cbclib' is not defined`

This error is linked to various mismatches between [`python-mip`](https://github.com/coin-or/python-mip), [`cbclib`](https://cbclib.readthedocs.io/en/latest/install.html#) and their respective binaries on various systems. Upgrading `gcc`, `gfortran` may help. See [full thread](https://github.com/coin-or/python-mip/issues/335).
