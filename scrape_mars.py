from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from flask import jsonify


def scrape_news():
    page = requests.get("https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest")
    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.body
    divs = body.find_all('div',class_='slide')

    news_title = divs[0].find('div',class_='content_title').text
    news_p = divs[0].find('div',class_='rollover_description_inner').text

    news_dict = {'news_title':news_title.replace('\n',''), 'news_p':news_p.replace('\n','')}

    return news_dict

def grab_image():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')

    main_feature = soup.find('section', class_='main_feature')
    main_a = main_feature.find('a', class_='button')
    
    featured_image_url = main_a['data-fancybox-href']
    featured_dlink = main_a['data-link']
    
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image_url
    featured_dlink = "https://www.jpl.nasa.gov" + featured_dlink

    try:
        for x in range(1):
            html = browser.html
            soup = BeautifulSoup(html, 'lxml')


            browser.click_link_by_partial_text('MORE')
            time.sleep(3)

        slides = soup.find_all('li',class_='slide')
    except Exception as e:
        print(e)
    
    temp = 0

    for slide in slides:
        try:
            dlink = slide.a['data-link']
            img_url = slide.a['data-fancybox-href']

            if dlink == featured_dlink:
                featured_image_url = "https://www.jpl.nasa.gov" + img_url

        except KeyError as Ke:
            temp += 1
        except WebDriverException as WDE:
            temp += 1
        except Exception as e:
            temp += 1
    
    return featured_image_url

def get_mars_weather():
    page_weather = requests.get("https://twitter.com/marswxreport?lang=en")
    soup_weather = BeautifulSoup(page_weather.content, 'html.parser')
    body_weather = soup_weather.body
    divs_weather = body_weather.find_all('div',class_='content')
    temp_arr = []
    for div in divs_weather:
        temp_text = div.p.text
        if 'Sol ' in temp_text:
            temp_arr.append(temp_text)

    mars_weather = temp_arr[0]
    
    return mars_weather

def get_mars_data():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    mars_df = tables[0]
    
    mars_df.columns = ['Description','Value'];
    mars_df = mars_df.set_index('Description');
    mars_html = mars_df.to_html();
    mars_html = mars_html.replace('\n', '')

    return mars_html

def get_mars_hemisphere():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    url_hemispehere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemispehere)

    html_hemi = requests.get(url_hemispehere).text
    soup_hemi = BeautifulSoup(html_hemi, 'lxml')

    thumbs = soup_hemi.find_all('a', class_='product-item')

    thumb_list = []
    word_list = []

    for thumb in thumbs:
        thumb_list.append(thumb['href'])
        word_list.append(thumb['href'].split('/')[5].split('_')[0].title()) #title() capitalized first letter

    hemisphere_image_url = []
    try:
        for word in word_list:
            html_hemi = browser.html
            soup_hemi = BeautifulSoup(html_hemi, 'lxml')
            
            browser.click_link_by_partial_text(word)
            
            html_hemi_next = browser.html
            soup_hemi_next = BeautifulSoup(html_hemi_next, 'lxml')
            
            url_tag = soup_hemi_next.find('div', class_='downloads')
            url = url_tag.ul.li.a['href']
            
            title_tag = soup_hemi_next.find('h2',class_='title')
            title = title_tag.text
            
            hemisphere_image_url.append({'title': title, 'img_url': url})
            
            browser.back()
        
    except Exception as e:
        print(e)
        
    return hemisphere_image_url

def scrape():
    news_dict = scrape_news()
    featured_image_url = grab_image()
    mars_weather = get_mars_weather()
    mars_html = get_mars_data()
    hemisphere_image_url_list = get_mars_hemisphere()
    
    return_dict = {
        'news_dict': news_dict,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'mars_html':mars_html,
        'hemisphere_image_url_list': hemisphere_image_url_list
        }
    return return_dict

    #print(news_dict['news_title'])
    #print(news_dict['news_p'])
    #print(featured_image_url)
    #print(mars_weather)
    #print(mars_html)
    #print(hemisphere_image_url)