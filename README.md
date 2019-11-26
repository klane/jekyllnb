# JekyllNB: Host Jupyter Notebooks on Jekyll Sites

[![Test Status](https://github.com/klane/jekyllnb/workflows/Tests/badge.svg)](https://github.com/klane/jekyllnb/actions)
[![Documentation Status](https://img.shields.io/readthedocs/jekyllnb.svg?label=Docs&logo=read%20the%20docs)](https://jekyllnb.readthedocs.io/en/latest)
[![Coverage Status](https://img.shields.io/codecov/c/github/klane/jekyllnb.svg?label=Coverage&logo=codecov)](https://codecov.io/gh/klane/jekyllnb)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=klane/jekyllnb)](https://dependabot.com)
[![License](https://img.shields.io/github/license/klane/jekyllnb.svg?label=License)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

JekyllNB extends Jupyter's command line tool `nbconvert` to add the Jekyll header to Markdown files and save generated images to a desired location. This allows you to easily convert all your notebooks to the required format and immediately build your Jekyll site.

## Installation (coming soon)

JekyllNB is available on PyPI and can be installed with `pip`.

```bash
pip install jekyllnb
```

## Usage

JekyllNB is a Jupyter app just like `nbconvert`. Call it with `jupyter jekyllnb`. The preprocessor reads metadata from your notebook to populate the Jekyll header. Add a `jekyll` section to your notebook metadata similar to:

```
"jekyll": {
    "layout": "notebook",
    "permalink": "/hello/",
    "title": "Hello World!"
}
```

The exporter will add the following header to the generated Markdown:

```
---
layout: notebook
permalink: /hello/
title: Hello World!
---
```

## Options

Since `jekyllnb` extends `nbconvert`, all existing options are supported. The following new options are available:

- `--site-dir`: Root directory of your Jekyll site. Generated Markdown files and images will be saved relative to this location.
- `--image-dir`: Alias for the `nbconvert` option `NbConvertApp.output_files_dir`. This is where your images will be saved relative to `--site-dir`.

## nbconvert

JekyllNB also supports `nbconvert` by registering an entry point for the exporter. You can use the Jekyll exporter from `nbconvert` by calling `jupyter nbconvert --to jekyll`.

**Note**: The `--site-dir` and `--image-dir` options above are not available with `nbconvert`.
