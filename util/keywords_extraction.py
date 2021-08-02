from sklearn.feature_extraction.text import TfidfVectorizer
from util.topic_extraction import preprocessing


def top_n_keywords(feature_names, v, n=10):
    """
    Find top n keywords for each text
    :param feature_names: list of TfIdf features
    :param v: text TfIdf vector
    :param n: number of keywords to extract
    :return: string with n top keywords
    """
    return "; ".join([x[1] for x in sorted(list(zip(v, feature_names)), reverse=True)[:n]])


def get_keywords(corpus, n=10):
    """
    Collect keywords for each text in corpus
    :param n: number of keywords to extract
    :param corpus: list of raw texts
    :return: list with top n keywords for each text in corpus
    """
    preprocessed_corpus = [preprocessing(text) for text in corpus]
    vectorizer = TfidfVectorizer()
    vec_data = vectorizer.fit_transform(preprocessed_corpus)
    feature_names = vectorizer.get_feature_names()
    all_text_keywords = [top_n_keywords(feature_names, v, n) for v in vec_data.toarray()]
    return all_text_keywords, vectorizer


def get_keywords_preprocessed(corpus, vectorizer, n=10):
    """
    Collect keywords for each text in corpus with pretrained TfIdf model
    :param n: number of keywords to extract
    :param vectorizer: pretrained TfIdf model
    :param corpus: list of raw texts
    :return: list with top n keywords for each text in corpus
    """
    preprocessed_corpus = [preprocessing(text) for text in corpus]
    vec_data = vectorizer.transform(preprocessed_corpus)
    feature_names = vectorizer.get_feature_names()
    all_text_keywords = [top_n_keywords(feature_names, v, n) for v in vec_data.toarray()]
    return all_text_keywords
