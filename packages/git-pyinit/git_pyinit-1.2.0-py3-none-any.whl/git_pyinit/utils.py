from .toml_reader import TomlResults


def format_template(results: TomlResults) -> str:
    template = """
    name: Linting Stage

    on: [push]

    jobs:
        build:
          runs-on: ubuntu-latest
          strategy:
            matrix:
              python-version: {py_vers}
          steps:
          - uses: actions/checkout@v3
          - name: Set Up Python ${{{{ matrix.python-version }}}}
            uses: actions/setup-python@v3
            with:
              python-version: ${{{{ matrix.python-version }}}}
          - name: Install Dependencies
            run: |
              python -m pip install --upgrade pip
              pip install {yaml_commands}
    """.format(
        py_vers=str(results.py_vers),
        yaml_commands=" ".join([tool.yaml_command for tool in results.tools if tool.active]),
    )
    for tool in results.tools:
        if not tool.active:
            continue
        template += f"""
              - name: Analyzing code with {tool.name}
                run: |
                  {tool}
        """
    return template
