# git pyinit

[![PyPI - Version](https://img.shields.io/pypi/v/git-pyinit.svg)](https://pypi.org/project/git-pyinit)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/git-pyinit.svg)](https://pypi.org/project/git-pyinit)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)
- [How to use](#how-to-use)
    - [Example](#example)

## Installation

```console
pip install git-pyinit
```

## License

`git-pyinit` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## How to use

Due to how `git` works in looking for commands, after you `pip install` you should have an executable along your path named `git-pyinit`. This means you can run the following command

```console
git pyinit -h
```

and see the help. git-pyinit has a few args, and all others are __assumed__ got be for `git init`. If you do not specify a directory argument, then it will act as if your __current__ directory will be the init argument and will try to create it.

#### Example

If you are unfamiliar with hatch, you should read up on it [here](https://hatch.pypa.io/latest/)

Running the following command:

```console
git pyinit "test dir"
```

will create the following directory structure locally

![dir-structure](./_images/directory_structure.png)

and will create this default yaml file

![yaml-file](./_images/default_yaml.png)

* These will be the default github actions
