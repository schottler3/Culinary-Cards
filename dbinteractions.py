import psycopg2
import os
####################################################################################
# users related functions
# Returns Boolean if user is not in system
def getUserInstanceFromUsername(username):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if username is None:
        return False
    try:
        qstr = "select * from users where username = %s"
        cursor.execute(qstr,(username,))
        result = cursor.fetchone()
        if result is not None:
            return True
        return False
    except:
        print(f"Failed to select user")
        return False
    finally:
        cursor.close()
        connection.close()


# Returns -1 if user is not in system
def getUserIDFromAuth(auth):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if auth is None:
        return -1
    try:
        qstr = "select userID from users where authenticationid = %s"
        cursor.execute(qstr,(auth,))
        result = cursor.fetchone()
        if result != None:
            return result[0]
        return -1 
    except:
        print(f"Failed to select user")
        return -1
    finally:
        cursor.close()
        connection.close()
    
def addUserToDBAuthOnly(auth):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    # str was messing with str method :(
    qstr = "insert into users (username,authenticationid,bio) values (%s,%s,%s)"
    try:
        cursor.execute("select max(userid) from users")
        maxid = cursor.fetchone()[0]
        cursor.execute(qstr,("user" + str(maxid+1),auth,""))
        connection.commit()
    except:
        print("Failed to commit new user to users with auth")
    finally:
        cursor.close()
        connection.close()


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
    print(userID)
    try:
        qstr = "select * from users where userid = %s"
        cursor.execute(qstr, (str(userID),))
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

def deleteUserByUserID(userid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if userid is None:
        return False
    try:
        str = "delete from users where userid = %s"
        cursor.execute(str, userid)
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
        cursor.execute(str, (userid,))
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
        return True
    except:
        print("Failed to update user")
        return False
    finally:
        cursor.close()
        connection.close()


# Returns list of tuples in form: (recipeid,title,description,ingredients,instructions,created_on,user_id)
def getAllLikedRecipesForUser(userid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if userid is None:
        return []
    try:
        str = """select recipe.recipeid, recipe.title, recipe.description, recipe.ingredients, recipe.instructions, recipe.created_on,recipe.userid
        from recipe_like join recipe on recipe_like.recipeid = recipe.recipeid
        where recipe_like.userid = %s"""
        cursor.execute(str, (userid,))
        result = cursor.fetchall()
        if result:
            return result
        else:
            return []
    except:
        print("Failed to get liked recipes")
        return []
    finally:
        cursor.close()
        connection.close()

# Returns list of tuples in form: (recipeid,title,description,ingredients,instructions,created_on,likecount)
def getAllRecipesUser(userid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if userid is None:
        return []
    try:
        str = """
            select recipe.recipeid, recipe.title, recipe.description, recipe.ingredients,
            recipe.instructions, recipe.created_on,count(recipe_like.likeid) as postlikes
            from recipe
            left join recipe_like on recipe.recipeid = recipe_like.recipeid
            where recipe.userid = %s
            group by recipe.recipeid"""
        cursor.execute(str, (userid,))
        result = cursor.fetchall()
        if result:
            return result
        else:
            return []
    except:
        print("Failed to get recipes for specific user")
    finally:
        cursor.close()
        connection.close()

# Returns list of tuples in form: (recipeid,title,description,ingredients,instructions,created_on,likecount)
def getAllRecipesUserLikesDesc(userid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if userid is None:
        return []
    try:
        str = """
            select recipe.recipeid, recipe.title, recipe.description, recipe.ingredients, 
            recipe.instructions, recipe.created_on,count(recipe_like.likeid) as postlikes
            from recipe
            left join recipe_like on recipe.recipeid = recipe_like.recipeid
            where recipe.userid = %s
            group by recipe.recipeid
            order by postlikes desc
            """
        cursor.execute(str, (userid,))
        result = cursor.fetchall()
        if result:
            return result
        else:
            return []
    except:
        print("Failed to get recipes for specific user")
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
        str = "select * from recipe_search where title_desc_ingredients_username @@ to_tsquery(%s)"
        cursor.execute(str, (keywords,))
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
# ingredients & instructions are lists of strings
def addRecipeToDB(dict):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    str = "insert into recipe (title,description,ingredients,ingredients_nomeasure,instructions,userid,title_desc_ingredients_username) values (%s,%s,%s,%s,%s,%s,to_tsvector(%s))"
    title_desc_ingredients_username = dict["title"] + " " + dict["description"]
    ingredients_nomeasure = ""
    for ingredient in dict["ingredients"]:
        ingredients = ingredient.split(",")
        title_desc_ingredients_username += " " + ingredients[0]
        ingredients_nomeasure += ingredients[0] + " "
    try:
        cursor.execute("select username from users where userid = %s", dict["userid"])
        username = cursor.fetchone()[0]
        title_desc_ingredients_username += " " + username
        cursor.execute(str,(dict["title"],dict["description"],dict["ingredients"],ingredients_nomeasure,dict["instructions"],dict["userid"],title_desc_ingredients_username))
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
    title_desc_ingredients_username = dict["title"] + " " + dict["description"]
    ingredients_nomeasure = ""
    for ingredient in dict["ingredients"]:
        ingredients = ingredient.split(",")
        title_desc_ingredients_username += " " + ingredients[0]
        ingredients_nomeasure += ingredients[0] + " "
    # str was messing with str method :(
    qstr = "update recipe set title = %s, description = %s, ingredients = %s, ingredients_nomeasure = %s,instructions = %s, title_desc_ingredients_username = to_tsvector(%s) where recipeid = %s"
    try:
        cursor.execute("select userid from recipe where recipeid = %s",dict["recipeid"])
        userid = cursor.fetchone()[0]
        userid = str(userid)
        cursor.execute("select username from users where userid = %s",userid)
        username = cursor.fetchone()[0]
        title_desc_ingredients_username += " " + username
        cursor.execute(qstr,(dict["title"],dict["description"],dict["ingredients"], ingredients_nomeasure,dict["instructions"],title_desc_ingredients_username,dict["recipeid"]))
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
        cursor.execute(str, (recipeid,))
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
        if result[0] >= 0:
            return result[0]
        else:
            return -1
    except:
        print("Failed to get recipe like count")
    finally:
        cursor.close()
        connection.close()

def getRecipeCommentCount(recipeid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if recipeid is None:
        return -1
    try:
        str = "select count(*) as comments from recipe_comment where recipeid = %s"
        cursor.execute(str, recipeid)
        result = cursor.fetchone()
        if result[0] >= 0:
            return result[0]
        else:
            return -1
    except:
        print("Failed to get recipe comment count")
    finally:
        cursor.close()
        connection.close()

# Returns list of tuples in form: (commentid,comment_time,comment_content,username,userid)
def getAllCommentsForRecipe(recipeid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if recipeid is None:
        return []
    try:
        str = """select recipe_comment.commentid, recipe_comment.comment_time, recipe_comment.comment_content, users.username, users.userid
        from recipe_comment
        join users on recipe_comment.userid = users.userid 
        where recipe_comment.recipeid = %s
        order by recipe_comment.comment_time desc"""
        cursor.execute(str, (recipeid,))
        result = cursor.fetchall()
        if result:
            return result
        else:
            return []
    except:
        print("Failed to get all comments for specific recipe")
        return []
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