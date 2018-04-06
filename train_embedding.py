from gensim import models

class Corpus(object):

    def __init__(self, papers):
        self.papers = papers  # collection of papers


    def __iter__(self):
        # each yield should return one document. For now, lets do titles
        cursor = self.papers.find({'title': {'$exists': True}})
        for paper_with_title in cursor:
            # [0] because ADS gives title as a list...
            yield paper_with_title['title'][0].split()  # Want list of list of words.


def clean_text(documents):
    # basic cleaning for the input docs to improve performance
    # this can be added to the corpus yielder
    # copied from https://radimrehurek.com/gensim/tut1.html
    # Not yet done!
    raise NotImplementedError

    # remove common words and tokenize
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in documents]

    # remove words that appear only once
    from collections import defaultdict
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]

    # TODO remove latex?

    return texts


def get_vectors(corpus, save_loc=None):
    # see https://rare-technologies.com/word2vec-tutorial/
    # see https://radimrehurek.com/gensim/models/word2vec.html
    # all parameters: https://radimrehurek.com/gensim/models/word2vec.html#gensim.models.word2vec.Word2Vec
    model = models.Word2Vec(corpus, size=100, window=5, min_count=0, workers=4)  # corpus is iterable
    if save_loc is not None:
        model.save(save_loc)
    return model