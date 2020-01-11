# Usage with nbconvert

JekyllNB also supports `nbconvert` by registering an entry point for the exporter.
You can use the Jekyll exporter with `nbconvert` by calling `jupyter nbconvert --to jekyll`.

**Note**: None of the options added by JekyllNB are available with `nbconvert`.

```text
site-dir
├── page-dir
│   └── notebook.md
└── image-dir
    └── notebook
        ├── image1.png
        └── image2.png
```

## Example

Calling `jupyter nbconvert --to jekyll --output-dir docs/_pages
--NbConvertApp.output_files_dir=assets/images/hello-world hello-word.ipynb`
with the notebook located [here](https://github.com/klane/jekyllnb/blob/master/tests/assets/hello-world.ipynb)
will result in the following site layout.

```text
docs
└── _pages
    ├── hello-world.md
    └── assets
        └── images
            └── hello-world
                └── hello-world_4_0.png
```
