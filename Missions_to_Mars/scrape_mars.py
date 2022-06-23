# Jupyter Notebook Conversion to Python Script
################################################

# Dependencies and Setup
from string import whitespace
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# Set Executable Path & Initialize Chrome Browser
#################################################
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)

# NASA Mars News Site Web Scraper
#################################################
def mars_news(browser):
    # Visit the NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    # Parse Results HTML with BeautifulSoup
    # Find Everything Inside:
    #   <ul class="item_list">
    #     <li class="slide">
    try:
        slide_element = news_soup.select_one("ul.item_list li.slide")
        slide_element.find("div", class_="content_title")

        # Scrape the Latest News Title
        # Use Parent Element to Find First <a> Tag and Save it as news_title
        news_title = slide_element.find("div", class_="content_title").get_text()

        news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_paragraph


# JPL Mars Space Images - Featured Image
#################################################

def featured_image(browser):
    # Visit the JPL 
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    full_image_button = browser.find_by_tag("button")[1]
    full_image_button.click()

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    try:
        # img_url = img.get("src")
     img_url = image_soup.find("img",class_='fancybox-image').get("src")
    except AttributeError:
        return None 
   # Use Base URL to Create Absolute URL
    img_url = f"https://spaceimages-mars.com/{img_url}"
    return img_url


# Mars Facts
#################################################
# Mars Facts Web Scraper
def mars_facts():
    # Visit the Mars Facts Site Using Pandas to Read
    try:
        df = pd.read_html("https://galaxyfacts-mars.com/")[0]
    except BaseException:
        return None
    df.columns=["Description", "Mars","Earth"]
    # df.set_index("Description", inplace=True)

    return df.to_html(classes="table table-striped",)

# Mars Hemispheres
#################################################
# Mars Hemispheres Web Scraper
def hemisphere(browser):
    # Visit the USGS Astrogeology Science Center Site
    url = "https://marshemispheres.com/"
    browser.visit(url)

    hemisphere_image_urls = []

    # Get a List of All the Hemisphere
    # h3 is where the title is and size the class is iteamLink product-item
    links = browser.find_by_css("iteamLink product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()
        
        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.find_link_by_text("Description").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h3.title").text
        
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate Backwards
        browser.back()
    return hemisphere_image_urls

# Helper Function
def scrape_hemisphere(html_text):
    hemisphere_soup = BeautifulSoup(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere


# Main Web Scraping Bot
#################################################
def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    facts = mars_facts()
    hemisphere_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "facts": facts,
        "hemispheres": hemisphere_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())

