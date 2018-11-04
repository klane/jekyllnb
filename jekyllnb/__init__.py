import os
from nbconvert.exporters import MarkdownExporter
from nbconvert.filters.strings import path2url
from nbconvert.preprocessors import Preprocessor
from traitlets import default
from traitlets.config import Config


class JekyllExporter(MarkdownExporter):
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

    def jekyllpath(self, path):
        # convert default image path to one compatible with Jekyll
        return "{{ site.baseurl }}/" + path2url(path)

    def default_filters(self):
        for pair in super(JekyllExporter, self).default_filters():
            yield pair
        yield ('jekyllpath', self.jekyllpath)


class JekyllPreprocessor(Preprocessor):
    def preprocess(self, nb, resources):
        metadata = nb.metadata.get('jekyll', {})
        resources['metadata']['layout'] = metadata.get('layout', 'page')
        resources['metadata']['title'] = metadata.get('title', None)
        resources['metadata']['permalink'] = metadata.get('permalink', None)

        return super(JekyllPreprocessor, self).preprocess(nb, resources)

    def preprocess_cell(self, cell, resources, cell_index):
        return cell, resources
