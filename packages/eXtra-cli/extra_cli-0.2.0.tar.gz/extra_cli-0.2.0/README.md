# eXtra

eXtra is a project management tool specifically designed for bioinformatics projects. It enables reproducible analysis of
large datasets, making it effortless to share and collaborate with others.


[![image](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat-square)](https://anaconda.org/bioconda/eXtra-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- [x] A human-readable configuration file
- [x] Git integration
- [x] Guaranteed reproducibility and portability
- [ ] Managing data, containers, and workflows, all in one place

## Installation

The easiest way to install eXtra is to use pip:

```bash
pip install eXtra-cli
```

## Quickstart

To get started with eXtra, use the `eXtra init` command to create a new project:

```bash
eXtra init my_project # This will by default create a Git repository
cd my_project
```

To add a new dataset to your project, use the `eXtra add` command:

```bash
eXtra add SRP123456 # ENCSR123ABC, GSE123456, etc. are also supported
```

You can also add privately hosted datasets:

```bash
eXtra add me@some_host:path/to/my_dataset ftp://ftp.example.com/another_dataset
```

If you share your project with others, they can easily retrieve the datasets you added:

```bash
eXtra install
```

For more information, please refer to [examples](examples/README.md).

## License

This project is licensed under the MIT license. See [LICENSE](LICENSE) for details.
