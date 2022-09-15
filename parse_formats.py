#!/usr/bin/python3
"""Parse FORMATS from manual/ into text files."""
import dataclasses
import pathlib
import re
import textwrap
import typing as t

cwd = pathlib.Path(__file__).parent
manual_dir = cwd / "manual"

# Since tmux 1.6 manual pages used this before formats
needle = "The following variables are available, where appropriate:"


@dataclasses.dataclass
class Format:
    variable_name: str
    alias: str | None
    replaced_with: str


@dataclasses.dataclass
class Manual:
    version: str
    machine_version: float
    path: pathlib.Path
    formats: list[Format] = dataclasses.field(default_factory=list)


format_re = re.compile(
    r"""
^\s{5}
(?P<variable_name>[a-z_]+){1}
(?:[ \t]){5,15}                        # skip spaces
(?P<alias>\#[a-zA-Z]{1})?
(?:[ \t]){5,15}                        # skip spaces
(?P<replaced_with>[a-zA-Z ]+){1}$
""",
    re.VERBOSE | re.MULTILINE,
)


def run() -> int:
    if not manual_dir.is_dir():
        raise Exception("manual/ dir mustexist in CWD in relation to this script")

    # Fetch files
    version_map: dict[str, Manual] = {}
    for file in sorted(manual_dir.glob("*.txt")):
        version_raw = str(file.stem).rsplit(".txt")[0]

        machine_version = version_raw
        if not machine_version[-1].isdigit():
            machine_version = machine_version[:-1] + str(ord(machine_version[-1]) - 96)
        version = float(machine_version)
        version_map[version_raw] = Manual(
            version=version_raw, machine_version=version, path=file
        )

    # Parse formats from files
    for manual in version_map.values():
        if manual.machine_version < 1.6:
            continue

        contents = open(manual.path).read()

        for line in format_re.finditer(contents):
            if line is not None:
                match = line.groupdict()
                assert match is not None
                manual.formats.append(Format(**match))

    for manual in version_map.values():
        print(f"tmux {manual.version}")

        # Array
        formats = ", ".join([f'"{format.variable_name}"' for format in manual.formats])
        print(f"     Formats: [{formats}]")

        # Dataclass
        print(
            textwrap.dedent(
                f"""
@dataclasses.dataclass
class TmuxObject:
    """
                + "\n    ".join(
                    [f"{format.variable_name}: str" for format in manual.formats]
                )
            )
        )

    return 0


if __name__ == "__main__":
    run()
