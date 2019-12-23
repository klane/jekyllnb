# JekyllNB: Jupyter Notebooks to Jekyll Markdown

[![Test Status](https://github.com/klane/jekyllnb/workflows/Tests/badge.svg)](https://github.com/klane/jekyllnb/actions)
[![Documentation Status](https://img.shields.io/readthedocs/jekyllnb.svg?label=Docs&logo=read%20the%20docs)](https://jekyllnb.readthedocs.io/en/latest)
[![Coverage Status](https://img.shields.io/codecov/c/github/klane/jekyllnb.svg?label=Coverage&logo=codecov)](https://codecov.io/gh/klane/jekyllnb)
[![PyPI Version](https://img.shields.io/pypi/v/jekyllnb?label=Version&logo=pypi)](https://pypi.org/project/jekyllnb)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=klane/jekyllnb)](https://dependabot.com)
[![License](https://img.shields.io/github/license/klane/jekyllnb.svg?label=License)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-black-000000.svg)](https://github.com/psf/black)

JekyllNB extends Jupyter's command line tool `nbconvert` to add the Jekyll header to Markdown files and save generated images to a desired location.
This allows you to easily convert all your notebooks to the required format and immediately build your Jekyll site.

## Installation

JekyllNB is available on PyPI and can be installed with `pip`.

```bash
pip install jekyllnb
```

## Usage

JekyllNB is a Jupyter app just like `nbconvert`. Call it with `jupyter jekyllnb`.
The preprocessor reads metadata from your notebook to populate the Jekyll header.
Add a `jekyll` section to your notebook metadata similar to:

```json
"jekyll": {
    "layout": "notebook",
    "permalink": "/hello/",
    "title": "Hello World!"
}
```

The exporter will add the following header to the generated Markdown:

```text
---
layout: notebook
permalink: /hello/
title: Hello World!
---
```

## Options

Since `jekyllnb` extends `nbconvert`, all existing options are supported. The following new options are available:

- `--site-dir`: Root directory of your Jekyll site. Markdown (`page-dir`) and image (`image-dir`) folders will be created here if they do not exist.
- `--page-dir`: Directory for generated Markdown files (e.g. _pages or _posts).
- `--image-dir`: Directory for images. Images are organized into folders for each notebook by default.
Alias for the `nbconvert` option `NbConvertApp.output_files_dir`.
- `--no-auto-folder`: Flag to turn off the default behavior of organizing images by notebook name within `image-dir`. (default: `false`)

## nbconvert

JekyllNB also supports `nbconvert` by registering an entry point for the exporter.
You can use the Jekyll exporter with `nbconvert` by calling `jupyter nbconvert --to jekyll`.

**Note**: The options above are not available with `nbconvert`.
