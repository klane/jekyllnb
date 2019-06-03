from nbconvert.preprocessors import Preprocessor


class JekyllPreprocessor(Preprocessor):
    def preprocess(self, nb, resources):
        name = resources['metadata']['name']
        metadata = {
            'layout': 'page',
            'title': name,
            'permalink': '/' + name
        }
        metadata.update(nb.metadata.get('jekyll', {}))
        resources['metadata']['jekyll'] = metadata

        return nb, resources
