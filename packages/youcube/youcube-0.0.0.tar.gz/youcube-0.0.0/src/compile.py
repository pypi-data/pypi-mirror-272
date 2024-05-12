#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Compiles YC to pyc files
"""

from os import rename
from os.path import isdir, join
from pathlib import Path
from py_compile import compile as py_compile


def main() -> None:
    """Starts the compilation"""
    blacklist = ["__main__.py"]

    for path in Path("youcube").rglob("*.py"):
        if not isdir(path) and path.name not in blacklist:
            compile_path = py_compile(path, optimize=2)
            new_name = Path(
                join(Path(compile_path).parent, path.name.replace(".py", ".pyc"))
            )
            rename(compile_path, new_name)
            print(path, "->", new_name)


if __name__ == "__main__":
    main()

