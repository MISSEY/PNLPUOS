import xml.etree.ElementTree as ET
import pandas as pd
#from somajo.tokenizer import Tokenizer # A tokenizer and sentence splitter for German and English web and social media texts
from nltk import tokenize
from nltk import TweetTokenizer

def read_corpus(filename, corpus, n):
    """
    Read corpus and return preprocessed documents and sentiment list
    :param filename: Filename of corpus
    :param corpus: Type of corpus
    :param n: Number of documents
    :return: Documents list, sentiments list
    """
    docs = list()
    sentiments = list()
    if corpus == 'germeval':
        root = ET.parse(filename).getroot()
        for doc in root.iter('Document'):
            for text in doc.iter('text'):
                docs.append(text.text)
            for sentiment in doc.iter('sentiment'):
                sentiments.append(sentiment.text)

    elif corpus == 'pnlp':
        data = pd.read_csv(filename, sep=";")

        Question_1 = data[data['Question Text'] == 'Please tell us what is working well.']
        Question_2 = data[data['Question Text'] == 'Please tell us what needs to be improved.']

    elif corpus == 'twitter':
        data = pd.read_csv(filename)
        docs = data['Text'].tolist()
        sentiments = data['Sentiment'].tolist()

    elif corpus == 'imdb':
        data = pd.read_csv(filename)
        print(data.head())
        docs = data['review'].tolist()
        sentiments = data['sentiment'].tolist()

    elif corpus == 'twitter140':
        data = pd.read_csv(filename, encoding="ISO-8859-1",
                           names=["target", "weird number", "date", "query", "user", "text"])
        data = data.sample(frac=1) # ordered dataset -> shuffle beforehand
        docs = data['text'].tolist()
        sentiments = data['target'].tolist()

    elif corpus == 'amazon':
        data = pd.read_csv(filename, encoding='utf-8', sep='\t', header=None)
        data = data.sample(frac=1)
        docs = data[0].tolist()
        sentiments = data[1].tolist()

    elif corpus == 'tomatoes':
        data = pd.read_csv(filename, encoding='ISO-8859-1')
        data = data.sample(frac=1)
        docs = data['Text'].tolist()
        sentiments = data['Rating'].tolist()

    elif corpus == 'german':
        data = pd.read_csv(filename)
        print(data.head())
        docs = data['Text'].tolist()
        sentiments = data['Sentiment'].tolist()

        print("text :", docs[:5])
        print("senti :", sentiments[:5])

    return preprocess(docs, sentiments, n)


def preprocess(docs, sentiments, n):
    """
    Filters <br> tags, URLs and twitter handles
    :param docs: Document list
    :param sentiments: Sentiment list
    :param n: Number of documents
    :return: Processed corpus
    """
    processed_tweets = list()
    processed_sentiments = list()
    tok = TweetTokenizer()


    for i, doc in enumerate(docs):
        if i > n:
            return processed_tweets, processed_sentiments

        if not pd.isna(sentiments[i]):
            #print(doc)
            #print(type(doc))
            #tokens = list(filter(lambda a: not a.startswith('<br' or '@' or 'http'), tok.tokenize(doc))) #tokenize and filter out <br>
            tokens = tok.tokenize(doc)
            tweet_new = ' '.join(tokens)
            processed_tweets.append(tweet_new)
            processed_sentiments.append(str(sentiments[i]))




    return processed_tweets, processed_sentiments
