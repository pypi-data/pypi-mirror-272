# d2cd
> **Note:** This project is currently under active development.

<p align="center">
  <img src="https://private-user-images.githubusercontent.com/8393701/328679398-d89d4abd-1d01-4536-9bd0-c129f733d17b.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTUxMTcyNDksIm5iZiI6MTcxNTExNjk0OSwicGF0aCI6Ii84MzkzNzAxLzMyODY3OTM5OC1kODlkNGFiZC0xZDAxLTQ1MzYtOWJkMC1jMTI5ZjczM2QxN2IucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI0MDUwNyUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDA1MDdUMjEyMjI5WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9MThkODQ3YmIxYmUzMjQ2YmMwMjk2NGFmMjQzYzk5NjZmNGZiOTAwNmVmZjA3MDllMTdmZjUxZTBkNTE2NjY3MiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmYWN0b3JfaWQ9MCZrZXlfaWQ9MCZyZXBvX2lkPTAifQ.xDJJRKF_nctcSnjHZIMeXHItVpgPbWJztQhmWJMNl0A" width="400"/>
</p>


**D**ocker **C**ompose **C**ontinuous **D**elivery (`d2cd`) is a GitOps agent designed to maintain the state of your Docker Compose projects on your server by continuously applying changes from a Git repository.

## Install
Docker Compose is the recomended way
```bash
# download docker-compose.yml
$ wget https://raw.githubusercontent.com/veerendra2/d2cd/main/docker-compose.yml

# configure and run
$ docker compose up -d
```
From source
> **Note:** This tool is currently in pre-alpha stage, and daemonization is not yet implemented.
```
$ git clone git@github.com:veerendra2/d2cd.git
$ cd d2cd
$ pip3 install .
```

## Configuration
Below is a sample `config.yml` file to help you get started:

```yaml
---
sync_interval_seconds: 600
repos:
  - name: d2cd-test
    url: git@github.com:veerendra2/d2cd-test-repo.git
    branch: main
    auth:
      ssh_key_location: "~/.ssh/id_rsa"
    docker_compose_paths:
      - python/docker-compose.yml
```
You can also use `username` and `password`(`token`) for authentication

```yaml
sync_interval_seconds: 600
repos:
  - name: d2cd-test
    url: git@github.com:veerendra2/d2cd-test-repo.git
    branch: main
    auth:
      username: "USERNAME"
      password: "PASSWORD"
    docker_compose_paths:
      - python/docker-compose.yml
```
