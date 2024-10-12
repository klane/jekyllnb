import os
from typing import Any, Callable, ClassVar, Literal, Optional

from nbconvert.exporters import MarkdownExporter
from nbconvert.filters.strings import path2url
from traitlets import default
from traitlets.config import Config


class JekyllExporter(MarkdownExporter):
    """Exporter to write Markdown with Jekyll metadata."""

    # path to available template files
    extra_template_basedirs: ClassVar[list[str]] = [
        os.path.join(os.path.dirname(__file__), "templates")
    ]

    # enabled preprocessors
    preprocessors: ClassVar[list[str]] = ["jekyllnb.JekyllPreprocessor"]

    # placeholder to store notebook resources
    resources: ClassVar[dict[str, Any]] = {}

    def from_filename(
        self, filename: str, resources: Optional[dict[str, Any]] = None, **kwargs
    ) -> tuple[str, dict[str, Any]]:
        """Convert notebook from a file.

        Args:
            filename (str): Full filename of the notebook to convert.
            resources (dict): Additional resources used by preprocessors and filters.
            kwargs: Additional arguments to pass to the exporter.

        Returns:
            NotebookNode: Converted notebook.
            dict: Resources dictionary.

        """
        if resources:
            self.resources.update(resources)

        return super().from_filename(filename, resources=resources, **kwargs)

    @default("template_name")
    def _template_name_default(self) -> Literal["jekyll"]:
        """Specify default template name."""
        return "jekyll"

    @property
    def default_config(self) -> Config:
        """Specify default configuration."""
        config = Config({"JekyllPreprocessor": {"enabled": True}})
        config.merge(super().default_config)
        return config

    def default_filters(self) -> list[tuple[str, Callable]]:
        """Specify default filters."""
        site_dir = self.resources.get("site_dir")

        # convert image path to one compatible with Jekyll
        return [
            *super().default_filters(),
            (
                "jekyllpath",
                lambda path: "{{ site.baseurl }}/"
                + path2url(os.path.relpath(path, site_dir)),
            ),
        ]
