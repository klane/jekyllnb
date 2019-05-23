from nbconvert.preprocessors import Preprocessor


class JekyllPreprocessor(Preprocessor):
    def preprocess(self, nb, resources):
        name = resources['metadata']['name']
        resources['metadata']['jekyll'] = {'layout': 'page',
                                           'title': name,
                                           'permalink': '/' + name
                                           }
        metadata = nb.metadata.get('jekyll', {})

        for key in metadata:
            resources['metadata']['jekyll'][key] = metadata[key]

        return nb, resources
