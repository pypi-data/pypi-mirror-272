from pathlib import Path
import shutil
from iccicd.repo import PyProjectInterface, SphinxInterface


def get_test_data_dir():
    return Path(__file__).parent / "data"


def test_bump_pyproject_version():

    repo_dir = get_test_data_dir() / "version_bump"
    shutil.copy(
        repo_dir / "testpyproject.toml", repo_dir / "testpyproject_working.toml"
    )

    pyproject = PyProjectInterface(repo_dir, "testpyproject_working.toml")
    pyproject.bump_version("minor")

    version = pyproject.get_version()
    (repo_dir / "testpyproject_working.toml").unlink()

    assert version.major == 0
    assert version.minor == 1
    assert version.patch == 0


def test_set_sphinx_version():

    repo_dir = get_test_data_dir() / "version_bump"
    shutil.copy(repo_dir / "docs" / "conf.xpy", repo_dir / "docs" / "conf_working.xpy")

    sphinx = SphinxInterface(repo_dir, Path("docs/conf_working.xpy"))
    sphinx.set_version("1.2.3")

    version = sphinx.get_version()
    (repo_dir / "docs" / "conf_working.xpy").unlink()

    assert version == "1.2.3"
