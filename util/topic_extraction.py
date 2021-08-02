from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import pymorphy2
from stop_words import get_stop_words

morph = pymorphy2.MorphAnalyzer()
stop_words = get_stop_words('russian')


def lemmatize(text):
    """
    Lemmatize input words
    :param text: raw text, string format
    :return: list of normalized words
    """
    words = text.split()
    res = list()
    for word in words:
        p = morph.parse(word)[0]
        res.append(p.normal_form)
    return res


def clean_text(lemmatized_text):
    """
    Remove digits, punctuation.
    :param lemmatized_text: list of input words
    :return: Clean list of words
    """
    punct_marks = '''!()-[]{};?@#$%:'"“”«»–\,./^&amp;*_'''
    new_words = [word for word in lemmatized_text if word not in punct_marks and not word.isdigit()]
    return new_words


def preprocessing(text):
    """
    Clean text and lemmatize words
    :param text: raw text, string format
    :return:
    """
    lemmatized_text = lemmatize(text)
    cleaned_text = clean_text(lemmatized_text)
    filtered_sentence = [w for w in cleaned_text if w not in stop_words]
    preprocessed_text = " ".join(filtered_sentence)
    return preprocessed_text


def get_topics(data, topics=5, n_keywords=5):
    """
    Take raw corpus and train topic model
    :param data: list of texts, corpus
    :param topics:
    :param n_keywords:
    :return:
    """
    preprocessed_corpus = [preprocessing(text) for text in data]
    vectorizer = CountVectorizer()
    vec_corpus = vectorizer.fit_transform(preprocessed_corpus).toarray()

    lda = LatentDirichletAllocation(n_components=topics, random_state=0)
    lda.fit(vec_corpus)

    doc_topic_matrix = lda.transform(vec_corpus)
    topic_tokens_matrix = lda.components_

    topics_pred = doc_topic_matrix.argmax(axis=1)

    topic_keywords = dict()
    for i in range(topics):
        topic_keywords[i] = [x[0] for x in sorted(list(zip(vectorizer.get_feature_names(), topic_tokens_matrix[i])),
                                                  key=lambda x: x[1],
                                                  reverse=True)[:n_keywords]]

    return topic_keywords, topics_pred, vectorizer, lda


def get_topics_pretrained(data, lda, vectorizer):
    preprocessed_corpus = [preprocessing(text) for text in data]
    vec_data = vectorizer.transform(preprocessed_corpus).toarray()
    doc_topic_matrix = lda.transform(vec_data)
    topics_pred = doc_topic_matrix.argmax(axis=1)
    return topics_pred


def set_topics_to_data(input_df, topics_pred, topics):
    """
    Add new topic column to dataframe
    :param input_df: dataframe with text to set topics to
    :param topics_pred: list of topic indexes, length equal to data
    :param topics: dict index to topic name
    :return: dataframe with topic column
    """
    data = input_df.copy()
    data['topic'] = topics_pred
    for i in topics:
        data.loc[data['topic'] == i, 'topic'] = topics[i]
    return data
