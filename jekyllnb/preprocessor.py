from typing import Any

from nbconvert.preprocessors import Preprocessor
from nbformat import NotebookNode


class JekyllPreprocessor(Preprocessor):
    """Preprocessor to add Jekyll metadata."""

    def preprocess(
        self, nb: NotebookNode, resources: dict[str, Any]
    ) -> tuple[NotebookNode, dict[str, Any]]:
        """Preprocess notebook.

        Add Jekyll metadata to notebook resources.

        Args:
            nb (NotebookNode): Notebook being converted.
            resources (dict): Additional resources used by preprocessors and filters.

        Returns:
            NotebookNode: Modified notebook.
            dict: Modified resources dictionary.

        """
        name = resources["metadata"]["name"]
        metadata = {"layout": "page", "title": name, "permalink": "/" + name}
        metadata.update(nb.metadata.get("jekyll", {}))
        resources["metadata"]["jekyll"] = metadata

        return nb, resources
