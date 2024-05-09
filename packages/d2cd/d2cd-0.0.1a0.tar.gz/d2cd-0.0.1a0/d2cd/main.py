#!/usr/bin/env python3

"""
Main module
"""

import os
import time

from .banner import display_info
from .cli import parse_arguments
from .config_loader import ConfigLoader
from .utils.docker_compose_utils import DockerComposeUtils
from .utils.git_utils import GitUtils
from .utils.logger import log


def main():
    args = parse_arguments()
    if args.debug:
        log.level("DEBUG")

    cfg = ConfigLoader(config_file=args.config_file)
    config = cfg.get_config()

    display_info()

    for repo in config["repos"]:
        with GitUtils(
            branch=repo["branch"],
            repo_url=repo["url"],
            auth=repo["auth"],
        ) as gt:
            gt.clone_repository()

    log.info("Start reconciliation in loop")
    first_iteration = True

    while True:
        for repo in config["repos"]:
            with GitUtils(branch=repo["branch"], repo_url=repo["url"]) as gt:
                if gt.pull_changes():
                    full_paths = [
                        os.path.join(gt.repo_location, path)
                        for path in repo["docker_compose_paths"]
                    ]
                    with DockerComposeUtils(compose_files=full_paths) as dc:
                        if first_iteration:
                            dc.up()
                            first_iteration = False
                else:
                    log.info("No changes in upstream git repo")
        time.sleep(config["sync_interval_seconds"])
