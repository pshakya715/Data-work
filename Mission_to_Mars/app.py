# import necessary libraries
from flask import Flask, render_template
from flask_pymongo import PyMongo
import mission_to_mars

# create instance of Flask app
app = Flask(__name__)

#.config["MONGO_URI"] = "mongodb://localhost:27017/"
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# create route that renders index.html template
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = mission_to_mars.scrape() 
    mars.update({}, mars_data, upsert=True)
    return "Scrapping done!"

if __name__ == "__main__":
    app.run(debug=True)
    