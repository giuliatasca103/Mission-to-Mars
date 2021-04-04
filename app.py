from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# tells python that our app will connect to Mongo using a URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# URI we use to connect our app to Mongo; saying app can reach mongo through server
mongo = PyMongo(app)

# when we visit web app's HTML page, we will see home page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   # tells flask to return an HTML template using index.html file
   # mars=mars tells python to use mars collection in mongodb
   return render_template("index.html", mars=mars)

# defines route that Flask will be using
# /scrape will run function that we create just beneath it
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

# tell it to run
if __name__ == "__main__":
   app.run()

