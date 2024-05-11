from pathlib import Path
from typing import Any, cast
import logging
import tomlkit
from tomlkit import TOMLDocument

from iccicd.version import Version

logger = logging.getLogger(__name__)


class PyProjectInterface:
    def __init__(self, repo_path: Path, toml_file_name: str = "pyproject.toml") -> None:
        self.repo_path = repo_path
        self.toml_file_name = toml_file_name

    def get_version(self) -> Version:
        pyproject_path = self.repo_path / self.toml_file_name
        with open(pyproject_path, "r") as f:
            content = f.read()
        doc: dict[str, Any] = tomlkit.parse(content)
        return Version(doc["project"]["version"])

    def bump_version(self, bump_type: str) -> Version:
        pyproject_path = self.repo_path / self.toml_file_name
        logger.info(f"Bumping '{bump_type}' version in {pyproject_path}")
        with open(pyproject_path, "r") as f:
            content = f.read()
        doc: dict[str, Any] = tomlkit.parse(content)
        version = Version(doc["project"]["version"])

        if bump_type == "patch":
            version.patch += 1
        elif bump_type == "minor":
            version.patch = 0
            version.minor += 1
        elif bump_type == "major":
            version.major += 1
            version.minor = 0
            version.patch = 0

        doc["project"]["version"] = str(version)

        with open(pyproject_path, "w") as f:
            f.write(tomlkit.dumps(cast("TOMLDocument", doc)))

        logger.info(f"Version bumped to {version}")

        return version
