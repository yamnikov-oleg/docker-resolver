# Docker container hostnames resolver for host machine

This small script will poll docker for container starts and stops to update
host machines's `/etc/hosts` file.

There's another product for that called `resolvable`, but it didn't work for me,
therefore I've wrote my own utility for that.

## Usage

1. Clone the repo
2. `docker-compose up -d`

Now, if you start a container with name `website`, it will be available on
your host machine through `website.docker`.

If you don't like the `.docker` suffix, feel free to edit `cname_to_host` function in `listener.py`.
