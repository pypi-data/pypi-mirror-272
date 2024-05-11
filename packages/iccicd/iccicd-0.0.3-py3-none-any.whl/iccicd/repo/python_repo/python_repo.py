from pathlib import Path

from iccicd.repo import Repo
from iccicd.version import Version

from .pyproject_interface import PyProjectInterface
from .sphinx_interface import SphinxInterface


class PythonRepo(Repo):
    def __init__(self, path: Path) -> None:
        super().__init__(path)
        self.sphinx = SphinxInterface(self.path)
        self.pyproject = PyProjectInterface(self.path)

    def get_version(self) -> Version:
        return self.pyproject.get_version()

    def bump_version(self, bump_type: str):
        new_version = self.pyproject.bump_version(bump_type)
        self.sphinx.set_version(str(new_version))
