#!/usr/bin/env python
# coding: utf-8

# In[18]:

#REFERENCE FROM SARIKHIN

#========CLEANING CODE TEXT-PRE-PROCESSING=========# 
"""
Note :
- wajib memakai python 2.7
- sudah terinstal lib sebagai berikut :
- pandas
- seaborn
- sklearn
- nltk(corpus, tokenize)
- pysastrawi
"""

# Import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import nltk 
import string
import re
# %matplotlib inline
# pd.set_option('display.max_colwidth', 100)

# Load dataset
def load_data():
    data = pd.read_excel('DatasetText021.xlsx')
    return data


kalimat_df = load_data()

#definisi dataframe
df = pd.DataFrame(kalimat_df[['No', 'Kalimat']])#ubah dataframe sesuai column kalian


#=========================================================================#

def remove(kalimat):
    #remove angka
    kalimat = re.sub('[0-9]+', '', kalimat)
    return kalimat
df['remove_angka'] = df['Kalimat'].apply(lambda x: remove(x))

#=========================================================================#

df.drop_duplicates(subset ="remove_angka", keep = 'first', inplace = True)

#=========================================================================#

nltk.download('stopwords')

#=========================================================================#

#import stopword
from nltk.corpus import stopwords 
stopwords_indonesia = stopwords.words('indonesian')
 
#import sastrawi
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
factory = StemmerFactory()
stemmer = factory.create_stemmer()

#tokenize
from nltk.tokenize import TweetTokenizer
 
# Happy Emoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])
 
# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])
 
# all emoticons (happy + sad)
emoticons = emoticons_happy.union(emoticons_sad)
 
def clean_kalimats(kalimat):
 
    # remove hyperlinks
    kalimat = re.sub(r'https?:\/\/.*[\r\n]*', '', kalimat)
    
    # remove hashtags
    # only removing the hash # sign from the word
    kalimat = re.sub(r'#', '', kalimat)
    
    #remove coma
    kalimat = re.sub(r',','',kalimat)
    
    #remove angka
    kalimat = re.sub('[0-9]+', '', kalimat)
 
    # tokenize tweets
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    kalimat_tokens = tokenizer.tokenize(kalimat)
 
    kalimats_clean = []    
    for word in kalimat_tokens:
        if (word not in stopwords_indonesia and # remove stopwords
              word not in emoticons and # remove emoticons
                word not in string.punctuation): # remove punctuation
            #tweets_clean.append(word)
            stem_word = stemmer.stem(word) # stemming word
            kalimats_clean.append(stem_word)
 
    return kalimats_clean
df['kalimat_clean'] = df['remove_angka'].apply(lambda x: clean_kalimats(x))

#=========================================================================#

#remove punct

def remove_punct(Kalimat):
    Kalimat  = " ".join([char for char in Kalimat if char not in string.punctuation])
    return Kalimat
df['kalimat_baru'] = df['kalimat_clean'].apply(lambda x: remove_punct(x))

 #=========================================================================#
  
df.sort_values("kalimat_baru", inplace = True)
df.drop(df.columns[[1,2,3]], axis = 1, inplace = True)
df.drop_duplicates(subset ="kalimat_baru", keep = 'first', inplace = True)
df.to_excel('outputPPDMfix.xlsx',encoding='utf8', index=False)
df
