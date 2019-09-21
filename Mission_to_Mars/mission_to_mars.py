#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
from time import sleep


def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_p = mars_news(browser)

    mars = {
        "title" : news_title,
        "paragraph" : news_p,
        "image_URL" : jpl_image(browser),
        "weather" : mars_weather_tweet(browser),
        "facts" : mars_facts(),
        "hemispheres" : mars_hemis(browser)
    }

    browser.quit()

    return mars


# # NASA Mars News
def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    title_soup = BeautifulSoup(html, 'html.parser')

    news_title = title_soup.find("div", class_= "content_title").text
    news_p = title_soup.find("div", class_="article_teaser_body").text

    return news_title, news_p

# # JPL Mars Space Images - Featured Image
def jpl_image(browser):
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html=browser.html
    img_soup=BeautifulSoup(html, "html.parser")

    image=img_soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url


# # Mars Weather
def mars_weather_tweet(browser):
    # Scrape the URL of the page
    weather_url="https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    html = browser.html
    twitter_soup = BeautifulSoup(html, "html.parser")

    mars_weather = twitter_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    mars_weather_text = mars_weather.find('p', 'tweet-text').text

    return mars_weather_text


# # Mars Facts
def mars_facts():
    facts_tables = pd.read_html('http://space-facts.com/mars/')
    facts_table_df = facts_tables[1]
    facts_table_df.columns = ['Parameter','Value']

    return facts_table_df.to_html()


# # Mars Hemispheres
def mars_hemis(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemi_strings =[]
    links = soup.find_all('h3')

    for hemi in links:
        hemi_strings.append(hemi.text)


    hemisphere_image_urls = []

    for hemi in hemi_strings:
        hemi_dict = {}
        
        browser.click_link_by_partial_text(hemi)
        
        hemi_dict["img_url"] = browser.find_by_text('Sample')['href']
        
        hemi_dict["title"] = hemi
        
        hemisphere_image_urls.append(hemi_dict)
        
        pprint(hemisphere_image_urls)
        
        browser.back()
        
    return hemisphere_image_urls

