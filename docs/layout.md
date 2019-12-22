<h1>Site Layout</h1>

All files are placed relative to `site-dir` (root directory) with Markdown files in `page-dir` and images in `image-dir`.
By default images are organized into folders for each notebook.

Given a Jupyter notebook `notebook.ipynb`, calling `jekyllnb` will result in the following site layout.

```text
site-dir
├── page-dir
│   └── notebook.md
└── image-dir
    └── notebook <──── auto-generated
        ├── image1.png
        └── image2.png
```

## Example

Calling `jupyter jekyllnb --site-dir docs --page-dir _pages --image-dir assets/images hello-word.ipynb`
with the notebook located [here](https://github.com/klane/jekyllnb/blob/master/tests/assets/hello-world.ipynb)
will result in the following site layout.

```text
docs
├── _pages
│   └── hello-world.md
└── assets
    └── images
        └── hello-world
            └── hello-world_4_0.png
```

Adding the `--no-auto-folder` flag will place all images in `image-dir`.

```text
docs
├── _pages
│   └── hello-world.md
└── assets
    └── images
        └── hello-world_4_0.png
```
