# import libraries
import pandas as pd
import pymongo
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser

# define a placeholder for saved variables
mars_dict = {}

# function to get headlines, paragraphs, not images
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

    # browser reload
    browser.reload()

    # Close the browser after scraping
    browser.quit()
    
    #return scraped object
    return scrape_soup

# function to get Featured image
def get_featured_img_func(url):
    # Path to chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Go to website
    browser.visit(url)   
    
    # find "Full Image" button to click on it to get to next webpage
    full_img = browser.find_by_id("full_image")
    full_img.click()
    
    # find "More Info" button to click on it to get to next webpage
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    
    # read website's html
    html = browser.html
    soup = bs(html, 'html.parser')
    
    # find "a" tag to find href containing the URL
    result = browser.find_by_tag("a")
    relative_image_path = result[58]["href"] 
    
    # get image title
    relative_image_title = soup.find('h1', class_='article_title')
    relative_image_title = relative_image_title.get_text()
    relative_image_title = relative_image_title.split('\t')
    relative_image_title
    relative_image_title[4]
    final_title_feature_img = []
    final_title_feature_img.append({'Title': relative_image_title[4], 'URL': relative_image_path})    
    
    # Close the browser after scraping
    browser.quit()
    
    #return scraped object
    return final_title_feature_img

# function to get Hemis images
def get_hemis_img(url):
    # Path to chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
            
    # Go to website
    browser.visit(url)
    
    # read website's html
    html = browser.html
    soup = bs(html, 'html.parser')

    # find "a" tag
    result = browser.find_by_tag("a")
    
    # define a list to hold 1st link to full images
    hemis_image_path_list = []
    for i in range(8):
        # if link exist, skip saving to list
        if (result[i+4]["href"]) in hemis_image_path_list:
            print('')
        else:
            hemis_image_path_list.append(result[i+4]["href"])

    # browser reload
    browser.reload()

    # Close the browser after scraping
    browser.quit()
    
    final_hemis_img_url_list = []
    for i in range(len(hemis_image_path_list)):
        # Path to chromedriver
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
        
        # Go to website
        browser.visit(hemis_image_path_list[i])
        
        # read website's html
        html = browser.html
        soup = bs(html, 'html.parser')
        
        # get image title
        result_title = soup.find('h2', class_='title').get_text()  
        
        # get image URL
        result = soup.find('img', class_='wide-image')["src"]
        final_url = 'https://astrogeology.usgs.gov' + result
        
        # concat image URL to get complete URL link
        final_hemis_img_url_list.append({"title": result_title, "img_url": final_url})

        # browser reload
        browser.reload()

        # Close the browser after scraping
        browser.quit()
    
    return final_hemis_img_url_list



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

    # call function to get the URL
    final_title_feature_img = get_featured_img_func(url)

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

    # Split by new line \n
    mars_weather_splits = mars_weather.split('\n')   
    # Remove the twitter tag after pressure measurement
    temp = mars_weather_splits[2].split('pic.twitter.com/MhPPOHJg3m') 
    # Delete the pressure measurement with twitter tag   
    del mars_weather_splits[2]
    # add back filtered pressure
    mars_weather_splits.append(temp[0])
    # create a list of weather profile
    final_mars_weather = []
    temperature_list = ['Temperature', 'Wind', 'Pressure']
    for i in range(3):
        mars_weather_splits_dict = {'weather': temperature_list[i], 'value': mars_weather_splits[i]}
        final_mars_weather.append(mars_weather_splits_dict)

    ### 4) Mars Facts
    #* Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and 
    #use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    #* Use Pandas to convert the data to a HTML table string.

    # Set Website URL to scrape
    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)

    mars_earth_comp_df = tables[0]
    mars_earth_comp_df.columns = ['Mars-Earth Comparison', 'Mars', 'Earth']
    mars_comparison = []
    dict_temp = {}
    for i in range(len(mars_earth_comp_df)):
        for j in range(1):
            dict_temp = {"description": mars_earth_comp_df.iloc[i][j], "mars": mars_earth_comp_df.iloc[i][j+1], 
                        "earth": mars_earth_comp_df.iloc[i][j+2]}
            mars_comparison.append(dict_temp)
    
    mars_planet_profile_df = tables[1]
    mars_planet_profile_df.columns = ['Mars Planet Profile', 'Measurement']
    mars_profile = []
    dict_temp = {}
    for i in range(len(mars_planet_profile_df)):
        for j in range(1):
            dict_temp = {"description":mars_planet_profile_df.iloc[i][j], "value": mars_planet_profile_df.iloc[i][j+1]}
            mars_profile.append(dict_temp)

    #* 5) Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) 
    #to obtain high resolution images for each of Mar's hemispheres.
    #* You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    #* Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing 
    #the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
    #* Append the dictionary with the image url string and the hemisphere title to a list. 
    # This list will contain one dictionary for each hemisphere.

    # Set Website URL to scrape
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # call function to get Hemis Images URL
    final_hemis_img_url_list = get_hemis_img(url)

    mars_dict["mars_title"] = news_title
    mars_dict["mars_news"] = news_p
    mars_dict["mars_image"] = final_title_feature_img
    mars_dict["mars_currentweather"] = final_mars_weather
    mars_dict["mars_comparison"] = mars_comparison
    mars_dict["mars_profile"] = mars_profile
    mars_dict["mars_image_urls"] = final_hemis_img_url_list

    return mars_dict
