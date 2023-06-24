# Imagedup

A tool to manage image duplicates - program find image duplicates in a specified folder
and removes them if necessary.

## Installation

We recommend to use `pyenv` to manage necessary python version and `poetry` to manage
dependencies installation:
```sh
% brew install pyenv pyenv-virtualenv
```

Then the process of configuring the environment looks like following:
```sh
% pyenv install 3.9.1
% pyenv virtualenv 3.9.1 imagedup
% pyenv activate imagedup
```

Then install necessary dependencies:
```sh
% pip install poetry
% poetry config virtualenvs.create false
% poetry install --with-root
```

## Usage

You can run an `imagedup` command right from the repository root in the following way:
```sh
% python -m imagedup ./dataset
```

By default the tool does not delete files and simply prints the files to delete into
the standard output. If you want to delete duplicates, consider calling the tool like
following:
```sh
% python -m imagedup.shell ./dataset -q --rm
```
