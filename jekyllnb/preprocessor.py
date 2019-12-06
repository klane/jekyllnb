from nbconvert.preprocessors import Preprocessor


class JekyllPreprocessor(Preprocessor):
    def preprocess(self, nb, resources):  # skipcq: PYL-R0201
        name = resources["metadata"]["name"]
        metadata = {"layout": "page", "title": name, "permalink": "/" + name}
        metadata.update(nb.metadata.get("jekyll", {}))
        resources["metadata"]["jekyll"] = metadata

        return nb, resources
