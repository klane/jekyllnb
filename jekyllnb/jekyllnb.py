import os
import re

import click
from nbconvert import MarkdownExporter
from nbconvert.writers import FilesWriter
from nbconvert.nbconvertapp import NbConvertApp, nbconvert_aliases, nbconvert_flags
from traitlets import Bool, Unicode, default, observe
from traitlets.config import catch_config_error

from .__version__ import __version__


jekyllnb_aliases = {}
jekyllnb_aliases.update(nbconvert_aliases)
jekyllnb_aliases.update({
    'site-dir': 'JekyllNB.site_dir',
    'page-dir': 'JekyllNB.page_dir',
    'image-dir': 'NbConvertApp.output_files_dir'
})

jekyllnb_flags = {}
jekyllnb_flags.update(nbconvert_flags)
jekyllnb_flags.update({
    'no-auto-folder': (
        {'JekyllNB': {'auto_folder': False}},
        'Do not create image folder with notebook name at image-dir level.'
    )
})


class JekyllNB(NbConvertApp):
    name = 'jupyter-jekyllnb'
    description = 'Convert Jupyter notebooks to Jekyll-ready Markdown'
    version = __version__

    aliases = jekyllnb_aliases
    flags = jekyllnb_flags

    auto_folder = Bool(True).tag(config=True)
    site_dir = Unicode('').tag(config=True)
    page_dir = Unicode('').tag(config=True)

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
        super(JekyllNB, self).initialize(argv)
        self.writer.build_directory = os.path.join(self.site_dir, self.page_dir)

        if self.auto_folder:
            self.output_files_dir = os.path.join(self.output_files_dir, '{notebook_name}')

    def init_single_notebook_resources(self, notebook_filename):
        resources = super(JekyllNB, self).init_single_notebook_resources(notebook_filename)
        resources['image_dir'] = resources['output_files_dir']
        resources['output_files_dir'] = os.path.join(self.site_dir,
                                                     resources['output_files_dir'])

        return resources


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

    resources = {
        'unique_key': notebook_name,
        'output_files_dir': os.path.join(outdir, notebook_name),
        'metadata': {'layout': layout,
                     'title': re.sub(r"[_-]+", " ", notebook_name).title()
                     }
    }

    exporter = MarkdownExporter(template_file=template,
                                filters={'jekyllpath': jekyllpath})
    output, resources = exporter.from_filename(notebook, resources=resources)

    writer = FilesWriter()
    writer.write(output, resources, notebook_name=notebook_name)


def jekyllpath(path):
    # convert default image path to one compatible with Jekyll
    return "{{ site.baseurl }}/" + path.replace("\\", "/")
