import click
import os
import re
import shutil
from nbconvert import MarkdownExporter
from nbconvert.writers import FilesWriter
from nbconvert.nbconvertapp import NbConvertApp, nbconvert_aliases
from traitlets import Unicode


jekyllnb_aliases = {}
jekyllnb_aliases.update(nbconvert_aliases)
jekyllnb_aliases.update({
    'img-dir': 'NbConvertApp.output_files_dir',
    'site-dir': 'JekyllNB.site_dir',
})


class JekyllNB(NbConvertApp):
    aliases = jekyllnb_aliases
    export_format = Unicode('jekyll')
    site_dir = Unicode('').tag(config=True)

    def start(self):
        if self.site_dir:
            build_dir = os.path.join(self.site_dir, self.writer.build_directory)
            self.writer.build_directory = build_dir

        super(JekyllNB, self).start()

        if self.site_dir:
            img_dir = os.path.join(self.writer.build_directory,
                                   self.output_files_dir.split(os.path.sep)[0])
            shutil.move(img_dir, self.site_dir)


# setup command line arguments and options
@click.command()
@click.argument('notebook')
@click.option('--layout', default='page')
@click.option('--template', default=os.path.join(os.path.dirname(__file__), 'templates',
                            'jekyll.tpl'))
@click.option('--outdir', default='images')
def cli(notebook, layout, template, outdir):
    basename = os.path.basename(notebook)
    notebook_name = basename[:basename.rfind('.')]

    resources = {}
    resources['metadata'] = {}
    resources['unique_key'] = notebook_name
    resources['output_files_dir'] = os.path.join(outdir, notebook_name)
    resources['metadata']['layout'] = layout
    resources['metadata']['title'] = re.sub(r"[_-]+", " ", notebook_name).title()

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
