from splinter import Browser
from bs4 import BeautifulSoup as bs
import os
import pandas as pd
import requests


def init_browser():
  executable_path = {'executable_path': 'chromedriver.exe'}
  browser = Browser('chrome', **executable_path, headless=False)
  
def scrape():
    browser = init_browser()
    mars_data = {}

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(2)
    
    html = browser.html
    soup = bs(html,"html.parser")
    
    news_title = soup.find("div",class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p
    
    image_url = ('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    response = requests.get(image_url)
    soup = bs(response.text, 'html.parser')

    images = soup.find_all('a', class_="fancybox")
    for image in images:
        featured_image_url = image['data-fancybox-href']

    mars_data['featured_image_url'] = featured_image_url
    
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    
    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    mars_weather = soup.find(class_="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-5f2r5o r-1mi0q7o").text
    mars_data['mars_weather'] = mars_weather
    
    facts_url = "https://space-facts.com/mars/"
    table = pd.read_html(facts_url)
    
    mars_facts = table[0]
    mars_facts.columns = ["Parameter", "Values"]
    mars_facts.set_index(["Parameter"])
    
    mars_facts_html = mars_facts.to_html()
    mars_facts_html = mars_facts_html.replace("\n", "")
    mars_data['mars_facts_html'] = mars_facts_html
    
    hemisphere_image_urls = []
    
    cerberus_url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced')

    response = requests.get(cerberus_url)
    soup = bs(response.text, 'html.parser')

    cerberus_img = soup.find_all('div', class_="wide-image-wrapper")
    for img in cerberus_img:
        pic = img.find('li')
        img_url = pic.find('a')['href']
    title = soup.find('h2', class_='title').text
    cerberus = {"title": title, "img_url": img_url}
    hemisphere_image_urls.append(cerberus)
    
    schiaparelli_url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced')

    response = requests.get(schiaparelli_url)
    soup = bs(response.text, 'html.parser')

    shiaparelli_img = soup.find_all('div', class_="wide-image-wrapper")
    for img in shiaparelli_img:
        pic = img.find('li')
        img_url = pic.find('a')['href']
    title = soup.find('h2', class_='title').text
    shiaparelli = {"title": title, "img_url": img_url}
    hemisphere_image_urls.append(shiaparelli)
    
    syrtis_major_url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced')

    response = requests.get(syrtis_major_url)
    soup = bs(response.text, 'html.parser')

    syrtris_img = soup.find_all('div', class_="wide-image-wrapper")
    for img in syrtris_img:
        pic = img.find('li')
        img_url = pic.find('a')['href']
    title = soup.find('h2', class_='title').text
    syrtris = {"title": title, "img_url": img_url}
    hemisphere_image_urls.append(syrtris)
    
    valles_marineris_url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced')

    response = requests.get(valles_marineris_url)
    soup = bs(response.text, 'html.parser')

    valles_marineris_img = soup.find_all('div', class_="wide-image-wrapper")
    for img in valles_marineris_img:
        pic = img.find('li')
        img_url = pic.find('a')['href']
    title = soup.find('h2', class_='title').text
    valles_marineris = {"title": title, "img_url": img_url}
    hemisphere_image_urls.append(valles_marineris)
    
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls
    
    return mars_data
