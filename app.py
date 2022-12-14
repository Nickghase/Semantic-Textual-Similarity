
import numpy as np
import pandas as pd
import re
import string
import nltk 
from nltk.stem import WordNetLemmatizer 
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline
import spacy
from collections import Counter
import pickle
import streamlit as st
nlp = spacy.load('en_core_web_sm')

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')



st.header('SEMANTIC TEXTUAL SIMILARITY')
text1 = pickle.load(open('text1.pkl','rb'))
text2 = pickle.load(open('text2.pkl','rb'))

selected_text1 = st.selectbox(
    "select a text from the dropdown",
    text1)

selected_text2 = st.selectbox(
    "select a text from the dropdown",
    text2)

copydata = pd.DataFrame([[selected_text1,selected_text2]],columns = ["text1","text2"])

def remove_punc(copydata):
  pattern = r'[' + string.punctuation + ']'
  copydata['text1']=copydata['text1'].map(lambda m:re.sub(pattern," ",m))
  copydata['text2']=copydata['text2'].map(lambda m:re.sub(pattern," ",m))
  return copydata


def lower(copydata):
  copydata['text1']=copydata['text1'].map(lambda m:m.lower())
  copydata['text2']=copydata['text2'].map(lambda m:m.lower())
  return copydata


def tokenization(text):
    tokens = re.split(' ',text)
    return tokens

def token(copydata):
  copydata['text1']= copydata['text1'].apply(lambda x: tokenization(x))
  copydata['text2']= copydata['text2'].apply(lambda x: tokenization(x))
  return copydata


sw=nltk.corpus.stopwords.words('english')

def remove_SW(copydata):
   copydata['text1']=copydata['text1'].apply(lambda x: [item for item in x if item not in sw])
   copydata['text2']=copydata['text2'].apply(lambda x: [item for item in x if item not in sw])
   return copydata


def remove_digits(copydata):
  copydata['text1']=copydata['text1'].apply(lambda x: [item for item in x if not item.isdigit()])
  copydata['text2']=copydata['text2'].apply(lambda x: [item for item in x if not item.isdigit()])
  return copydata


lemmatizer = WordNetLemmatizer()

def lemmatize(copydata):
  copydata['text1']=copydata['text1'].apply(lambda x: [lemmatizer.lemmatize(item) for item in x])
  copydata['text2']=copydata['text2'].apply(lambda x: [lemmatizer.lemmatize(item) for item in x])
  return copydata


def remove_empty_tokens(copydata):
  copydata['text1']=copydata['text1'].apply(lambda x: [item for item in x if item !=''])
  copydata['text2']=copydata['text2'].apply(lambda x: [item for item in x if item !=''])
  return copydata


def remove_single_letters(copydata):
  copydata['text1']=copydata['text1'].apply(lambda x: [item for item in x if len(item) > 1])
  copydata['text2']=copydata['text2'].apply(lambda x: [item for item in x if len(item) > 1])
  return copydata


def detoken(copydata):
  copydata['text1']= copydata['text1'].apply(lambda x: TreebankWordDetokenizer().detokenize(x))
  copydata['text2']= copydata['text2'].apply(lambda x: TreebankWordDetokenizer().detokenize(x))
  return copydata

def replace_spaces(x,space,second):
  result = x.replace(space, second)
  return result
def remove_space(copydata):
  copydata['text1']= copydata['text1'].apply(lambda x: replace_spaces(x,'  ',' '))
  copydata['text2']= copydata['text2'].apply(lambda x: replace_spaces(x,'  ',' '))
  return copydata

def count_vcr():
  for i in range(len(copydata)):
    doc1=copydata['text1'][i]
    doc2=copydata['text2'][i]
    docs=(doc1,doc2)
    matrix = CountVectorizer().fit_transform(docs)
    cosine_sim = cosine_similarity(matrix[0], matrix[1])
    similarity.append(cosine_sim)
  return similarity

copydata=copydata.pipe(remove_punc).pipe(token).pipe(remove_SW).pipe(remove_digits).pipe(lemmatize).pipe(remove_empty_tokens).pipe(remove_single_letters)

similarity=[]
def get_similarity():
  bow_converter = CountVectorizer()
  copydata.pipe(detoken).pipe(remove_space)

  similarity=count_vcr()
  data_cvr=copydata.copy()
  data_cvr['Similarity']=similarity
  return data_cvr


if st.button('Show Similarity'):
    data_cvr = get_similarity()
    st.text(data_cvr.iloc[0,0])
    st.text(data_cvr.iloc[0,1])
    st.text(data_cvr.iloc[0,2])
