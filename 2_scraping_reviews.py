# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 23:36:59 2020

@author: salomelamartinie
"""

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
# The ActionChain class to avoid the "Element is not clickable" issue
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time


def check_exists_by_css_selector(css):
    try:
        driver.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False
    return True

def scraping_1_page(driver,review_text_list,title_list,rate_list,hotel_list,hotel_id):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    review_selector = soup.find_all('div',class_="_2wrUUKlw _3hFEdNs8")
    for review in review_selector:
        title = review.find('div',class_="glasR4aX").text
        review_text = review.find('div',class_="cPQsENeY").text
        rate = int(review.find('div',class_="nf9vGX55").find('span')['class'][1].split('bubble_')[1])/10
        title_list.append(title)
        review_text_list.append(review_text)
        rate_list.append(rate)
        hotel_list.append(hotel_id)
    time.sleep(0.5)
    
def go_to_the_next_page(driver):
    try : 
        driver.find_element_by_css_selector('a.ui_button:nth-child(2)').click()
    except(StaleElementReferenceException, ElementClickInterceptedException, ElementNotInteractableException):
        # wait for the "next" button to be Clickable 
        print("in the Except : ")
        wait = WebDriverWait(driver, 60)
        wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, 'element_to_be_clickable')))
        # Click the "next" button as soon as it will be Clickable   
        ActionChains(driver).move_to_element(driver.find_element_by_css_selector('element_to_be_clickable')).click().perform()

def create_csv_with_reviews(filename,review_text_list,title_list,rate_list,hotel_list):
    df = pd.DataFrame({"hotel_id":hotel_list,"rate":rate_list,"title":title_list,"review":review_text_list})    
    df.to_csv(filename, index = False, header=True,encoding='utf-8-sig')

def scraping_reviews_1_hotel(driver,review_text_list,title_list,rate_list,hotel_list,hotel_id,url):
    page_link = url
    #page_link="https://www.tripadvisor.fr/Hotel_Review-g298470-d1473791-Reviews-LUX_Saint_Gilles-Saint_Gilles_Les_Bains_Arrondissement_of_Saint_Paul.html"
    # create a new Firefox session
    driver.get(page_link)
    #zoom out 
    driver.execute_script('document.body.style.MozTransform = "scale(0.5)";')
    time.sleep(5)
    nb_click_next = 0
    while True:
        while nb_click_next < 20:
            scraping_1_page(driver,review_text_list,title_list,rate_list,hotel_list,hotel_id)
            if (check_exists_by_css_selector('a.ui_button:nth-child(2)')):      
                go_to_the_next_page(driver)
                nb_click_next = nb_click_next + 1
            else:
                break
        

    
if __name__ == "__main__":
    try:
        driver = webdriver.Firefox()
        df = pd.read_csv('all_hotel_url.csv')
        review_text_list, title_list, rate_list, hotel_list = [], [], [], []
        for hotel_id, url in enumerate(df.url):
            scraping_reviews_1_hotel(driver,review_text_list,title_list,rate_list,hotel_list,hotel_id,url)
        driver.close()
        create_csv_with_reviews("all_reviews.csv",review_text_list,title_list,rate_list,hotel_list)
    except:
        print("Interruption manuelle ou autre problème rencontré..")
        create_csv_with_reviews("all_reviews_test.csv",review_text_list,title_list,rate_list,hotel_list)

            

