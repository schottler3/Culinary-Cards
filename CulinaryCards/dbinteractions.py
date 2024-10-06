import psycopg2
import os

####################################################################################
# users related functions

# dict has these keys: username, email, authid, fname,lname, bio
def addUserToDB(dict):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    str = "insert into users (username,user_email,authenticationid,fname,lname,bio) values (%s,%s,%s,%s,%s,%s)"
    try:
        cursor.execute(str,(dict["username"],dict["email"],dict["authid"],dict["fname"],dict["lname"],dict["bio"]))
        connection.commit()
    except:
        print("Failed to commit new user to users")
    finally:
        cursor.close()
        connection.close()

def getUserInfoByUserID(userID):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if userID is None:
        return {}
    try:
        str = "select * from users where userid = %s"
        cursor.execute(str, userID)
        result = cursor.fetchone()
        if result != None:
            resultdict = {}
            for col in range(len(cursor.description)):
                resultdict[cursor.description[col][0]] = result[col]
            return resultdict
        return {} 
    except:
        print("Failed to select user")
        return {}
    finally:
        cursor.close()
        connection.close()

def deleteUserByUsername(username):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if username is None:
        return False
    try:
        str = "delete from users where username = %s"
        cursor.execute(str, username)
        connection.commit()
    except:
        print("Failed to delete user")
    finally:
        cursor.close()
        connection.close()

def getLikeCountForUser(userid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if userid is None:
        return -1
    try:
        str = "select count(*) as likes from recipe_like where userid = %s"
        cursor.execute(str, userid)
        result = cursor.fetchone()
        if result[0] >= 0:
            return result[0]
        else:
            return -1
    except:
        print("Failed to get user like count")
    finally:
        cursor.close()
        connection.close()

def updateUser(username,email,fname,lname,bio,userid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    str = "update users set username = %s, user_email = %s, fname = %s, lname = %s, bio = %s where userid = %s"
    try:
        cursor.execute(str,(username,email,fname,lname,bio,userid))
        connection.commit()
    except:
        print("Failed to update user")
    finally:
        cursor.close()
        connection.close()

####################################################################################

# recipe related functions
def searchRecipeByKeywords(keywords):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if keywords is None:
        return {}
    keywords = keywords.split(" ")
    keywords = " & ".join(keywords)
    keywords += ":*"
    try:
        str = "select * from recipe_search where title_desc @@ to_tsquery(%s)"
        cursor.execute(str, keywords)
        result = cursor.fetchall()
        resultlst = []
        if result != None:
            for i in range(len(result)):
                resultdict = {}
                for col in range(len(cursor.description)):
                    resultdict[cursor.description[col][0]] = result[i][col]
                resultlst.append(resultdict)
        return resultlst 
    except:
        print("Failed to search recipe")
        return {}
    finally:
        cursor.close()
        connection.close()

# dict has keys: title,description, ingredients, instructions, userid
def addRecipeToDB(dict):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    str = "insert into recipe (title,description,ingredients,instructions,userid,title_desc) values (%s,%s,%s,%s,%s,to_tsvector(%s))"
    title_desc = dict["title"] + dict["description"]

    try:
        cursor.execute(str,(dict["title"],dict["description"],dict["ingredients"],dict["instructions"],dict["userid"],title_desc))
        connection.commit()
        cursor.execute("refresh materialized view recipe_search")
        connection.commit()
    except:
        print("Failed to commit new recipe")
    finally:
        cursor.close()
        connection.close()

# dict has keys: title,description, ingredients, instructions,recipeid
def updateRecipeInDB(dict):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    title_desc = dict["title"] + dict["description"]
    str = "update recipe set title = %s, description = %s, ingredients = %s, instructions = %s title_desc = to_tsvector(%s) where recipeid = %s"
    try:
        cursor.execute(str,(dict["title"],dict["description"],dict["ingredients"],dict["instructions"],title_desc),dict["recipeid"])
        connection.commit()
        cursor.execute("refresh materialized view recipe_search")
        connection.commit()
    except:
        print("Failed to update recipe")
    finally:
        cursor.close()
        connection.close()

def deleteRecipeInDB(recipeid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if recipeid is None:
        return False
    try:
        str = "delete from recipe where recipeid = %s"
        cursor.execute(str, recipeid)
        connection.commit()
        cursor.execute("refresh materialized view recipe_search")
        connection.commit()
    except:
        print("Failed to delete recipe")
    finally:
        cursor.close()
        connection.close()

def getRecipeLikes(recipeid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if recipeid is None:
        return -1
    try:
        str = "select count(*) as likes from recipe_like where recipeid = %s"
        cursor.execute(str, recipeid)
        result = cursor.fetchone()
        if result["likes"] >= 0:
            return result[0]
        else:
            return -1
    except:
        print("Failed to get recipe like count")
    finally:
        cursor.close()
        connection.close()

def getRecipeComments(recipeid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if recipeid is None:
        return -1
    try:
        str = "select count(*) as comments from recipe_comment where recipeid = %s"
        cursor.execute(str, recipeid)
        result = cursor.fetchone()
        if result["comments"] >= 0:
            return result[0]
        else:
            return -1
    except:
        print("Failed to get recipe comment count")
    finally:
        cursor.close()
        connection.close()

####################################################################################
#recipe_like funcitons

def addRecipeLike(recipeid,userid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    str = "insert into recipe_like (recipeid, userid) values(%s, %s)"
    try:
        cursor.execute(str,(recipeid,userid))
        connection.commit()
    except:
        print("Failed to add new recipe like")
    finally:
        cursor.close()
        connection.close()

def deleteRecipeLike(likeid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    try:
        str = "delete from recipe_like where likeid = %s"
        cursor.execute(str, likeid)
        connection.commit()
    except:
        print("Failed to delete recipe like")
    finally:
        cursor.close()
        connection.close()

####################################################################################
# recipe_comment functions

def addRecipeComment(userid,recipeid,comment_content):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    str = "insert into recipe_comment (recipeid, userid,comment_content) values(%s, %s,%s)"
    try:
        cursor.execute(str,(recipeid,userid,comment_content))
        connection.commit()
    except:
        print("Failed to add new recipe comment")
    finally:
        cursor.close()
        connection.close()

def deleteRecipeContent(commentid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    try:
        str = "delete from recipe_comment where commentid = %s"
        cursor.execute(str, commentid)
        connection.commit()
    except:
        print("Failed to delete recipe comment")
    finally:
        cursor.close()
        connection.close()

def updateRecipeComment(comment_content,commentid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    str = "update recipe_like set comment_content = %s where commentid = %s"
    try:
        cursor.execute(str,(comment_content,commentid))
        connection.commit()
    except:
        print("Failed to update recipe comment")
    finally:
        cursor.close()
        connection.close()

####################################################################################