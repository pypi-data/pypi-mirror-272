from typing import List
from pathlib import Path
from typing import Optional as Opt
import re
import os

WD = Path(os.getcwd())


def _read(p: Path) -> List[str]:
    with p.open() as f:
        return f.readlines()


def bundle(
    src: Path,
    include_paths: List[Path] = None,
    add_line=False,
    # relpath = True,
) -> str:
    if include_paths is None:
        include_paths = []

    is_once = set()
    edges = set()

    def expand(file: Path) -> str:
        dir = file.parent

        # angle: #include <header>
        def find_file(
            header: str,
            angle: bool = False,
        ) -> Opt[Path]:
            if not angle:
                file = dir / header
                if file.exists():
                    return file
            for d in include_paths:
                file = d / header
                if file.exists():
                    return file
            return None

        def included_file(
            line: str,
        ) -> Opt[str]:
            ptn = r"^\s*#\s*include\s*<(.+)>\s*\n$"
            m = re.match(ptn, line)
            if m is not None:
                header = m.groups()[0]
                return find_file(header, True)
            ptn = r"^\s*#\s*include\s*\"(.+)\"\s*\n$"
            m = re.match(ptn, line)
            if m is not None:
                header = m.groups()[0]
                return find_file(header)

        def is_pragma_once(
            line: str,
        ) -> bool:
            ptn = r"^\s*#\s*pragma\s+once\s*\n$"
            return re.match(ptn, line) is not None

        lines = _read(file)
        result_lines = []
        al = True
        for i, l in enumerate(lines):
            if is_pragma_once(l):
                is_once.add(file)
                al = True
                continue
            dep = included_file(l)
            if dep is None:
                if al and add_line:
                    f = file
                    # if relpath:
                    #     f.relative_to(WD, walk_up=True)
                    result_lines.append(
                        f'#line {i + 1} "{f}"\n'
                    )
                    al = False
                result_lines.append(l)
                continue
            if dep in is_once:
                al = True
                continue
            e = (file, dep)
            if e in edges:
                raise "circular includes"
            edges.add(e)
            result_lines.append(expand(dep))
            al = True
            edges.remove(e)

        # result_lines.reverse()
        # while result_lines:
        #     if result_lines[-1] != "\n":
        #         break
        #     result_lines.pop()
        # result_lines.reverse()
        return "".join(result_lines)

    return expand(src)
