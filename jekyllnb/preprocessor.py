from nbconvert.preprocessors import Preprocessor


class JekyllPreprocessor(Preprocessor):
    def preprocess(self, nb, resources):
        metadata = nb.metadata.get('jekyll', {})
        resources['metadata']['layout'] = metadata.get('layout', 'page')
        resources['metadata']['title'] = metadata.get('title', None)
        resources['metadata']['permalink'] = metadata.get('permalink', None)

        return super(JekyllPreprocessor, self).preprocess(nb, resources)

    def preprocess_cell(self, cell, resources, cell_index):
        return cell, resources
