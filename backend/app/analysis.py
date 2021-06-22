import pandas as pd
import numpy as np
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.test.utils import datapath
from sqlalchemy import create_engine
import scispacy
import spacy
from pprint import pprint
import pyLDAvis
import pyLDAvis.gensim_models
from wordcloud import WordCloud
from pathlib import Path
import nltk
import os
from background_task import background
from django.conf import settings
import os

NUM_TOPICS = 25

# lda_model path
MODEL_PATH = "/app/app/lda_model/"
LDA_MODEL_PATH = MODEL_PATH + "lda_model"
WORD_DICT_PATH = MODEL_PATH + "word_dictionart"

id2word = corpora.Dictionary.load_from_text(WORD_DICT_PATH)
lda_model = gensim.models.ldamodel.LdaModel.load(LDA_MODEL_PATH)

# nltk stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['background', 'methods', 'introduction', 'conclusions', 'results', 
                'purpose', 'materials', 'discussions','methodology', 'abstract', 'section', 'text'])

nlp = spacy.load('en_core_sci_sm', disable=['parser', 'ner'])

@background(schedule=5)
def tokenize():
    postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(
            username=os.environ.get('RDS_DATABASE_USER'),
            password=os.environ.get('RDS_DATABASE_PASSWORD'),
            ipaddress=os.environ.get('RDS_DATABASE_HOST'),
            port='5432',
            dbname=os.environ.get('RDS_DATABASE_NAME')))
        # Create the connection

    cnx = create_engine(postgres_str)
    data = pd.read_sql_query('''SELECT * FROM app_article''', con=cnx)
    print(len(data))
    print(str(data["Tokenized"]))

    for index, row in data.iterrows():
        if row['Title'].startswith("OrderedDict") or row['Abstract'].startswith("OrderedDict"):
            continue
        list_of_text = row.Title + " " + row.Abstract
        for item in row.Keywords:
            list_of_text = list_of_text + " " + item
        # print(list_of_text)
        list_of_words = list(gensim.utils.simple_preprocess(str(list_of_text), deacc=True))
        # print(list_of_words)
        cleaned_words = [word for word in simple_preprocess(str(list_of_words)) if word not in stop_words]
        row.Tokenized = cleaned_words
    
    print(data.head(5))

    data.to_sql('app_cleanarticle', con=cnx, if_exists='replace', index=False)


def lda_to_output_labels(lda_result, class_count):
    """ 
    This function returns the output vector of a given LDA result
    For class count of 10 for example, (3, 0.97) becomes [0, 0, 0, 0.97, 0, 0, 0, 0, 0, 0]
    """
    output = np.zeros(class_count)
    for res in lda_result:
        output[res[0]] = res[1]
    return output


def lemmatization(tokens, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):

    """https://spacy.io/api/annotation"""
    doc = nlp(" ".join(tokens))
    return [token.lemma_ for token in doc if token.pos_ in allowed_postags]

def analyze(sentence):
    # tokenize sentence
    tokenized_words = gensim.utils.simple_preprocess(str(sentence), deacc=True)

    # remove stop words
    clean_words = [word for word in simple_preprocess(str(tokenized_words)) if word not in stop_words]

    tokens = [word for word in clean_words if word in id2word.token2id.keys()]
    
    # lemmatize clean worlds
    data_lemmatized = lemmatization(tokens, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
    print("tokens:")
    print(data_lemmatized)
    
    corpus = id2word.doc2bow(data_lemmatized)
    lda_output = lda_to_output_labels(lda_model[corpus][0], NUM_TOPICS)
    class_number = np.argmax(lda_output)
    print("class number" + str(class_number))
    return class_number
