import os
from typing import Any, Dict, Sequence

from nbconvert.nbconvertapp import NbConvertApp, nbconvert_aliases, nbconvert_flags
from traitlets import Bool, Unicode, default, observe
from traitlets.config import catch_config_error

from .__version__ import __version__

JEKYLLNB_ALIASES = {}  # type: Dict[str, str]
JEKYLLNB_ALIASES.update(nbconvert_aliases)
JEKYLLNB_ALIASES.update(
    {
        "site-dir": "JekyllNB.site_dir",
        "page-dir": "JekyllNB.page_dir",
        "image-dir": "NbConvertApp.output_files_dir",
    }
)

JEKYLLNB_FLAGS = {}  # type: Dict[str, Sequence[Any]]
JEKYLLNB_FLAGS.update(nbconvert_flags)
JEKYLLNB_FLAGS.update(
    {
        "no-auto-folder": (
            {"JekyllNB": {"auto_folder": False}},
            "Do not create image folder with notebook name at image-dir level.",
        )
    }
)


class JekyllNB(NbConvertApp):
    """Application to convert notebooks (``*.ipynb``) to Jekyll Markdown (``.md``)"""

    name = "jupyter-jekyllnb"
    description = "Convert Jupyter notebooks to Jekyll-ready Markdown"
    version = __version__

    aliases = JEKYLLNB_ALIASES
    flags = JEKYLLNB_FLAGS

    auto_folder = Bool(True).tag(config=True)
    site_dir = Unicode("").tag(config=True)
    page_dir = Unicode("").tag(config=True)

    @default("export_format")
    def _export_format_default(self):  # skipcq: PYL-R0201
        """Default export format"""
        return "jekyll"

    @observe("export_format")
    def _export_format_changed(self, change):
        """Ensure export format is jekyll"""
        default_format = self._export_format_default()

        if change["new"].lower() != default_format:
            raise ValueError(
                "Invalid export format {}, value must be {}".format(
                    change["new"], default_format
                )
            )

    @catch_config_error
    def initialize(self, argv=None):
        """Initialize application, notebooks, writer, and postprocessor"""
        super().initialize(argv)
        self.writer.build_directory = os.path.join(self.site_dir, self.page_dir)

        if self.auto_folder:
            self.output_files_dir = os.path.join(
                self.output_files_dir, "{notebook_name}"
            )

    def init_single_notebook_resources(self, notebook_filename):
        """Initialize resources

        Initializes the resources dictionary for a single notebook.

        Args:
            notebook_filename (str): Full filename of the notebook to convert.

        Returns:
            dict: Resources dictionary for a single notebook.

            Dictionary must include the following keys:
                - config_dir: location of the Jupyter config directory
                - unique_key: notebook name
                - output_files_dir: directory where output files should be saved
        """
        resources = super().init_single_notebook_resources(notebook_filename)
        resources["image_dir"] = resources["output_files_dir"]
        resources["output_files_dir"] = os.path.join(
            os.getcwd(), self.site_dir, resources["output_files_dir"]
        )

        return resources
