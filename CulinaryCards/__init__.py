import os
import psycopg2
import requests
from datetime import *
from flask import Flask
from flask import *
import dbinteractions as db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search",methods=['POST'])
def redirectToSearch():
    user_query = request.form["queryhome"]

    results = db.searchRecipeByKeywords(user_query)
    testdictuser = {
        "username" : "Adam",
        "email" : "adamkvant@gmail.com",
        "authid" : "ijfoqwdjiojwoidjq",
        "fname" : "Adam",
        "lname" : "Kvant",
        "bio" : "Hello World"
    }

    testdictrecipe = {
        "title" : "Chicken Alfredo",
        "description" : "The superior pasta",
        "ingredients" : ["Chicken","Alfredo"],
        "instructions" : ["Add love"],
        "userid" : "1"
    }

    testdictrecipeupdate = {
        "title" : "Chicken Alfredo2",
        "description" : "The bestest pasta",
        "ingredients" : ["Chicken","Alfredo Sauce","Pesto"],
        "instructions" : ["Add pasta","Add chicken"],
        "recipeid" : "1"
    }

    #db.addUserToDB(testdictuser)
    # db.updateUser("Adam2","kvant003@umn.edu","Kvant","Adam","World Hello","2")
    #db.addRecipeToDB(testdictrecipe)
    # db.deleteRecipeInDB("1")
    # db.updateRecipeInDB(testdictrecipeupdate)
    # db.addRecipeLike("2","2")
    # print(db.getAllLikedRecipesForUser("2"))
    # print(db.searchRecipeByKeywords("Chicken"))

    # api_url = f"https://api.edamam.com/search?q={user_query}&app_id={os.environ.get('EDAMAM_APP_ID')}&app_key={os.environ.get('EDAMAM_APP_KEY')}"
    
    # api_response = requests.get(api_url)

    # api_json = api_response.json()
    # print(api_json)

    return render_template("test.html",results=results)

if __name__ == "__main__":
    if os.getenv("FLASK_ENV") == "development":
        app.run(debug=True)
    else:
        app.run()