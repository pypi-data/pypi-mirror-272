"""
Used to scan the given directories for loadable files
"""

import os
from typing import Iterable

PY_END = (".py", ".pyc", ".pyo")


def scan(dirs: Iterable[str]) -> dict:
    ret = {}
    ret["python"] = {}
    ret["cython"] = {}
    ret["imp"] = {}
    for dir_ in dirs:
        try:
            for fn_ in os.listdir(dir_):
                _apply_scan(ret, str(dir_), str(fn_))
        except FileNotFoundError:
            ...
    return ret


cdef _apply_scan(dict ret, str dir_, str fn_):
    if fn_.startswith("_"):
        return
    full = os.path.join(dir_, fn_)
    if "." not in full:
        return
    bname = full[: full.rindex(".")]
    if fn_.endswith(PY_END):
        if bname not in ret["python"]:
            ret["python"][bname] = {"path": full}
