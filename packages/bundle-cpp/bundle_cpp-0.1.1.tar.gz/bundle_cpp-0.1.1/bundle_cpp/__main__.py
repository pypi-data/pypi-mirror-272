import os
from typing import List
import argparse
from pathlib import Path
from dataclasses import dataclass
import dataclasses
from typing import Optional as Opt
from . import bundle


WD = Path(os.getcwd())


@dataclass
class CLIParam:
    src: Path
    include_paths: List[Path] = dataclasses.field(
        default_factory=list
    )
    dst: Opt[Path] = None


def cli():
    # https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-I",
        type=str,
        action="append",
        metavar="include_path",
        default=[WD],
        dest="include_paths",
        help="can be set multiple times.",
    )
    parser.add_argument(
        "-o",
        type=str,
        metavar="out_file",
        # default="generated.cpp",
        dest="dst",
        help="e.g. main_generated.cpp. not set, print stdout.",
    )
    g = parser.add_argument_group("required positional")
    g.add_argument(
        "src_file",
        type=str,
        help="e.g. main.cpp",
    )
    args = parser.parse_args()
    include_paths = [
        Path(p).resolve() for p in args.include_paths
    ]
    dst = None if args.dst is None else Path(args.dst).resolve()
    args = CLIParam(
        Path(args.src_file).resolve(),
        include_paths,
        dst,
    )
    res = bundle(args.src, args.include_paths)[:-1]
    if args.dst is None:
        print(res)
        return
    with args.dst.open("w") as f:
        f.write(res)


if __name__ == "__main__":
    cli()
    # f = f"{CFD}/main2.cpp"
    # paths = [CFD]
    # print(os.path.abspath("/root/"))
    # f = f"{CFD}/cycle_include/main.cpp"
    # f = f"{CFD}/pragma_once/main.cpp"
    # f = f"{CFD}/twice/main.cpp"
    # f = f"{CFD}/../../lib/cpp/template_v1.hpp"
    # print(bundle(f, paths))
    # print(bundle(f, paths).split('\n'))
