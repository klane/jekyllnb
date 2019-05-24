import os
import re
import sys

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
    'image-dir': 'NbConvertApp.output_files_dir',
    'site-dir': 'JekyllNB.site_dir'
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
    def parse_command_line(self, argv=None):
        argv = sys.argv[1:] if argv is None else argv

        try:
            index_site = ['site-dir' in arg for arg in argv].index(True)
            index_output = ['output-dir' in arg for arg in argv].index(True)

            build_dir = os.path.join(argv[index_site+1], argv[index_output+1])
            argv[index_output+1] = build_dir
        except ValueError:
            pass

        super(JekyllNB, self).parse_command_line(argv)

    def init_single_notebook_resources(self, notebook_filename):
        if self.auto_folder:
            self.output_files_dir = os.path.join(self.output_files_dir, '{notebook_name}')

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
