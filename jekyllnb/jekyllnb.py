import click
import os
import re
from nbconvert import MarkdownExporter
from nbconvert.writers import FilesWriter


# setup command line arguments and options
@click.command()
@click.argument('notebook')
@click.option('--layout', default='page')
@click.option('--template', default=os.path.join(os.path.dirname(__file__), 'templates', 'jekyll.tpl'))
@click.option('--outdir', default='images')
def cli(notebook, layout, template, outdir):
    basename = os.path.basename(notebook)
    notebook_name = basename[:basename.rfind('.')]

    resources = {}
    resources['metadata'] = {}
    resources['unique_key'] = notebook_name
    resources['output_files_dir'] = os.path.join(outdir, notebook_name)
    resources['metadata']['layout'] = layout
    resources['metadata']['title'] = re.sub(r"[_-]+"," ", notebook_name).title()

    exporter = MarkdownExporter(template_file=template,
                                filters={'jekyllpath': jekyllpath})
    output, resources = exporter.from_filename(notebook, resources=resources)

    writer = FilesWriter()
    writer.write(output, resources, notebook_name=notebook_name)


def jekyllpath(path):
    # convert default image path to one compatible with Jekyll
    return "{{ site.baseurl }}/" + path.replace("\\", "/")


if __name__ == "__main__":
    cli()
