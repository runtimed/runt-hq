# Linting configuration

Runt-hq uses the [pre-commit](https://pre-commit.com/) hook to ensure that all
of the lint rules are followed.

The set of enforced rules include:

- Ruff (both for formatting as well as for linting)
- mypy
- uv lock file

The configuration for the pre-commit hooks are set in the
[.pre-commit-config.yaml](../.pre-commit-config.yaml) file. You can install the
hooks by runnig `pre-commit install` and

The individual tool configurations should generally be set in the
[pyproject.toml](../pyproject.toml) file wherever possible
