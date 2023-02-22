<!-- Shields -->
[![codecov](https://codecov.io/gh/maekind/github_crawler/branch/main/graph/badge.svg?token=L8IS93O0XV)](https://codecov.io/gh/maekind/github_crawler)<!-- [![codecov](https://img.shields.io/codecov/c/github/maekind/python_samples?label=codecov&logo=codecov)](https://codecov.io/gh/maekind/python_samples) -->
[![build](https://img.shields.io/github/actions/workflow/status/maekind/github_crawler/.github/workflows/pythonpackage.yaml)](https://github.com/maekind/github_crawler) <!-- TODO: This should point to the pypi package -->
[![licence](https://img.shields.io/badge/License-MIT-orange.svg)](https://github.com/maekind/github_crawler/blob/main/LICENSE)
[![size](https://img.shields.io/github/repo-size/maekind/github_crawler)](https://github.com/maekind/github_crawler)
[![last_commit](https://img.shields.io/github/last-commit/maekind/github_crawler?color=violet)](https://github.com/maekind/github_crawler)
[![language](https://img.shields.io/github/languages/top/maekind/github_crawler?color=yellowgreen)](https://github.com/maekind/github_crawler)

# Github search crawler 

## Description

<a href="https://confluence.rdpnts.com/display/IKB/Python+developer+technical+task">See task description</a>

## Environment configuration

In order to execute the crawler protype, you have to create a virtual environment.
The following statement upgrades your current pip installation and installs the pipenv virtual environment.

`$> pip install --upgrade pip && pip install pipenv`

Then, you have to install the required packages.

`$> pipenv install`

# Activating the virtual environment

To activate the virtual environment, exceute the following command:

`$> pipenv shell`

## Testing

From the root folder run the following command:

`$> pytest tests -v --cov=./src --cov-report=xml:./coverage.xml --cov-report term-missing --cov-fail-under=90`

## Crawler execution

A main.py file is provided in the root folder.
The main program expects the following parameters:
- -i / --input: a json file following the format describer in the task description. This parameter is mandatory.
- -o / --output [optional]: a json file name to store the results.
- -v / --verbose [optional]: flag to let know the application to show debug messages. By default, logging is configured in the INFO level. So, debug messages won't be shown.
- -c / --console-logging [optional]: flag to let know the application to show logging messages in to the standard output. By default, logging is performed to a file and only the result is print to the stout.

Hereby there is an exemple:

`$> python3 main.py -v -i ./tests/repositories.json`

This command launches the crawler in debug mode and gathers information about repositories following the given searching keywords.

## Contributors

<a href="https://github.com/maekind/github_crawler/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=maekind/github_crawler" />
</a>

<a href="mailto:marco@marcoespinosa.es">Say hello!</a>
