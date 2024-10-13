import os
import requests
import json
import uuid
import schedule
import random
from os import environ as env
from urllib.parse import quote_plus, urlencode
from functools import wraps

from datetime import *

from flask import Flask, redirect, render_template, session, url_for,request, json

from dotenv import find_dotenv, load_dotenv
from authlib.integrations.flask_client import OAuth
import dbinteractions as db
import apirequests as apireq
import apirequests as apireq
import recipeOfTheDay as rotd

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
        


# https://stackoverflow.com/questions/63449414/is-there-a-way-that-i-can-make-a-python-command-get-sent-at-exactly-midnight
# schedule.every().day().at("00:00").do(getRecipeOfDay)

# initial call
rotd.setRecipeOfTheDay()

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'user' not in session and 'token' not in session:
      # Redirect to Login page here
      return redirect('/login')
    return f(*args, **kwargs) #do the normal behavior -- return as it does.

  return decorated

@app.route("/")
def index():
    return render_template("index.html",recipeofday = rotd.getRecipeOfTheDay())

@app.route("/createRecipe")
def createRecipe():
    return render_template("createRecipe.html")

@app.route("/search",methods=['POST'])
def redirectToSearch():
    sendData = []
    user_query = request.form["queryhome"]
    results = db.searchRecipeByKeywords(user_query)
    # if len(results) < 1:
    #     results = apireq.recipe_search(user_query)
    # for item in results:
    #     recipe = item['recipe']
    #     label = recipe.get('label')
    #     calories = recipe.get('calories')
    #     sendData.append([label, calories])
    for item in results:
        print(f"item: {item}")
    return render_template("searchResults.html",results=results)

@app.route("/login")
def login():
    
    session["nonce"] = str(uuid.uuid4().hex)
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True),nonce = session["nonce"]
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    AuthToken = oauth.auth0.authorize_access_token()
    token = oauth.auth0.parse_id_token(AuthToken, nonce = session["nonce"])
    token = token.get("sub")
    userId = db.getUserIDFromAuth(token)
    if  userId != -1:
        session["user"] = userId
        session["token"] = token
    else:
        db.addUserToDBAuthOnly(token)
        userId = db.getUserIDFromAuth(token)
        session["user"] = userId
        session["token"] = token
    return redirect("/")

@app.route("/profile")
def profile():
    if 'user' in session:
        user = session['user']
        if('token' in session):
            userid = db.getUserIDFromAuth(session['token']) 
            if userid != -1:
                user = db.getUserInfoByUserID(session['user'])
                userlikes = db.getLikeCountForUser(session['user'])
                recipes = db.getAllRecipesUser(session['user'])
                #recipes = [(1,2,3,4,5,6,7,8), (1,2,3,4,5,6,7,8)]
                recipecount = len(recipes)
                print(user)
                print(1)
                return render_template('profile.html', user=user,userlikes = userlikes,recipes = recipes,recipecount = recipecount)
            else:
                print(2)
                return redirect('/login')
        print(3)
        return render_template('profile.html', user=user)
    else:
        print(4)
        return redirect('/login')

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

@requires_auth
@app.route("/api/deleterecipe",methods=['DELETE'])
def deleteRecipeAPI():
    request = request.get_json()
    #TODO Need to verify that user owns the recipe before deleting
    if db.deleteRecipe(request["recipeid"]):
        return json.jsonify({"status": "success", "message": "Recipe Deleted"}), 200
    else:
        return json.jsonify({"status": "failure", "message": "Recipe failed to DELETE"}), 400

@requires_auth
@app.route("/api/editprofile",methods=['PUT'])
def submitEditProfile():
    edits = request.get_json()
    if db.updateUser(edits["username"],None,"","",edits["bio"],session["user"]):
        return json.jsonify({"status": "success", "message": "Profile updated"}), 200
    else:
        return json.jsonify({"status": "failure", "message": "Failed profile update"}), 400
    
@app.route("/api/isUser",methods=['PUT'])
def getUsernames():
    username = request.args.get("username")
    if db.getUserInstanceFromUsername(username):
        return json.jsonify({"status": "success", "message": "True"}), 200
    else:
        return json.jsonify({"status": "failure", "message": "False"}), 400

@app.route("/api/getuserpostsbylikes",methods=['PUT'])
def getUserPostsSortByLikes():
    userid = request.get_json()
    #userid should be in the userid["userid"] location
    results = db.getAllRecipesUserLikesDesc(userid["userid"])
    lst =[]
    for recipe in results:
        lst.append({
            "recipeid" : recipe[0],
            "title" : recipe[1],
            "description" : recipe[2],
            "ingredients" : recipe[3],
            "instructions" : recipe[4],
            "createdon" : recipe[5],
            "likecount" : recipe[6],
        })

    if len(results) != 0:
        return json.jsonify({"status": "success", "message": "Succeeded to sort user profile by likes", "results" : lst}), 200
    else:
        return json.jsonify({"status": "failure", "message": "Failed to sort user profile by likes"}), 400



if __name__ == "__main__":
    if os.getenv("FLASK_ENV") == "development":
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        app.run(debug=True)
    else:
        app.run()

#######################################################
#Adam's test stuff
# testdictuser = {
    #     "username" : "Adam",
    #     "email" : "adamkvant@gmail.com",
    #     "authid" : "ijfoqwdjiojwoidjq",
    #     "fname" : "Adam",
    #     "lname" : "Kvant",
    #     "bio" : "Hello World"
    # }

    # testdictrecipe = {
    #     "title" : "Chicken Alfredo",
    #     "description" : "The superior pasta",
    #     "ingredients" : ["Chicken","Alfredo"],
    #     "instructions" : ["Add love"],
    #     "userid" : "1"
    # }

    # testdictrecipeupdate = {
    #     "title" : "Chicken Alfredo2",
    #     "description" : "The bestest pasta",
    #     "ingredients" : ["Chicken","Alfredo Sauce","Pesto"],
    #     "instructions" : ["Add pasta","Add chicken"],
    #     "recipeid" : "1"
    # }

    #db.addUserToDB(testdictuser)
    # db.updateUser("Adam2","kvant003@umn.edu","Kvant","Adam","World Hello","2")
    db.addRecipeToDB(testdictrecipe)
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