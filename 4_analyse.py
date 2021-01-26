# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 21:35:32 2020

@author: Naomi
"""



from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from PIL import Image
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

def split_df_pos_neg(df):
    df_neg = df[df['rate']<3]
    df_pos = df[df['rate']>3]
    return df_pos, df_neg

    

def best_features(review,nb_features,ngram_range1,ngram_range2):
    my_stop_words = stopwords.words('french') + ['très']
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
    return df_mot_sorted


def display_best_features(df_mot_sorted):
    plt.figure(figsize=(30,7))
    plt.scatter(df_mot_sorted.mot,df_mot_sorted.occurence)
    ax = df_mot_sorted.plot.bar(x='mot', y='occurence', rot=0,width=0.8)
    


def words_occur_to_wordcloud_to_file(hotel_id,best_feature_by_hotel_dict,display,save):        
    mask_bas = np.array(Image.open('images/bas.PNG'))
    mask_haut = np.array(Image.open('images/haut.PNG'))
    best_features_neg = best_feature_by_hotel_dict[hotel_id]['neg']
    best_features_pos = best_feature_by_hotel_dict[hotel_id]['pos']
    #word_cloud_dict= { (best_features_neg.iloc[i].mot,best_features_neg.iloc[i].occurence) for i in range(best_features_neg.shape[0]) }
    word_cloud_dict_pos = { best_features_pos.iloc[i].mot:best_features_pos.iloc[i].occurence for i in range(best_features_pos.shape[0]) }  
    word_cloud_dict_neg = { best_features_neg.iloc[i].mot:best_features_neg.iloc[i].occurence for i in range(best_features_neg.shape[0]) }  
   
    wordcloud_pos = WordCloud( background_color="white", mask=mask_haut,width=mask_haut.shape[1],height=mask_haut.shape[0],contour_width=10, contour_color='green').generate_from_frequencies(frequencies=word_cloud_dict_pos)
    wordcloud_neg = WordCloud( background_color="white", mask=mask_bas,width=mask_bas.shape[1],height=mask_bas.shape[0],contour_width=10, contour_color='red').generate_from_frequencies(frequencies=word_cloud_dict_neg)
   
    for wordcloud in [wordcloud_pos, wordcloud_neg]:
        if display == True:
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()
        
    if save == True:
        wordcloud_pos.to_file("app/static/wordclouds/pos"+str(hotel_id)+".png")
        wordcloud_neg.to_file("app/static/wordclouds/neg"+str(hotel_id)+".png")



if __name__ == "__main__":
    reviews = pd.read_csv("all_reviews_S_prep.csv")
    reviews = reviews.drop_duplicates()
    hotels = pd.read_csv("all_hotel_url.csv")
    
    best_feature_by_hotel_dict = {}
    for no, hotel in enumerate(hotels.hotel):
        print(no)
        try:
            df = reviews[reviews['hotel_id']==no]
            df_pos = split_df_pos_neg(df)[0]
            df_neg = split_df_pos_neg(df)[1]
            best_features_pos = best_features(df_pos.review_title,100,2,4)
            try:
                best_features_neg = best_features(df_neg.review_title,50,3,3)
            except ValueError:
                df_mot = pd.DataFrame({'mot':[], 'occurence':[]})
                best_features_neg = df_mot
                
            #display_best_features(best_features)
            best_feature_un_hotel_dict = {'pos':best_features_pos,'neg':best_features_neg,'name_hotel':hotel,'id_hotel':no}
            best_feature_by_hotel_dict[no] = best_feature_un_hotel_dict
            best_feature_by_hotel_dict[hotel] = best_feature_un_hotel_dict
            
            
            words_occur_to_wordcloud_to_file(no,best_feature_by_hotel_dict,True,True)
        except ValueError:
            print('pas de reviews pour cet hotel')
            
            

words_to_keep = ["petit déjeuner","salle bain","buffet","famille"]
     

  
