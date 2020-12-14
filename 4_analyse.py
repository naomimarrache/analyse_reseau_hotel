# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 21:35:32 2020

@author: Naomi
"""

from nltk.corpus import stopwords
import matplotlib.pyplot as plt

import pandas as pd



from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

"""
corpus = df.review_title
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)
print(vectorizer.get_feature_names())

feature_names = vectorizer.get_feature_names()
dense = X.todense()
denselist = dense.tolist()
dataframe = pd.DataFrame(denselist, columns=feature_names)
"""


"""
tfIdfVectorizer=TfidfVectorizer()
tfIdf = tfIdfVectorizer.fit_transform(df.review)
df = pd.DataFrame(tfIdf[0].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
df = df.sort_values('TF-IDF', ascending=True)
print (df.head(50))
"""

def split_df_pos_neg(df):
    df_neg = df[df['rate']<3]
    df_pos = df[df['rate']>3]
    return df_pos, df_neg

    

def hist_mots_importants(review,nb_features,ngram_range1,ngram_range2):
    my_stop_words = stopwords.words('french')
    vect = CountVectorizer(stop_words=my_stop_words,max_features=nb_features,ngram_range=(ngram_range1, ngram_range2))
    vect.fit(review)
    X = vect.transform(review)
    # Transform to an array
    my_array = X.toarray()
    # Transform back to a dataframe, assign column names
    X_df = pd.DataFrame(my_array, columns=vect.get_feature_names())
    occurence = []
    mots = []
    for mot in X_df.columns:
        occurence.append(X_df[mot].sum())
        mots.append(mot)
    df_mot = pd.DataFrame({'mot':mots, 'occurence':occurence})
    df_mot_sorted = df_mot.sort_values('occurence',ascending=False)
    plt.figure(figsize=(30,7))
    plt.scatter(df_mot_sorted.mot,df_mot_sorted.occurence)
    #ax = df_mot_sorted.plot.bar(x='mot', y='occurence', rot=0,width=0.8)
    return df_mot_sorted


if __name__ == "__main__":
    df = pd.read_csv("all_reviews.csv")
    df_pos = split_df_pos_neg(df)[0]
    df_neg = split_df_pos_neg(df)[1]
    vect = hist_mots_importants(df_neg.review,20,3,4)
    
"""
faire beaucoup de semantique pour renvoyer les features les
plus pertinents
ex : hotel très à supprimer
remplacer "pas très" par "pas" --> hotel pas beau = hotel pas NEG beau
"""
