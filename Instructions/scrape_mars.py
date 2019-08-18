# import libraries
import pandas as pd
import pymongo
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser

# define a placeholder for saved variables
mars_dict = {}

# website scrape function
def scraping_func(url):
    # Path to chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Go to website
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    scrape_soup = bs(html, 'html.parser')

    # Close the browser after scraping
    browser.quit()
    
    #return scraped object
    return scrape_soup


def scrape():
    ### 1) NASA Mars News
    # * Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. 
    # Assign the text to variables that you can reference later.

    # Set Website URL to scrape
    url = 'https://mars.nasa.gov/news/'

    # Call scrape function and pass in url
    scrape_soup = scraping_func(url)

    # Get latest title
    news_title_find = scrape_soup.find('div', class_='content_title')

    # Get title from scrape
    news_title = news_title_find.get_text()

    # Get latest title's paragraph
    news_p_find = scrape_soup.find('div', class_='article_teaser_body')
    news_p = news_p_find.get_text()

    ### 2) JPL Mars Space Images - Featured Image
    #* Use splinter to navigate the site and find the image url for the current Featured Mars Image and 
    # assign the url string to a variable called `featured_image_url`.

    # Set Website URL to scrape
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars/'

    # Call scrape function and pass in url
    scrape_soup = scraping_func(url)

    # Get latest picture
    relative_image_path = scrape_soup.find_all('img')[3]["src"]
    featured_image_url = url + relative_image_path

    ### 3) Mars Weather
    #* Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and 
    # scrape the latest Mars weather tweet from the page. 
    #Save the tweet text for the weather report as a variable called `mars_weather`

    # Set Website URL to scrape
    url = 'https://twitter.com/marswxreport?lang=en'

    # Call scrape function and pass in url
    scrape_soup = scraping_func(url)

    # Get latest weather tweet
    mars_weather_find = scrape_soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    mars_weather = mars_weather_find.get_text()

    ### 4) Mars Facts
    #* Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and 
    #use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    #* Use Pandas to convert the data to a HTML table string.

    # Set Website URL to scrape
    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)

    mars_earth_comp_df = tables[0]
    mars_earth_comp_df.columns = ['Mars-Earth Comparison', 'Mars', 'Earth']
    mars_comparison = {}
    dict_temp = {}
    for i in range(len(mars_earth_comp_df)):
        for j in range(1):
            dict_temp = {mars_earth_comp_df.iloc[i][j]: mars_earth_comp_df.iloc[i][j+1]}
            mars_comparison.update(dict_temp)

    mars_planet_profile_df = tables[1]
    mars_planet_profile_df.columns = ['Mars Planet Profile', 'Measurement']
    mars_profile = {}
    dict_temp = {}
    for i in range(len(mars_planet_profile_df)):
        for j in range(1):
            dict_temp = {mars_planet_profile_df.iloc[i][j]: mars_planet_profile_df.iloc[i][j+1]}
            mars_profile.update(dict_temp)

    #* 5) Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) 
    #to obtain high resolution images for each of Mar's hemispheres.
    #* You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    #* Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing 
    #the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
    #* Append the dictionary with the image url string and the hemisphere title to a list. 
    # This list will contain one dictionary for each hemisphere.

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg"},
    ]

    mars_dict["mars_title"] = news_title
    mars_dict["mars_news"] = news_p
    mars_dict["mars_image"] = featured_image_url
    mars_dict["mars_currentweather"] = mars_weather
    mars_dict["mars_comparison"] = mars_comparison
    mars_dict["mars_profile"] = mars_profile
    mars_dict["mars_image_urls"] = hemisphere_image_urls

    return mars_dict
