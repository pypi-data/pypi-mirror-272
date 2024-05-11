#!/usr/bin/env python3

import os
import argparse
import logging
from pathlib import Path

from iccore import logging_utils
from iccore import runtime

from iccicd.packaging import PyPiContext, PythonPackage
from iccicd.repo import PythonRepo
from iccicd.version_control.gitlab import GitlabInterface, GitlabProject, GitlabUser

logger = logging.getLogger(__name__)


def launch_common(args):
    runtime.ctx.set_is_dry_run(args.dry_run)
    logging_utils.setup_default_logger()


def deploy(args):
    launch_common(args)

    print("into deployment")
    logger.info("Doing deployment")

    pypi_ctx = PyPiContext(args.pypi_token, args.use_test_pypi)
    package = PythonPackage(args.repo_dir)
    package.build()
    package.upload(pypi_ctx)

    logger.info("Finished deployment")


def bump_version(args):
    launch_common(args)

    logger.info("Bumping version number")

    repo = PythonRepo(args.repo_dir)
    repo.bump_version(args.bump_type)

    logger.info("Finished bumping version number")


def gitlab_ci_push(args):
    launch_common(args)

    logger.info("CI pushing state of current checkout")

    user = GitlabUser(args.user_name, args.user_email)
    project = GitlabProject(args.instance_url, args.repo_url)

    gitlab = GitlabInterface(project, user, args.access_token)
    gitlab.push_change_ci(args.message)

    logger.info("CI finished pushing state of current checkout")


def main_cli():
    print("called main cli")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry_run",
        type=bool,
        default=False,
        help="Dry run script - don't make real changes",
    )
    subparsers = parser.add_subparsers(required=True)

    deploy_parser = subparsers.add_parser("deploy")
    deploy_parser.add_argument(
        "--repo_dir",
        type=Path,
        default=Path(os.getcwd()),
        help="Path to the repo to be deployed",
    )

    deploy_parser.add_argument(
        "--pypi_token",
        type=str,
        default="",
        help="Token for uploading packages to PyPI",
    )

    deploy_parser.add_argument(
        "--use_test_pypi", type=bool, default=False, help="Use the testpypi repository"
    )
    deploy_parser.set_defaults(func=deploy)

    bump_parser = subparsers.add_parser("version_bump")
    bump_parser.add_argument(
        "--repo_dir",
        type=Path,
        default=Path(os.getcwd()),
        help="Path to the repo to be version bumped",
    )

    bump_parser.add_argument(
        "--bump_type",
        type=str,
        default="patch",
        help="Whether to bump 'major', 'minor' or 'patch' version",
    )
    bump_parser.set_defaults(func=bump_version)

    ci_push_parser = subparsers.add_parser("ci_push")
    ci_push_parser.add_argument("--user_name", type=str, help="Name of the CI user")
    ci_push_parser.add_argument("--user_email", type=str, help="Email of the CI user")
    ci_push_parser.add_argument(
        "--instance_url", type=str, help="Url for the target ci instance"
    )
    ci_push_parser.add_argument(
        "--repo_url", type=str, help="Url for the repo relative to the ci instance"
    )
    ci_push_parser.add_argument(
        "--access_token", type=str, help="Oath access token for the repo"
    )
    ci_push_parser.add_argument("--message", type=str, help="Commit message")
    ci_push_parser.set_defaults(func=gitlab_ci_push)

    args = parser.parse_args()
    args.func(args)
    print("args parsed")


if __name__ == "__main__":
    main_cli()
