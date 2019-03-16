import os
import re
import shutil
import sys

import click
from nbconvert import MarkdownExporter
from nbconvert.writers import FilesWriter
from nbconvert.nbconvertapp import NbConvertApp, nbconvert_aliases
from traitlets import Unicode, default, observe
from traitlets.config import catch_config_error


jekyllnb_aliases = {}
jekyllnb_aliases.update(nbconvert_aliases)
jekyllnb_aliases.update({
    'image-dir': 'NbConvertApp.output_files_dir',
    'site-dir': 'JekyllNB.site_dir',
})


class JekyllNB(NbConvertApp):
    aliases = jekyllnb_aliases
    site_dir = Unicode('').tag(config=True)

    @default('export_format')
    def _export_format_default(self):
        return 'jekyll'

    @observe('export_format')
    def _export_format_changed(self, change):
        default = self._export_format_default()

        if change['new'].lower() != default:
            raise ValueError('Invalid export format {}, value must be {}'
                            .format(change['new'], default))

    @catch_config_error
    def initialize(self, argv=None):
        argv = sys.argv[1:] if argv is None else argv

        try:
            index_site = ['site-dir' in arg for arg in argv].index(True)
            index_output = ['output-dir' in arg for arg in argv].index(True)

            build_dir = os.path.join(argv[index_site+1], argv[index_output+1])
            argv[index_output+1] = build_dir
        except ValueError:
            pass

        super(JekyllNB, self).initialize(argv)

    def start(self):
        super(JekyllNB, self).start()

        if self.site_dir:
            image_dir = os.path.join(self.writer.build_directory,
                                     self.output_files_dir.split(os.path.sep)[0])
            shutil.move(image_dir, self.site_dir)


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
