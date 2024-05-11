# py-dcqc

<!--
[![ReadTheDocs](https://readthedocs.org/projects/dcqc/badge/?version=latest)](https://sage-bionetworks-workflows.github.io/dcqc/)
-->
[![PyPI-Server](https://img.shields.io/pypi/v/dcqc.svg)](https://pypi.org/project/dcqc/)
[![codecov](https://codecov.io/gh/Sage-Bionetworks-Workflows/py-dcqc/branch/main/graph/badge.svg?token=OCC4MOUG5P)](https://codecov.io/gh/Sage-Bionetworks-Workflows/py-dcqc)
[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](#pyscaffold)

> Python package for performing quality control (QC) for data coordination (DC)

This Python package provides a framework for performing quality control (QC) on data files. Quality control can range from low-level integrity checks (_e.g._ MD5 checksum, file extension) to high-level checks such as conformance to a format specification and consistency with associated metadata.

Early versions of this package were developed to be used by its sibling, the [nf-dcqc](https://github.com/Sage-Bionetworks-Workflows/nf-dcqc) Nextflow workflow. You can see examples of how to leverage py-dcqc there. Note that the initial command-line interface (CLI) was developed with nf-dcqc in mind, so smaller steps were favored to enable parallelism in Nextflow. Future iterations of this package will include user-friendly, high-level CLI commands.

# PyScaffold

This project has been set up using PyScaffold 4.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.

```console
putup --name dcqc --markdown --github-actions --pre-commit --license Apache-2.0 py-dcqc
```
