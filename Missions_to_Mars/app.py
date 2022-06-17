# MongoDB and Flask Application
#################################################

# Dependencies and Setup
from distutils.log import debug
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


# Flask Setup
#################################################
app = Flask(__name__)

# PyMongo Connection Setup
#################################################
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Flask Routes
#################################################
# Root Route to Query MongoDB & Pass Mars Data Into HTML Template: index.html to Display Data
# forward slash
# Print(dir(mongo))
# collection = table
@app.route("/")
def index():
    mars_data = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars_data)

# Scrape Route to Import `scrape_mars.py` Script & Call `scrape` Function
# decorator @
# if you want to visit this page you need /scrape
# upsert(update/insert) make the collection flexiable
@app.route("/scrape")
def scrapper():
    mars_info = scrape_mars.scrape_all()
    mars_collection = mongo.db.mars
    mars_collection.update({}, {"$set":mars_info}, upsert=True)
    return redirect("/")
    

if __name__ == "__main__":
    app.run(debug=True)