# `catc`: Configuration driven file concatenation tool

[![PyPI version](https://badge.fury.io/py/catc.svg)](https://pypi.org/project/catc)
[![Testsuite](https://github.com/01Joseph-Hwang10/catc/workflows/Test%20and%20Lint/badge.svg)](https://github.com/01Joseph-Hwang10/catc/actions?query=workflow%3A"Test+and+Lint")
[![Python version](https://img.shields.io/pypi/pyversions/catc.svg)](https://pypi.org/project/catc)
[![Project Status](https://img.shields.io/pypi/status/catc.svg)](https://pypi.org/project/catc/)
[![Supported Interpreters](https://img.shields.io/pypi/implementation/catc.svg)](https://pypi.org/project/catc/)
[![License](https://img.shields.io/pypi/l/catc.svg)](https://github.com/pawelzny/catc/blob/master/LICENSE)


`catc` (conCATenate by Configuration) is a file concatenation tool that allows you to concatenate files based on a configuration file.

## Quick Start

First, install `catc`:

```bash
pip install catc
```

Then, create a `catc.json` file in the root of your project,
and specify the files you want to concatenate:

```json
{
  "files": [
    "src/file.txt",
    "src/lib/**/*.txt"
  ],
  "output": "dist/merged.txt",
  "separator": "\n"
}
```

Finally, run `catc` to concatenate the files:

```bash
catc <directory/to/catc.json>
```

## API Documentation

> TODO: description

## Contributing

Any contribution is welcome! Check out [CONTRIBUTING.md](https://github.com/01Joseph-Hwang10/catc/blob/master/.github/CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](https://github.com/01Joseph-Hwang10/catc/blob/master/.github/CODE_OF_CONDUCT.md) for more information on how to get started.

## License

`ldm` is licensed under a [MIT License](https://github.com/01Joseph-Hwang10/catc/blob/master/LICENSE).