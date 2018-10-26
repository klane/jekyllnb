import click
import os
from traitlets.config import Config
from nbconvert import MarkdownExporter


# setup command line arguments and options
@click.command()
@click.argument('notebook')
@click.option('--template', default=os.path.join(os.path.dirname(__file__), 'templates', 'jekyll.tpl'))
@click.option('--outdir', default='images')
def cli(notebook, template, outdir):
    basename = os.path.basename(notebook)
    notebook_name = basename[:basename.rfind('.')]

    resources = {}
    resources['unique_key'] = notebook_name
    resources['output_files_dir'] = os.path.join(outdir, notebook_name)

    config = Config()
    exporter = MarkdownExporter(config=config, template_file=template,
                                filters={'jekyllpath': jekyllpath})
    exporter.from_filename(notebook, resources=resources)


def base64image(image):
    possibles = ["image/png", "image/jpeg", "image/svg+xml", "image/gif"]
    for possible in possibles:
        if possible in image['data'].keys():
            mimetype = possible
    return 'data:' + mimetype + ";base64," + image['data'][mimetype]


def jekyllpath(path):
    # convert default image path to one compatible with Jekyll
    return path.replace("./", "{{site.url}}{{site.baseurl}}/")
