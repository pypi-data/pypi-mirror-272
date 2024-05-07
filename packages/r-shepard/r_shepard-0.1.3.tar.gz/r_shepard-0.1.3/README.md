# r-shepard

![Coverage Status](./coverage-badge.svg)

Simple, self-hosted solution for collaborative (not real-time) R computing leveraging podman,
RStudio, and Tailscale.

Built with Django and HTMX.

## Develop

First start the development environment:

```bash
devenv up # starts redis, celery worker and celery beat
run-tests # runs the tests
```

Then start the Django development server:

```bash
python manage.py runserver # This could also be done from your IDE / debugging environment
```

## Installation instructions (Ubuntu 22.04).

### Requirements

- Install [podman](https://podman.io/docs/installation) (used for running RStudio containers)

```bash
sudo apt install podman`
```

- Install [Tailscale](https://tailscale.com/kb/1187/install-ubuntu-2204) (used for secure access to the RStudio containers):

```bash
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.tailscale-keyring.list | sudo tee /etc/apt/sources.list.d/tailscale.list
sudo apt-get update
sudo apt-get install tailscale
```

- Install git (needed for auto-commit functionality)

```bash
sudo apt install git
```

- Install `redis-server` (needed for celery which is used for scheduling the auto-commit tasks)

```bash
sudo apt install redis-server
```

### Django app

```bash
pip install r-shepard
```

## Minimum Viable Product

- [ ] Add installation instructions for Ubuntu 22.04
- [ ] ~~[gitwatch](https://github.com/gitwatch/gitwatch?tab=readme-ov-file) integration~~ Rolled my own solution. Need to document and integrate it into the UI.
- [x] Publish on PyPi
- [x] ~~Add views for project creation~~ Django admin is enough for now.
- [x] Test R Project/Package management inside the container (e.g. `renv`)
- [x] Add Volume management
- [x] Setup Frontend framework (e.g. ~~Bootstrap~~, PicoCSS)
- [x] Setup 2FA
- [x] Add Tailscale Serve integration
- [x] Add basic container management via podman
- [x] Add basic views for projects and container management
- [x] ~~Add Tailscale Funnel integration~~ Not needed right now
- [x] ~~Make it possible to assign users to projects (only superusers should be able to create projects and assign users to them)~~ Not needed right now

## Potential Future Features

- LDAP integration
- container-specific and user-specific auto-commits
