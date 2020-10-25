import os
from typing import Any, Dict, List

from nbconvert.exporters import MarkdownExporter
from nbconvert.filters.strings import path2url
from traitlets import default
from traitlets.config import Config


class JekyllExporter(MarkdownExporter):
    """Exporter to write Markdown with Jekyll metadata"""

    # path to available template files
    extra_template_basedirs: List[str] = [
        os.path.join(os.path.dirname(__file__), "templates")
    ]

    # enabled preprocessors
    preprocessors: List[str] = ["jekyllnb.JekyllPreprocessor"]

    # placeholder to store notebook resources
    resources: Dict[str, Any] = {}

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
        return super().from_filename(filename, resources=resources, **kwargs)

    @default("template_name")
    def _template_name_default(self):  # skipcq: PYL-R0201
        """Default template name"""
        return "jekyll"

    @property
    def default_config(self):
        """Default configuration"""
        config = Config({"JekyllPreprocessor": {"enabled": True}})
        config.merge(super().default_config)
        return config

    def default_filters(self):
        """Default filters"""
        yield from super().default_filters()

        site_dir = self.resources.get("site_dir")

        # convert image path to one compatible with Jekyll
        yield (
            "jekyllpath",
            lambda path: "{{ site.baseurl }}/"
            + path2url(os.path.relpath(path, site_dir)),
        )
