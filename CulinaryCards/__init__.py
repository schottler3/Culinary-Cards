import os
import requests
import json
import uuid
# import schedule
import random
from os import environ as env
from urllib.parse import quote_plus, urlencode
from functools import wraps
import io
from datetime import *

from flask import Flask, redirect, render_template, session, url_for,request, json,send_file

from dotenv import find_dotenv, load_dotenv
from authlib.integrations.flask_client import OAuth
import dbinteractions as db
import recipeOfTheDay as rotd
import unsplash
import pandas as pd

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
    return render_template("index.html", recipeofday = rotd.getRecipeOfTheDay())

@app.route("/createRecipe", defaults={'recipeid': None}, methods=['GET'])
@app.route("/createRecipe/<int:recipeid>", methods=['GET'])
@requires_auth
def createRecipe(recipeid):
    if recipeid:
        recipe = db.getRecipeByID(recipeid)
        if(recipe[0][7] != session["user"]):
            return redirect("/recipe/" + str(recipeid))
        return render_template("createRecipe.html", recipeid=recipeid)
    else:
        return render_template("createRecipe.html")

@app.route("/search",methods=['GET'])
def redirectToSearch():
    sendData = []
    user_query = ""
    if request.args.get("queryhome") is not None:
        user_query = request.args.get("queryhome")
    results = db.searchRecipeByKeywords(user_query)
    for i in range(len(results)):
        for j in range(len(results[i]["ingredients"])):
            results[i]["ingredients"][j] = results[i]["ingredients"][j].split(",")[-1]
    print(results)
    for i in range(len(results)):
        results[i]["imagelink"] = "/api/getrecipeimage/" + str(results[i]["recipeid"])

    return render_template("searchResults.html",results=results)

@app.route("/search/category/<string:category>",methods=['GET'])
def redirectToSearchCategory(category):
    sendData = []
    results = db.getAllRecipesCategory(category)
    for i in range(len(results)):
        for j in range(len(results[i]["ingredients"])):
            results[i]["ingredients"][j] = results[i]["ingredients"][j].split(",")[-1]
    print(results)
    for i in range(len(results)):
        results[i]["imagelink"] = "/api/getrecipeimage/" + str(results[i]["recipeid"])
    return render_template("searchResults.html",results=results)

@app.route("/api/getrecipeimage/<int:recipeid>",methods=['GET'])
def getRecipePic(recipeid):
    img = db.getRecipePicture(recipeid)
    if img is not None:
        if img[1] == "img":
            stream = io.BytesIO(img[0])
            print(1)
            return send_file(stream,download_name=img[1]+str(recipeid)), 200
        elif img[1] == "link":
            print(2)
            print(img[0])
            image_from_link = requests.get(img[0])
            image_raw = io.BytesIO(image_from_link.content)
            return send_file(image_raw,mimetype="image/jpeg") , 200
        elif img[1] == "file":
            print(3)
            return send_file(img[0], mimetype='image/png'),200
    else:
        print(4)
        return send_file("static/test.png", mimetype='image/png'),200

@app.route("/login")
def login():
    session["nonce"] = str(uuid.uuid4().hex)
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True),nonce = session["nonce"]
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    try:
        AuthToken = oauth.auth0.authorize_access_token()
        token = oauth.auth0.parse_id_token(AuthToken, nonce = session["nonce"])
        if not token:
            raise Exception("No Token Found")
        token = token.get("sub")
        print(token)
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
    except:
        print("Error parsing 0Auth token")
        session.pop("user", None)
        session.pop("token", None)
    return redirect("/")

@app.route("/profile")
def profile():
    userid = 0
    if request.args.get("profile") is not None:
        userid = int(request.args.get("profile"))
    print("printing userid",userid)
    if userid > 0:
        user = db.getUserInfoByUserID(userid)
        userlikes = db.getLikeCountForUser(userid)
        print("likes",userlikes)
        recipes = db.getAllRecipesUserLikesDesc(userid)
        recipecount = len(recipes)
        isUser=False
        if "user" in session and "token" in session and int(session["user"]) == userid:
            isUser = True
        return render_template('profile.html', isUser=isUser, profile=userid, user=user,userlikes = userlikes,recipes = recipes,recipecount = recipecount)
    elif 'user' in session:
        user = session['user']
        if('token' in session):
            userid = db.getUserIDFromAuth(session['token']) 
            if userid != -1:
                user = db.getUserInfoByUserID(session['user'])
                userlikes = db.getLikeCountForUser(session['user'])
                recipes = db.getAllRecipesUserLikesDesc(session['user'])
                #recipes = [(1,2,3,4,5,6,7,8), (1,2,3,4,5,6,7,8)]
                recipecount = len(recipes)
                print(user)
                print(1)
                return render_template('profile.html',isUser=True,profile=userid, user=user,userlikes = userlikes,recipes = recipes,recipecount = recipecount)
            else:
                print(2)
                return redirect('/login')
        print(3)
        return render_template('profile.html', user=user,isUser=False)
    else:
        print(4)
        return redirect('/login')
    
@app.route("/profile/likes")
def profileGetLiked():
    userid = 0
    if request.args.get("profile") is not None:
        userid = int(request.args.get("profile"))
    print("printing userid",userid)
    if userid > 0:
        user = db.getUserInfoByUserID(userid)
        userlikes = db.getLikeCountForUser(userid)
        print("likes",userlikes)
        recipes = db.getAllLikedRecipesForUser(userid)
        recipecount = db.getCountUserRecipes(userid)
        isUser=False
        if "user" in session and "token" in session and int(session["user"]) == userid:
            isUser = True
        return render_template('profile.html', isUser=isUser, profile=userid, user=user,userlikes = userlikes,recipes = recipes,recipecount = recipecount)
    if 'user' in session:
        user = session['user']
        if('token' in session):
            userid = db.getUserIDFromAuth(session['token']) 
            if userid != -1:
                user = db.getUserInfoByUserID(session['user'])
                userlikes = db.getLikeCountForUser(session['user'])
                recipes = db.getAllLikedRecipesForUser(session['user'])
                recipecount = db.getCountUserRecipes(session['user'])
                print(user)
                print(1)
                return render_template('profile.html',profile=userid, user=user,userlikes = userlikes,recipes = recipes,recipecount = recipecount,isUser=True)
            else:
                print(2)
                return redirect('/login')
        print(3)
        return render_template('profile.html', user=user,isUser=False)
    else:
        print(4)
        return redirect('/login')
    
@app.route("/profile/saved")
def profileGetSaved():
    if 'user' in session:
        user = session['user']
        if('token' in session):
            userid = db.getUserIDFromAuth(session['token']) 
            if userid != -1:
                user = db.getUserInfoByUserID(session['user'])
                userlikes = db.getLikeCountForUser(session['user'])
                recipes = db.getAllSavedRecipesForUser(session['user'])
                recipecount = db.getCountUserRecipes(session['user'])
                print(user)
                print(1)
                return render_template('profile.html', profile=userid, user=user,userlikes = userlikes,recipes = recipes,recipecount = recipecount,isUser=True)
            else:
                print(2)
                return redirect('/login')
        print(3)
        return render_template('profile.html', user=user,isUser=False)
    else:
        print(4)
        return redirect('/login')

@app.route("/recipe/<int:recipeid>", methods=["GET", "POST", "DELETE"])
def viewRecipePage(recipeid):
    if request.method == 'DELETE':
        data = request.get_json()

        if 'user' in session and "token" in session:
            userid = session.get('user')
        else:
            return json.jsonify({"status": "failure", "message": "User not logged in"}), 400
        
        commentid = data.get('commentid')
        commentuserid = data.get('commentuserid')

        print(f"commentid: {commentid}, userid: {userid}, commentuserid: {commentuserid}")
        print(commentuserid == userid)
        if commentuserid is not None and userid is not None:
            if int(commentuserid) == int(userid):
                print("SDLKFHJSDHFJKSHDLKFJHKJDSLJFHSDKJLFHKJSDHLK")
                db.deleteRecipeContent(commentid)

    savedstatus = False
    likedstatus = False

    if('user' in session and "token" in session):
        savedstatus = db.checkSaved(session["user"],recipeid)
        likedstatus = db.checkLiked(session["user"],recipeid)

    result = db.getRecipeByID(recipeid)
    likecount = db.getRecipeLikes(recipeid)

    print(f"result 0 is: {result[0]}")

    result[0] = list(result[0])
    user = db.getProfilePicture(result[0][7])

    for ingredient in range(len(result[0][3])):
        result[0][3][ingredient] = result[0][3][ingredient].replace(","," of ")
        if result[0][3][ingredient][0] == "0" and result[0][3][ingredient][1] == " ":
            result[0][3][ingredient] = result[0][3][ingredient][2::]

    result[0].append("/api/getrecipeimage/" + str(result[0][0]))
    result[0] = tuple(result[0])
    t = pd.DataFrame({'timestamp': [pd.Timestamp(result[0][5])]})
    t['words'] = t['timestamp'].dt.strftime('%A, %B %d, %Y')

    comments = db.getAllCommentsForRecipe(recipeid)
    print(comments)

    return render_template("recipePage.html", likedstatus = likedstatus,savedstatus = savedstatus, recipe=result[0], time=t.words[0], comments=comments,likes=likecount)

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

@app.route("/api/getrecipe/<int:recipeid>",methods=['GET'])
def getRecipe(recipeid):
    result = db.getRecipeByID(recipeid)
    return json.jsonify({"status": "success", "message": "Recipe retrieved", "recipe": result}), 200


@app.route("/api/deleterecipe", methods=['DELETE'])
@requires_auth
def deleteRecipeAPI():
    data = request.get_json()
    if db.deleteRecipeInDB(data["recipeid"]):
        return json.jsonify({"status": "success", "message": "Recipe Deleted"}), 200
    else:
        return json.jsonify({"status": "failure", "message": "Recipe failed to DELETE"}),
    

@app.route("/api/addrecipe",methods=['POST'])
@requires_auth
def addRecipeAPI():
    data = request.get_json()
    title = data.get('title')
    categories = data.get('categories')
    description = data.get('description')
    ingredients = data.get('ingredients')
    instructions = data.get('instructions')
    photoUrl = data.get('photoUrl')

    if 'user' in session and "token" in session:
        userid = session.get('user')
    else:
        return json.jsonify({"status": "failure", "message": "User not logged in"}), 400

    recipeDict = {
        'title': title,
        'description': description,
        'categories': categories,
        'ingredients': ingredients,
        'instructions': instructions,
        'userid': userid
    }

    if photoUrl == 'None':
        recipeid = db.addRecipeToDB(recipeDict)
        if recipeid:
            return json.jsonify({"status": "success", "recipeID": recipeid}), 200
        else:
            return json.jsonify({"status": "failure", "message": "Recipe failed to ADD"}), 400
    elif photoUrl != "None":
        recipeid = db.addRecipeToDBWithImageURL(recipeDict, photoUrl)
        return json.jsonify({"status": "success", "message": "Recipe added", "recipeID": recipeid}), 200
    else:
        return json.jsonify({"status": "failure", "message": "Recipe failed to ADD"}), 400
    

@app.route("/api/setRecipeImage",methods=['POST'])
@requires_auth
def setRecipeImageAPI():
    photo = request.files['image']
    recipeid = request.form['recipeid']

    if db.setRecipeImage(recipeid, photo):
        return json.jsonify({"status": "success", "message": "Image added"}), 200
    else:
        return json.jsonify({"status": "failure", "message": "Image failed to ADD"}), 400


@app.route("/api/editprofile",methods=['PUT'])
@requires_auth
def submitEditProfile():
    edits = request.get_json()
    if db.updateUser(edits["username"],None,"","",edits["bio"],session["user"]):
        return json.jsonify({"status": "success", "message": "Profile updated"}), 200
    else:
        return json.jsonify({"status": "failure", "message": "Failed profile update"}), 400
    
@app.route("/api/editprofilepicture", methods=['PUT'])
@requires_auth
def submitEditProfilePic():
    if "newpfp" not in request.files:
        return "No new image sent", 400
    
    if db.UpdateProfilePicture(session["user"], request.files["newpfp"]):
        print("Profile picture updated successfully")
        return json.jsonify({"status": "success", "message": "Profile Picture updated"}), 200
    else:
        print("Failed to update profile picture")
        return json.jsonify({"status": "failure", "message": "Failed profile picture update"}), 400


@app.route("/api/setusersave/<int:recipeid>", methods=['GET'])
@requires_auth
def updateRecipeSaved(recipeid): 
    result = db.updateUserSavedStatus(recipeid,session["user"])
    print(result)
    if result == "saved":
        print("recipe saved!")
        return json.jsonify({"status": "saved", "message": "recipe saved"}), 200
    elif result == "unsaved":
        print("recipe unsaved!")
        return json.jsonify({"status": "unsaved", "message": "recipe unsaved"}), 200
    else:
        print("Failed to update saved recipe status")
        return json.jsonify({"status": "failure", "message": "Failed to save/unsave"}), 400
    
@app.route("/api/setuserlike/<int:recipeid>", methods=['GET'])
@requires_auth
def updateRecipeLiked(recipeid): 
    result = db.updateUserLikedStatus(recipeid,session["user"])
    print(result)
    if result == "liked":
        print("recipe liked!")
        return json.jsonify({"status": "liked", "message": "recipe saved"}), 200
    elif result == "unliked":
        print("recipe unliked!")
        return json.jsonify({"status": "unliked", "message": "recipe unsaved"}), 200
    else:
        print("Failed to update like recipe status")
        return json.jsonify({"status": "failure", "message": "Failed to like/unlike"}), 400

@app.route("/api/getprofilepicture/<int:userid>", methods=['GET'])
def getProfilePic(userid):
    img = db.getProfilePicture(userid)
    print(img)
    if img is not None:
        if img[1] == "img":
            stream = io.BytesIO(img[0])
            print(1)
            return send_file(stream, download_name=img[1] + str(userid)), 200
        elif img[1] == "link":
            print(2)
            return redirect(img[0]), 302
        elif img[1] == "file":
            print(3)
            return send_file(img[0], mimetype='image/png'), 200
    else:
        print(4)
        return send_file("static/test.png", mimetype='image/png'), 200

@app.route("/api/isuser",methods=['GET'])
def getUsernames():
    if request.args.get("username") is not None:
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
    
@app.route("/api/addcomment/<int:recipeid>",methods=['POST'])
def addComment(recipeid):
    data = request.get_json()

    if 'user' in session and "token" in session:
        userid = session.get('user')
    else:
        return json.jsonify({"status": "failure", "message": "User not logged in"}), 400
    
    comment = data.get('comment')
    comment_time = data.get('comment_time')

    commentDict = {
        "comment": comment,
        "userid": userid,
        "recipeid": recipeid,
        "comment_time": comment_time
    }

    userinfo = db.getUserInfoByUserID(userid)
    username = userinfo['username']
    # print(f"Received data - User ID: {userid}, Recipe ID: {recipeid}, Comment: {comment}, Comment Time: {comment_time}")
    commentid = db.addCommentToDB(commentDict)
    return json.jsonify({"commentid": commentid, "userid": userid, "username": username}), 200

if __name__ == "__main__":
    if os.getenv("FLASK_ENV") == "development":
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        app.run(debug=True)
    else:
        app.run()


@app.route("/api/getrecipepreviewimage",methods=['GET'])
def getRecipePreviewImage():
    title = request.args.get("title")
    imgurl = unsplash.getImgUrl(title)
    return json.jsonify({"status": "success", "message": "Image URL retrieved", "imgurl": imgurl}), 200

@app.route("/api/getrecipeimage/<int:recipeid>",methods=['GET'])
def getRecipeImage(recipeid):
    img = db.getRecipePhoto(recipeid)
    print(img)
    if img is not None:
        if img[1] == "img":
            stream = io.BytesIO(img[0])
            print(1)
            return send_file(stream, download_name=f"{img[1]}_{session['user']}.png"), 200
        elif img[1] == "link":
            print("Link is: ", img[0])
            return redirect(img[0]), 302
        elif img[1] == "file":
            print(3)
            return send_file(img[0], mimetype='image/png'), 200
    else:
        print(4)
        return send_file("static/test.png", mimetype='image/png'), 200
    
@app.route("/api/updaterecipe",methods=['PUT'])
@requires_auth
def updateRecipe():
    data = request.get_json()
    recipeData = data.get('recipeData')
    title = recipeData.get('title')
    description = recipeData.get('description')
    ingredients = recipeData.get('ingredients')
    instructions = recipeData.get('instructions')
    categories = recipeData.get('categories')
    recipeid = data.get('recipeid')
    photoUrl = recipeData.get('photoUrl')

    recipeDict = {
        'title': title,
        'description': description,
        'ingredients': ingredients,
        'instructions': instructions,
        'recipeid': recipeid,
        'categories': categories
    }

    if db.updateRecipeInDB(recipeDict):
        if photoUrl != 'None':
            if db.updateRecipeURL(recipeid, photoUrl):
                return json.jsonify({"status": "success", "message": "Recipe updated with url"}), 200
        else:
            return json.jsonify({"status": "success", "message": "Recipe updated without url"}), 200
    else:
        return json.jsonify({"status": "failure", "message": "Recipe failed to UPDATE"}), 400

@app.route("/api/updaterecipeimage",methods=['POST'])
@requires_auth
def setRecipeImage():
    photo = request.files['image']
    recipeid = request.form['recipeid']

    if db.updateRecipeImage(recipeid, photo):
        return json.jsonify({"status": "success", "message": "Image added"}), 200
    else:
        return json.jsonify({"status": "failure", "message": "Image failed to ADD"}), 400

@app.route("/api/deleteaccount",methods=['DELETE'])
def deleteAccount():
    if 'user' in session and "token" in session:
        if db.deleteUserByUserID(session['user']):
            session.clear()
            return json.jsonify({"status": "success", "message": "Account Deleted"}), 200
        else:
            return json.jsonify({"status": "failure", "message": "Account failed to DELETE"}), 400
    else:
        return json.jsonify({"status": "failure", "message": "User not logged in"}), 400
