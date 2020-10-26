# JekyllNB: Jupyter Notebooks to Jekyll Markdown

[![Test Status](https://github.com/klane/jekyllnb/workflows/Tests/badge.svg)](https://github.com/klane/jekyllnb/actions)
[![Documentation Status](https://img.shields.io/readthedocs/jekyllnb?label=Docs&logo=read%20the%20docs&logoColor=white)](https://jekyllnb.readthedocs.io/en/latest)
[![Coverage Status](https://img.shields.io/codecov/c/github/klane/jekyllnb?label=Coverage&logo=codecov)](https://codecov.io/gh/klane/jekyllnb)
[![LGTM](https://img.shields.io/lgtm/alerts/github/klane/jekyllnb?label=Alerts&logo=lgtm)](https://lgtm.com/projects/g/klane/jekyllnb/alerts)
[![DeepSource](https://deepsource.io/gh/klane/jekyllnb.svg/?label=active+issues)](https://deepsource.io/gh/klane/jekyllnb/?ref=repository-badge)
[![PyPI Version](https://img.shields.io/pypi/v/jekyllnb?color=blue&label=Version&logo=python&logoColor=white)](https://pypi.org/project/jekyllnb)
[![Downloads](https://static.pepy.tech/personalized-badge/jekyllnb?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/jekyllnb)
[![License](https://img.shields.io/github/license/klane/jekyllnb?color=blue&label=License)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-black-black)](https://github.com/psf/black)

JekyllNB extends Jupyter's command line tool `nbconvert` to add the Jekyll front matter to Markdown files and save generated images to a desired location.
This allows you to easily convert all your notebooks to the required format and immediately build your Jekyll site.
It works great in a GitHub Actions workflow to convert your notebooks to Markdown and deploy to GitHub Pages.
See JekyllNB in action [here](https://github.com/klane/databall/blob/master/.github/workflows/gh-pages.yml).

## Installation

JekyllNB is available on PyPI and can be installed with `pip`.

```bash
pip install jekyllnb
```

## Usage

JekyllNB is a Jupyter app just like `nbconvert`. Call it with `jupyter jekyllnb`.
The preprocessor reads metadata from your notebook to populate the Jekyll front matter.
Add a `jekyll` section to your notebook metadata similar to:

```json
"jekyll": {
    "layout": "notebook",
    "permalink": "/hello/",
    "title": "Hello World!"
}
```

The exporter will add the following front matter to the generated Markdown:

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
