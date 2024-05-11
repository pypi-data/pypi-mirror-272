from dataclasses import InitVar, dataclass, field

import toml


@dataclass
class TomlResults:
    runs_on: list
    py_vers: list
    tools: list


@dataclass
class Tool:
    name: str
    command: InitVar[str] = field(default=None)
    yaml_command: str = field(init=False)
    active: bool = True
    flags: list = field(default_factory=list)
    file_command: str = field(default="$(git ls-files '*.py')")

    def __post_init__(self, command):
        self.command = command or self.name
        # Just have this for debug representation
        self.yaml_command = self.command

    def __str__(self):
        return f"{self.command} {self.file_command} {' '.join(self.flags)}"


def read_toml(filepath):
    with open(filepath) as f:
        return toml.load(f)


def get_tool_list(filepath):
    _toml = read_toml(filepath)
    _py_vers = _toml.get("build", {}).get("python_version", ["3.8"])
    _runs_on = _toml.get("build", {}).get("runs_on", ["ubuntu-latest"])
    tools = _toml.get("tool", {})
    active = tools.get("active", [])
    default = tools.get("default", {})
    _end = []
    for tool in active:
        tool_section = tools.get(tool, {})
        _end.append(
            Tool(
                name=tool_section.get("name", tool),
                command=tool_section.get("command", None),
                flags=tool_section.get("flags", default.get("flags", [])),
                file_command=tool_section.get("file_command", default.get("file_command", "$(git ls-files '*.py')")),
                active=tool_section.get("active", True),
            )
        )
    return TomlResults(runs_on=_runs_on, py_vers=_py_vers, tools=_end)
