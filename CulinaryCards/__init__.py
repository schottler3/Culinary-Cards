import os
import requests
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from datetime import *

from flask import Flask, redirect, render_template, session, url_for,request
from dotenv import find_dotenv, load_dotenv
from authlib.integrations.flask_client import OAuth
import dbinteractions as db
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/profile")
def profile():
    if 'user' in session:
        user = session['user']
        return render_template('profile.html', user=user)
    else:
        return redirect('/login')

@app.route("/createRecipe")
def createRecipe():
    return render_template("createRecipe.html")

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

    # api_url = f"https://api.edamam.com/search?q={user_query}&app_id={os.environ.get('EDAMAM_APP_ID')}&app_key={os.environ.get('EDAMAM_APP_KEY')}"

    # api_response = requests.get(api_url)

    # api_json = api_response.json()
    # print(api_json)

    # return render_template("test.html")
    return render_template("test.html")
    

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

if __name__ == "__main__":
    if os.getenv("FLASK_ENV") == "development":
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        app.run(debug=True)
    else:
        app.run()