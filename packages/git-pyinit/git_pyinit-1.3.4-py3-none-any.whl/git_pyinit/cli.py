import argparse
import os
import subprocess
import sys
from pathlib import Path

from .exceptions.common import GitNotInstalled, HatchNotInstalled
from .toml_reader import get_yaml_list
from .utils import format_template


class PrintConfig(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(Path(__file__).parent / "config.toml")
        sys.exit(0)


class OpenConfig(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        subprocess.run([os.environ.get("EDITOR", "vim"), str(Path(__file__).parent / "config.toml")], check=False)
        sys.exit(0)


def get_args(input=None):
    parser = argparse.ArgumentParser(
        description="git-pyinit: create a new git "
        + "repository using hatch structure, "
        + "and set up workflows automatically using a config.toml"
    )
    parser.add_argument(
        "project_name",
        help="name of the project, please keep "
        + "in mind hatch will replace spaces with -'s or _'s depending "
        + "on what is in your local repository",
        type=str,
        nargs="?",
    )
    parser.add_argument(
        "--edit-config", help="edit the config.toml file using default editor", action=OpenConfig, nargs=0
    )
    parser.add_argument("--config", help="Print out the config path and exit", action=PrintConfig, nargs=0)
    parser.add_argument(
        "-p", "--mkdir", help="Create all the parent directories if they don't exist", action="store_true"
    )
    # Assume that any other arg will be passed directly to git init
    return parser.parse_known_args(input)


def test_dependencies():
    # Make sure that git is installed on the system
    if subprocess.run(["git", "--version"], stdout=subprocess.DEVNULL, check=False).returncode:
        raise GitNotInstalled("git is not installed on this system or is not along your path, cannot continue.")
        sys.exit(1)
    # we should never hit this, but just in case
    elif subprocess.run(["hatch", "--version"], stdout=subprocess.DEVNULL, check=False).returncode:
        raise HatchNotInstalled("hatch is not installed on this system or is not along your path, cannot continue.")
        sys.exit(1)


def create_project_and_cd(args) -> int:
    if args.project_name:
        proj = Path(args.project_name).absolute()
        if args.mkdir:
            # Use the parent, and rely on hatch to create the project name directory
            proj.parent.mkdir(parents=True, exist_ok=True)
        os.chdir(proj.parent)
        x = subprocess.run(["hatch", "new", proj.name], stdout=subprocess.PIPE, check=False)
        if x.returncode:
            # if it failed, it most likely wasn't empty
            if proj.exists():
                os.chdir(proj)
            else:
                print(x.stdout.decode("utf-8"))
                return 1
        else:
            _str = x.stdout.decode("utf-8")
            print(_str)
            # Use this in case hatch changes what directory is output
            _created_dir = _str.split("\n")[0]
            os.chdir(_created_dir)
    # assume that they mean this directory
    else:
        current_dir = Path(os.getcwd()).absolute()
        os.chdir(current_dir.parent)
        subprocess.run(["hatch", "new", current_dir.name], check=False)
        os.chdir(current_dir.name)
    return 0


def write_workflow_yaml(path, tools):
    path.write_text(format_template(tools))


def get_workflow_file(name):
    if not name.endswith(".yml"):
        name += ".yml"
    return Path(".github", "workflows", name)


def main(_input=None, standalone=False):
    here = os.getcwd()

    args, assumed_git_args = get_args(_input)
    if (result := create_project_and_cd(args)) != 0 and not standalone:
        sys.exit(result)
    subprocess.run(["git", "init", *assumed_git_args], check=False)

    script_dir = Path(__file__).parent
    config = script_dir / "config.toml"
    if not config.exists():
        print("Could not find config, no yamls will be generated")
        if standalone:
            return 1
        else:
            sys.exit(1)
    else:
        yamls = get_yaml_list(config)
    for yaml in yamls:
        workflows_file = get_workflow_file(name=yaml.name)
        if not (parent := workflows_file.parent).exists():
            parent.mkdir(parents=True, exist_ok=True)
        write_workflow_yaml(workflows_file, yaml)
    print("Done.")

    # in case it's not being ran as a subshell
    os.chdir(here)


if __name__ == "__main__":
    main()
