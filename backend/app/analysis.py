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

# lda_model path
LDA_MODEL_PATH = datapath(os.path.join(settings.BASE_DIR, "\\app\\lda_model\\lda_model"))

# nltk stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['background', 'methods', 'introduction', 'conclusions', 'results', 
                'purpose', 'materials', 'discussions','methodology', 'abstract', 'section', 'text'])

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


def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    nlp = spacy.load('en_core_sci_sm', disable=['parser', 'ner'])

    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

def analyze(sentences):
    lda_model = gensim.models.ldamodel.LdaModel.load(LDA_MODEL_PATH)