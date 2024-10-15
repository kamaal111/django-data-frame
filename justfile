# List available commands
default:
    just --list --unsorted

# Test
test:
    #!/bin/zsh

    . .venv/bin/activate
    pytest

# Test with code coverage
test-cov:
    #!/bin/zsh

    . .venv/bin/activate
    pytest --cov=src/django_data_frame tests/

# Build
build:
    rye build

# Clean then build
clean-build:
    rye build --clean

# Lint code
lint:
    #!/bin/zsh

    . .venv/bin/activate
    ruff check .

# Lint and fix any issues that can be fixed automatically
lint-fix:
    #!/bin/zsh

    . .venv/bin/activate
    ruff check . --fix

# Format code
format:
    #!/bin/zsh

    . .venv/bin/activate
    ruff format .

# Prepare project to work with
prepare: install-modules setup-pre-commit

# Bootstrap all the tools needed to run this project
bootstrap: install-rye prepare

# Run after creating dev container
post-dev-container-create:
    just .devcontainer/post-create
    just bootstrap

# Install modules
install-modules:
    #!/bin/zsh

    . "$HOME/.rye/env"

    rye sync

assert-has-no-diffs:
    #!/bin/bash

    current_branch=$(git symbolic-ref --short HEAD)
    diffs=$(git diff --name-only "origin/$current_branch" | sed '/^$/d' | awk '{print NR}'| sort -nr | sed -n '1p')
    just assert-is-empty "$diffs"

[private]
assert-is-empty value:
    #!.venv/bin/python

    value = "{{ value }}"
    assert value == "" or int(value) == 0

[private]
setup-pre-commit:
    #!/bin/zsh

    . .venv/bin/activate
    pre-commit install

[private]
install-rye:
    #!/bin/zsh

    . ~/.zshrc

    cp -f .devcontainer/rye-config.toml ~/.rye/config.toml
    curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes"  bash

    . "$HOME/.rye/env"

    mkdir -p ~/.zfunc
    rye self completion -s zsh > ~/.zfunc/_rye

    mkdir -p $ZSH_CUSTOM/plugins/rye
    rye self completion -s zsh > $ZSH_CUSTOM/plugins/rye/_rye
