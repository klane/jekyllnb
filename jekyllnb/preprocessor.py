from nbconvert.preprocessors import Preprocessor


class JekyllPreprocessor(Preprocessor):
    """Preprocessor to add Jekyll metadata"""

    def preprocess(self, nb, resources):  # skipcq: PYL-R0201
        """Preprocess notebook

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
