import os

from nbconvert.exporters import MarkdownExporter
from nbconvert.filters.strings import path2url
from traitlets import default
from traitlets.config import Config


class JekyllExporter(MarkdownExporter):
    resources = {}

    def from_filename(self, filename, resources=None, **kw):
        self.resources = resources
        return super(JekyllExporter, self).from_filename(filename, resources=resources, **kw)

    @default('template_file')
    def _template_file_default(self):
        return 'jekyll'

    @property
    def template_path(self):
        return super(JekyllExporter, self).template_path + \
            [os.path.join(os.path.dirname(__file__), "templates")]

    @property
    def preprocessors(self):
        return super(JekyllExporter, self).preprocessors+["jekyllnb.JekyllPreprocessor"]

    @property
    def default_config(self):
        c = Config({'JekyllPreprocessor': {'enabled': True}})
        c.merge(super(JekyllExporter, self).default_config)
        return c

    def default_filters(self):
        for pair in super(JekyllExporter, self).default_filters():
            yield pair

        site_dir = self.resources.get('site_dir', '')

        if site_dir and not site_dir.endswith('/'):
            site_dir = site_dir + '/'

        # convert image path to one compatible with Jekyll
        yield ('jekyllpath', lambda path: "{{ site.baseurl }}/" +
                                          path2url(path.replace(site_dir, '')))
