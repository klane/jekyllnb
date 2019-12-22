<h1>Multiple Notebooks</h1>

Multiple notebooks can be converted at once using a wildcard.
Calling `jupyter jekyllnb --site-dir docs --page-dir _pages --image-dir assets/images *.ipynb`

```text
docs
├── _pages
│   ├── hello-world.md
│   └── goodbye-world.md
└── assets
    └── images
        ├── hello-world
        │   ├── hello-world_1.png
        │   └── hello-world_2.png
        └── goodbye-world
            ├── goodbye-world_1.png
            └── goodbye-world_2.png
```

Adding the `--no-auto-folder` flag will place all images in `image-dir`.

```text
docs
├── _pages
│   ├── hello-world.md
│   └── goodbye-world.md
└── assets
    └── images
        ├── hello-world_1.png
        ├── hello-world_2.png
        ├── goodbye-world_1.png
        └── goodbye-world_2.png
```
