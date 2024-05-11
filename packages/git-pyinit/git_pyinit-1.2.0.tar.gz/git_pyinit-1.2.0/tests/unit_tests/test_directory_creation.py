import pytest

from git_pyinit.cli import main

proj_name = "project1"
expected_found_files = [
    "project1/pyproject.toml",
    "project1/README.md",
    "project1/LICENSE.txt",
    "project1/tests/__init__.py",
    "project1/.git/description",
    "project1/.git/config",
    "project1/.git/HEAD",
    "project1/src/project1/__about__.py",
    "project1/src/project1/__init__.py",
    "project1/.git/hooks/pre-merge-commit.sample",
    "project1/.git/hooks/sendemail-validate.sample",
    "project1/.git/hooks/pre-applypatch.sample",
    "project1/.git/hooks/update.sample",
    "project1/.git/hooks/pre-receive.sample",
    "project1/.git/hooks/pre-rebase.sample",
    "project1/.git/hooks/fsmonitor-watchman.sample",
    "project1/.git/hooks/post-update.sample",
    "project1/.git/hooks/pre-push.sample",
    "project1/.git/hooks/applypatch-msg.sample",
    "project1/.git/hooks/commit-msg.sample",
    "project1/.git/hooks/push-to-checkout.sample",
    "project1/.git/hooks/pre-commit.sample",
    "project1/.git/hooks/prepare-commit-msg.sample",
    "project1/.git/info/exclude",
    "project1/.github/workflows/lint.yml",
]


@pytest.fixture(scope="function")
def tempdir(tmp_path_factory):
    fn = tmp_path_factory.mktemp("tempdir") / "folder1" / proj_name
    yield fn


def test_failure(tempdir):
    with pytest.raises(FileNotFoundError):
        main([str(tempdir)])
    assert not get_file_structure(tempdir)


def get_file_structure(_dir, relative_to=None):
    if relative_to:
        return [x.relative_to(relative_to) for x in _dir.rglob("*") if x.is_file()]
    else:
        return [x for x in _dir.rglob("*") if x.is_file()]


def test_success(tempdir):
    main([str(tempdir), "--mkdir"])
    structure = get_file_structure(tempdir, relative_to=tempdir.parent)
    assert structure
    str_structure = [str(x) for x in structure]
    for file in expected_found_files:
        assert file in str_structure, f"{file} not found in {structure}"
