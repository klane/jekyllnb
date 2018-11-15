# JekyllNB: Prep Jupyter Notebooks for Jekyll Sites

[![GitHub License](https://img.shields.io/github/license/klane/jekyllnb.svg)](https://github.com/klane/jekyllnb/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/klane/jekyllnb.svg?branch=master)](https://travis-ci.org/klane/jekyllnb)
[![codecov](https://codecov.io/gh/klane/jekyllnb/branch/master/graph/badge.svg)](https://codecov.io/gh/klane/jekyllnb)

--------------------------------------------------------------------------------

JekyllNB extends Jupyter's command line tool nbconvert to add the Jekyll header to Markdown files and move generated images to a desired location. It is called with `jupyter jekyllnb`.

## Options

- `--image-dir`: Alias for `NbConvertApp.output_files_dir`
- `--site-dir`: Root directory of the Jekyll site

## nbconvert

The Jekyll exporter also works with nbconvert simply by calling `jupyter nbconvert --to jekyll`
