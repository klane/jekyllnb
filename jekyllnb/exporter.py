import os

from nbconvert.exporters import MarkdownExporter
from nbconvert.filters.strings import path2url
from traitlets import default
from traitlets.config import Config


class JekyllExporter(MarkdownExporter):
    """Exporter to write Markdown with Jekyll metadata"""

    resources = {}

    def from_filename(self, filename, resources=None, **kwargs):
        """Convert notebook from a file

        Args:
            filename (str): Full filename of the notebook to convert.
            resources (dict): Additional resources used by preprocessors and filters.
            `**kwargs`: Ignored

        Returns:
            NotebookNode: Converted notebook.
            dict: Resources dictionary.
        """
        self.resources = resources
        return super(JekyllExporter, self).from_filename(
            filename, resources=resources, **kwargs
        )

    @default("template_file")
    def _template_file_default(self):  # skipcq: PYL-R0201
        """Default template file"""
        return "jekyll"

    @property
    def template_path(self):
        """Path to available template files"""
        return super(JekyllExporter, self).template_path + [
            os.path.join(os.path.dirname(__file__), "templates")
        ]

    @property
    def preprocessors(self):
        """Add JekyllPreprocessor to list of enabled preprocessors"""
        return super(JekyllExporter, self).preprocessors + [
            "jekyllnb.JekyllPreprocessor"
        ]

    @property
    def default_config(self):
        """Default configuration"""
        config = Config({"JekyllPreprocessor": {"enabled": True}})
        config.merge(super(JekyllExporter, self).default_config)
        return config

    def default_filters(self):
        """Default filters"""
        for pair in super(JekyllExporter, self).default_filters():
            yield pair

        image_dir = self.resources.get("image_dir", self.resources["output_files_dir"])

        # convert image path to one compatible with Jekyll
        yield (
            "jekyllpath",
            lambda path: "{{ site.baseurl }}/"
            + path2url(os.path.join(image_dir, os.path.basename(path))),
        )
