from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_info_db")

@app.route("/")
def index():
    mars_info = mongo.db.mars.find_one()
    return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars_dict = scrape_mars.scrape()

    mars.update({}, mars_dict, upsert=True)
    return redirect("/", code=302)
    #return ("/localhost/scrape")

if __name__ == "__main__":
    app.run(debug=True)
