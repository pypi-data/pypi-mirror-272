#!/usr/bin/env python3

"""
Docker Compose Utils
"""

from python_on_whales import DockerClient, docker

from .logger import log


class DockerComposeUtils:
    def __init__(self, compose_files=None):
        self.docker_client = DockerClient(compose_files=compose_files)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @staticmethod
    def version():
        return docker.compose.version()

    def up(self):
        """Run docker-compose up."""
        log.info("Run docker-compose up...")

        self.docker_client.compose.up(
            detach=True, quiet=True, build=True, remove_orphans=True, pull="always"
        )

    def ps(self):
        """Run docker-compose ps."""
        log.info("Run docker-compose ps...")
        self.docker_client.compose.ps()

    def restart(self):
        """Run docker-compose restart."""
        log.info("Run docker-compose restart...")
        self.docker_client.compose.restart()

    def ls(self):
        """Run docker-compose ls."""
        log.info("Run docker-compose ls...")
        self.docker_client.compose.ls()

    def down(self):
        """Run docker-compose down."""
        log.info("Run docker-compose down...")
        self.docker_client.compose.down()
