from flask import Flask, jsonify
import scrape_mars
import pymongo

app = Flask(__name__)

@app.route("/")
def welcome():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    db = client.scrape_db
    collection = db.items

    scraped_data = db.items.find()
    featured_image_url = scraped_data[0]['featured_image_url']
    hemisphere_image_url_list = scraped_data[0]['hemisphere_image_url_list']
    mars_html = scraped_data[0]['mars_html']
    mars_weather = scraped_data[0]['mars_weather']
    news_dict = scraped_data[0]['news_dict']

    scrape_dict = {
        'featured_image_url':featured_image_url,
        'hemisphere_image_url_list':hemisphere_image_url_list,
        'mars_html':mars_html,
        'mars_weather':mars_weather,
        'news_dict':news_dict
    }
    """List all available api routes."""
    return (
        jsonify(scrape_dict)
    )

@app.route("/scrape")
def scrape():

    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    """List all available api routes."""
    scrape_dict = scrape_mars.scrape()

    db = client.scrape_db
    collection = db.items
    collection.insert_one(scrape_dict)
    
    return (
        "data has been scraped"
    )

if __name__ == '__main__':
    app.run(debug=True)