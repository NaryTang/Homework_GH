from splinter import Browser
from bs4 import BeautifulSoup

def init_browser():
	executable_path = {'executable_path': 'chromedriver.exe'}
	return Browser('chrome', **executable_path, headless=False)

def scrape():
	browser = init_browser()

	listings = {}

	#!/usr/bin/env python
	# coding: utf-8

	# ### NASA Mars News

	# In[1]:


		# Dependencies
	from bs4 import BeautifulSoup
	import requests
	import pymongo


		# In[2]:


		# Initialize PyMongo to work with MongoDBs
	conn = 'mongodb://localhost:27017'
	client = pymongo.MongoClient(conn)


		# In[4]:


		# Define database and collection
	db = client.mars_db
	collection = db.articles


	# In[5]:


	# URL of page to be scraped
	url_news = "https://mars.nasa.gov/news/"

	# Retrieve page with the requests module
	response = requests.get(url_news)
	# Create BeautifulSoup object; parse with 'lxml'
	soup = BeautifulSoup(response.text, 'lxml')


	# In[27]:


	soup


	# In[36]:


	# Retrieve the parent divs for titles
	news_title = soup.find("img", class_="img-lazy")["alt"]


	# In[38]:


	# Retrieve the parent divs for paragrpahs
	news_paragraph = soup.find("div", class_="rollover_description_inner").text.strip()


	# ### JPL Mars Space Images - Featured Image

	# In[106]:


	# Dependencies
	from splinter import Browser
	from splinter.exceptions import ElementDoesNotExist
	from bs4 import BeautifulSoup

	# In[110]:


	executable_path = {'executable_path': 'chromedriver.exe'}
	browser = Browser('chrome', **executable_path, headless=False)


	# In[111]:


	url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(url_jpl)


	# In[112]:


	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')

	image_link = soup.find("article", class_="carousel_item")["style"]



	# In[ ]:


	image_link


	# In[79]:


	featured_url = image_link[23:-3]


	# In[82]:


	featured_image_url = "https://www.jpl.nasa.gov"+ featured_url


	# In[83]:


	featured_image_url


	# ### Mars Weather

	# In[113]:


	# Define database and collection
	db = client.mars_weather_db
	collection = db.articles


	# In[120]:


	# URL of page to be scraped
	url_weather = "https://twitter.com/marswxreport?lang=en"

	# Retrieve page with the requests module
	response = requests.get(url_weather)
	# Create BeautifulSoup object; parse with 'lxml'
	soup_mars_weather = BeautifulSoup(response.text, 'lxml')


	# In[121]:


	#soup_mars_weather


	# In[126]:


	# Retrieve the parent divs for all articles
	results = soup_mars_weather.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
	results


	# In[130]:


	# remove tail
	mars_weather = results[:-26]
	mars_weather


	# ### Mars Facts

	# In[131]:


	import pandas as pd


	# In[132]:


	url_mars_facts = "https://space-facts.com/mars/"


	# In[133]:


	tables = pd.read_html(url_mars_facts)
	tables


	# In[134]:


	type(tables)


	# In[136]:


	mars_facts_df = tables[0]
	mars_facts_df.columns


	# In[137]:


	mars_facts_df.head()


	# In[149]:


	mars_facts_df.columns = ["Description", "Values"]
	mars_facts_df.head()


	# ### DataFrames as HTML

	# In[150]:


	html_table = mars_facts_df.to_html()
	html_table


	# In[151]:


	html_table.replace("\n", "")


	# In[154]:


	mars_facts_df.to_html("table.html", index = False)


	# In[157]:


	#get_ipython().system('explorer table.html')


	# ### Mars Hemispheres

	# In[158]:


	hemisphere_image_urls = [
	    {"title": "Valles Marineris Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
	    {"title": "Cerberus Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
	    {"title": "Schiaparelli Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
	    {"title": "Syrtis Major Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
	]


	# ## Step 2 - MongoDB and Flask Application

	# In[ ]:
	listings = {
		"news_title": news_title,
		"news_paragraph": news_paragraph,
		"featured_image_url" : featured_image_url,
		"mars_weather": mars_weather,
		"hemisphere_image_urls": hemisphere_image_urls
	}

	return listings




