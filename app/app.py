# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
import pandas 

@app.route('/')
def home():
    name = "nao"
    
    hotels = pandas.read_csv('all_hotel_url.csv')
    id_hotel_list = []
    name_hotel_list = []
    for no, hotel in enumerate(hotels.hotel):
        id_hotel_list.append(no)
        name_hotel_list.append(hotel)
    
    
    return render_template('home.html', name=name, id_hotel_list=id_hotel_list,name_hotel_list=name_hotel_list)

"""
@app.route('/test',methods = ['POST'])
def test():
    result = request.form
    r = result['review']
    #prediction = "positive"
    prediction = pred(r)
    pb_detect = None
    if prediction == "oups":
      pb_detect = "exist"
    return render_template('test.html', review=r, prediction=prediction, langue=detect(r), pb_detect=pb_detect)

@app.route('/analyse_2',methods = ['POST'])
def analyse_2():
    result = request.form
    r = result['review']
    l = result['language']
    #prediction = "positive"
    if l == "English":
      prediction = pred_en(r)
    elif l == "French":
      prediction = pred_fr(r)
    return render_template('test.html', review=r, prediction=prediction, langue=l)

def pred_fr(r):
    #ici mettre le code du bon modele de ml en franÃ§ais
    return "negative"

def pred_en(r):
    #ici mettre le code du bon modele de ml en anglais
    return "negative"



def pred(r):
    name = None
    if detect(r) == "fr":
      return pred_fr(r)
    elif detect(r) == "en":
      return pred_en(r)
    else:
      #ni anglais ni francais detecte
      return "oups"
      #return 'DifficultÃ©s rencontrÃ©s pour dÃ©tÃ©cter la langue. Commentaire trop petit'

"""
if __name__ == '__main__':
        app.run(debug=True)