

#Netoyage

import pandas as pd
from nltk.corpus import stopwords
import langid 
from nltk.tokenize import word_tokenize
import re
import spacy
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import nltk

import matplotlib.pyplot as plt


"""
NETOYAGE ET PREPROCESSING
"""

#pas tous les emojis..
def remove_emoji(text):
      emoji_pattern = re.compile("["
                         u"\U0001F600-\U0001F64F"  # emoticons
                         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                         u"\U0001F680-\U0001F6FF"  # transport & map symbols
                         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                         u"\U00002702-\U000027B0"
                         u"\U000024C2-\U0001F251"
                         "]+", flags=re.UNICODE)
      return emoji_pattern.sub(r'', text)
  
    
def cleaning_df_from_file(filename):
    df = pd.read_csv(filename)
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    list_negation = ["n'","ne","ni","jamais","pas","sans","absence de","absence du","absence d'"]
    df['review_title'] = [df.title[i]+" "+ df.review[i] for i in range(df.shape[0]) ]
    df['review_title'] = df['review_title'].apply(lambda x:remove_emoji(x))
    #df['review_title'] = [review[:-3].lower().replace(".","") for review in df.review_title]
    df['review_title'] = df['review_title'].apply(lambda x:text_del_space(x))
    df['review_title'] = df['review_title'].apply(lambda x:text_noted_negation(x,list_negation,"__NEG__"))
    df['review_title'] = df['review_title'].apply(lambda x:lemmatize_without_strange_str(x))
    """
    df['review_tokens'] = [word_tokenize(review) for review in df.review_title]
    df['review_tokens'] = [ [token for token in review if token not in list_to_del] for review in df.review_tokens]
    """
    return df


def text_del_space(text):
    return text.replace('    ',' ').replace('    ',' ').replace('   ',' ').replace('  ',' ')


def text_noted_negation(text,list_negation,sign_negation):
    for negation in list_negation:
        neg = " "+ negation+" "
        noted_neg = neg + sign_negation + " "
        text= text.replace(neg,noted_neg)
    return text
        
        
def lemmatize_without_strange_str(review):  
    strange_str = ["l'","l’","d’","~",'"','"',"#","'","{","(","[","-","|","`","_","\\","@"
            ,")","]","}","*","!",":","/",";",".",",","?","&","’","..."]
    list_negation = ["n'","ne","ni","jamais","pas","sans","absence de","absence du","absence d'"]
    stopwords_fr = [ word for word in stopwords.words("french") if word not in list_negation ]
    list_to_del = stopwords_fr + strange_str    
    nlp = spacy.load('fr_core_news_sm')
    doc = nlp(review)
    lem_spacy_list = [token.lemma_ for token in doc if token.lemma_ not in list_to_del ]
    sentence_lem = ' '.join(lem_spacy_list)
    return sentence_lem

def create_csv_df_prep(df,filename):
    df = df.drop(['title','review'],axis=1)
    df.to_csv(filename, index = False, header=True,encoding='utf-8-sig')


if __name__ == "__main__":
    df = cleaning_df_from_file("all_reviews_S.csv")
    create_csv_df_prep(df,"all_reviews_S_prep.csv")


text = ' '.join(df.review_title)
wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()


