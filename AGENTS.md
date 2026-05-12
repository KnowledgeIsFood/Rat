# AGENTS.md

## Cursor Cloud specific instructions

This repository ("Rat") is currently an empty scaffold with only a `README.md`. There are no applications, services, dependencies, build tools, tests, or linting configured.

### Current state
- No source code or application logic exists yet.
- No package manager lockfiles or dependency manifests are present.
- No `Makefile`, `Dockerfile`, `docker-compose.yml`, or CI configuration exists.
- No test framework or lint tooling is configured.

### For future agents
- Once source code and dependencies are added, update this file with service startup instructions, test commands, and any non-obvious caveats.
- Update the VM update script (via `SetupVmEnvironment`) to install project dependencies once a dependency manifest is committed.
