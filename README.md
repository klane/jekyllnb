# JekyllNB: Host Jupyter Notebooks on Jekyll Sites with Ease

[![GitHub License](https://img.shields.io/github/license/klane/jekyllnb.svg)](https://github.com/klane/jekyllnb/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/klane/jekyllnb.svg?branch=master)](https://travis-ci.org/klane/jekyllnb)
[![codecov](https://codecov.io/gh/klane/jekyllnb/branch/master/graph/badge.svg)](https://codecov.io/gh/klane/jekyllnb)

JekyllNB extends Jupyter's command line tool `nbconvert` to add the Jekyll header to Markdown files and save generated images to a desired location. This allows you to easily convert all your notebooks to the required format and immediately build your Jekyll site.

## Installation (coming soon)

JekyllNB is hosted on PyPI and can be installed with `pip`.

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
