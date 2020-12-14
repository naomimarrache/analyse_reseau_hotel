# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 20:30:05 2020

@author: salomelamartinie
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
from selenium.webdriver.common.keys import Keys



# function to check if the button is presnent on the page, to avoid miss-click problem
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def fill_date_by_default(driver):
    driver.find_element_by_css_selector('.start').click()
    driver.find_element_by_css_selector('.end').click()
    driver.find_element_by_css_selector('.XKdpCeJ3 > button:nth-child(1)').click()
    
   
    
def srcaping_url_hotel(driver,url_list,name_list):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    time.sleep(10)
    hotel_selector=soup.find_all('div', attrs={'class' : 'listing_title'})
    for hotel in hotel_selector:
        url = prefix_url_hotel + hotel.find('a')['href']
        name = hotel.find('a').text.strip()
        url_list.append(url)
        name_list.append(name)
        
        
def url_get(page_link):
    # create a new Firefox session
    driver = webdriver.Firefox()
    driver.get(page_link)
    return driver
    
def create_csv_url_hotel(filename,url_list,name_list):
    df = pd.DataFrame({'url':url_list,'hotel':name_list})
    df.to_csv (filename, index = False, header=True,encoding='utf-8-sig')


def zoom_out(driver,nb):
    for i in range(nb):
        driver.find_element_by_tag_name('html').send_keys(Keys.CONTROL, '-')
        
if __name__ == '__main__':
    page_link="https://www.tripadvisor.fr/Hotels-g298470-Saint_Gilles_Les_Bains_Arrondissement_of_Saint_Paul-Hotels.html"
    driver = url_get(page_link)
    #driver.maximize_window()
    time.sleep(10)
    fill_date_by_default(driver)
    prefix_url_hotel="https://www.tripadvisor.fr"
    url_list=[]
    name_list=[]
    while True :
        srcaping_url_hotel(driver, url_list, name_list)
        break
    # close the driver
    driver.close()
    create_csv_url_hotel('all_hotel_url.csv',url_list,name_list)




