# List available commands
default:
    just --list --unsorted --list-heading $'Available commands\n'

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

# Run after creating dev container
post-dev-container-create:
    just .devcontainer/post-create
    just bootstrap

# Bootstrap all the tools needed to run this project
bootstrap: install-rye install-modules setup-pre-commit

install-modules:
    #!/bin/zsh

    . "$HOME/.rye/env"

    rye sync

[private]
setup-pre-commit:
    #!/bin/zsh

    . .venv/bin/activate
    pre-commit install

[private]
install-rye:
    #!/bin/zsh

    . ~/.zshrc

    cp -f rye-config.toml ~/.rye/config.toml
    curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes"  bash

    . "$HOME/.rye/env"

    mkdir -p ~/.zfunc
    rye self completion -s zsh > ~/.zfunc/_rye

    mkdir -p $ZSH_CUSTOM/plugins/rye
    rye self completion -s zsh > $ZSH_CUSTOM/plugins/rye/_rye
