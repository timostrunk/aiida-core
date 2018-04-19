#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import os
import sys

@click.command()
def validate_pyproject():
    """
    Ensure that the version of reentry in setup_requirements.py and pyproject.toml are identical
    """
    import setup_requirements
    import toml

    filename_pyproject = 'pyproject.toml'
    filename_requirements = 'setup_requirements.py'

    dir_path = os.path.dirname(os.path.realpath(__file__))
    toml_file = os.path.join(dir_path, os.pardir, filename_pyproject)

    reentry_requirement = None

    for requirement in setup_requirements.install_requires:
        if 'reentry' in requirement:
            reentry_requirement = requirement
            break

    if reentry_requirement is None:
        click.echo('Could not find the reentry requirement in {}'.format(filename_requirements), err=True)
        sys.exit(1)

    try:
        with open(toml_file, 'r') as handle:
            toml_string = handle.read()
    except IOError as exception:
        click.echo('Could not read the required file: {}'.format(toml_file), err=True)
        sys.exit(1)

    try:
        parsed_toml = toml.loads(toml_string)
    except Exception as exception:
        click.echo('Could not parse {}: {}'.format(toml_file, exception), err=True)
        sys.exit(1)

    try:
        pyproject_toml_requires = parsed_toml['build-system']['requires']
    except KeyError as exception:
        click.echo('Could not retrieve the build-system requires list from {}'.format(toml_file), err=True)
        sys.exit(1)

    if reentry_requirement not in pyproject_toml_requires:
        click.echo('Reentry requirement from {} {} is not mirrored in {}'.format(
            filename_requirements, reentry_requirement, toml_file), err=True)
        sys.exit(1)


if __name__ == '__main__':
    validate_pyproject()  # pylint: disable=no-value-for-parameter
