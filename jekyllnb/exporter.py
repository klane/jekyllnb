import os

from nbconvert.exporters import MarkdownExporter
from nbconvert.filters.strings import path2url
from traitlets import default
from traitlets.config import Config


class JekyllExporter(MarkdownExporter):
    resources = {}

    def from_filename(self, filename, resources=None, **kw):
        self.resources = resources
        return super(JekyllExporter, self).from_filename(
            filename, resources=resources, **kw
        )

    @default("template_file")
    def _template_file_default(self):
        return "jekyll"

    @property
    def template_path(self):
        return super(JekyllExporter, self).template_path + [
            os.path.join(os.path.dirname(__file__), "templates")
        ]

    @property
    def preprocessors(self):
        return super(JekyllExporter, self).preprocessors + [
            "jekyllnb.JekyllPreprocessor"
        ]

    @property
    def default_config(self):
        config = Config({"JekyllPreprocessor": {"enabled": True}})
        config.merge(super(JekyllExporter, self).default_config)
        return config

    def default_filters(self):
        for pair in super(JekyllExporter, self).default_filters():
            yield pair

        image_dir = self.resources.get("image_dir", self.resources["output_files_dir"])

        # convert image path to one compatible with Jekyll
        yield (
            "jekyllpath",
            lambda path: "{{ site.baseurl }}/"
            + path2url(os.path.join(image_dir, os.path.basename(path))),
        )
