import psycopg2
import os
from flask import request
from psycopg2 import Binary
from unsplash import getImgUrl
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
    qstr = "insert into users (username,authenticationid,bio) values (%s,%s,%s) returning userid"
    try:
        cursor.execute("select max(userid) from users")
        maxid = cursor.fetchone()[0]
        if(maxid is None):
            maxid = 0
        cursor.execute(qstr,("user" + str(maxid+1),auth,""))
        result = cursor.fetchone()[0]
        cursor.execute("insert into profile_img (userid) values (%s)",(result,))
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
        qstr = "delete from users where userid = %s"
        cursor.execute(qstr, (str(userid),))
        connection.commit()
        return True
    except:
        print("Failed to delete user")
        return False
    finally:
        cursor.close()
        connection.close()

def getLikeCountForUser(userid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if userid is None:
        return -1
    try:
        str = """select count(recipe_like.likeid) as total_likes
                from users
                join recipe on users.userid = recipe.userid
                left join recipe_like on recipe.recipeid = recipe_like.recipeid
                where users.userid = %s
                group by users.userid, users.username;
                """
        cursor.execute(str, (userid,))
        result = cursor.fetchone()
        if result[0] >= 0:
            return result[0]
        else:
            return 0
    except:
        print("Failed to get user like count, most likely doesn't have likes")
        return 0
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

def updateUserWithPicture(username,email,fname,lname,bio,userid,imgfile):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    str = "update users set username = %s, user_email = %s, fname = %s, lname = %s, bio = %s where userid = %s"
    img_str = "insert into profile_img (image_data,userid) values (%s,%s)"
    img_str_update = "update profile_img set image_data = %s where userid = %s"
    imgfileRAW = imgfile.read()
    try:
        cursor.execute(str,(username,email,fname,lname,bio,userid))
        cursor.execute("select * from profile_img where userid = %s")
        does_user_exist = cursor.fetchall()
        if not does_user_exist:
            cursor.execute(img_str,(Binary(imgfileRAW),userid))
        else:
            cursor.execute(img_str_update,Binary(imgfileRAW),userid)
        connection.commit()
        return True
    except:
        print("Failed to update user")
        return False
    finally:
        cursor.close()
        connection.close()

def UpdateProfilePicture(userid,image):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    img_str_update = "update profile_img set image_data = %s where userid = %s"
    imgFileRAW = image.read()
    try:
        cursor.execute(img_str_update,(Binary(imgFileRAW),userid))
        connection.commit()
        return True
    except:
        print("Failed to update user image")
        return False
    finally:
        cursor.close()
        connection.close()

def getProfilePicture(userid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    print(userid,"userid")
    img_str = "select image_data, image_link_sso from profile_img where userid = %s"
    try:
        cursor.execute(img_str,(userid,))
        result = cursor.fetchone()
        if result[0] is not None:
            return (result[0],"img")
        elif result[1] is not None:
            return (result[1],"link")
        else:
            return ("static/test.png", "file")
    except:
        print("Failed to get user image")
        return None
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
        where recipe_like.userid = %s
        order by recipe_like.like_time desc"""
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

# Returns list of tuples in form: (recipeid,title,description,ingredients,instructions,created_on,user_id)
def getAllSavedRecipesForUser(userid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if userid is None:
        return []
    try:
        str = """select recipe.recipeid, recipe.title, recipe.description, recipe.ingredients, recipe.instructions, recipe.created_on,recipe.userid
        from recipe_saved join recipe on recipe_saved.recipeid = recipe.recipeid
        where recipe_saved.userid = %s
        order by recipe_saved.savedtime desc"""
        cursor.execute(str, (userid,))
        result = cursor.fetchall()
        if result:
            return result
        else:
            return []
    except:
        print("Failed to get saved recipes")
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
        str = """select recipe.recipeid, recipe.title, recipe.description, recipe.ingredients,recipe.instructions, recipe.created_on, count(recipe_like.likeid) as postlikes
                from recipe left join recipe_like on recipe.recipeid = recipe_like.recipeid where recipe.userid = %s
                group by recipe.recipeid, recipe.title, recipe.description, recipe.ingredients, recipe.instructions, recipe.created_on
                order by postlikes desc;"""
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

def getCountUserRecipes(userid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if userid is None:
        return -1
    try:
        qstr = "select count(*) from recipe where userid = %s"
        cursor.execute(qstr,(userid,))
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
        str = """
                select recipe_search.recipeid,recipe_search.title,recipe_search.description,recipe_search.ingredients,
                recipe_search.instructions,users.username,recipe_search.categories,count(recipe_like.likeid) as like_count,
                recipe_img.image_data,recipe_img.image_link,users.userid
                from recipe_search
                join recipe on recipe_search.recipeid = recipe.recipeid
                join users on recipe.userid = users.userid
                left join recipe_like on recipe.recipeid = recipe_like.recipeid
                left join recipe_img on recipe.recipeid = recipe_img.recipeid
                where recipe_search.recipe_vector @@ to_tsquery(%s)
                group by recipe_search.recipeid,recipe_search.title,recipe_search.description,recipe_search.ingredients,recipe_search.instructions,
                users.username,recipe_search.categories,recipe_img.image_data,recipe_img.image_link,users.userid
                order by like_count desc
            """
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


def getRecipePicture(recipeid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    img_str = "select image_data, image_link from recipe_img where recipeid = %s"
    try:
        cursor.execute(img_str,(recipeid,))
        result = cursor.fetchone()
        if result[0] is not None:
            return (result[0],"img")
        elif result[1] is not None:
            return (result[1],"link")
        else:
            return ("static/resources/lunch.jpg", "file")
    except:
        print("Failed to get recipe image")
        return None
    finally:
        cursor.close()
        connection.close()

# dict has keys: title,description, ingredients, instructions, userid, categories
# ingredients & instructions are lists of strings
def addRecipeToDB(dict):
    print("dict", dict)
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    str = "insert into recipe (title,description,ingredients,ingredients_nomeasure,instructions,userid,categories,recipe_vector) values (%s,%s,%s,%s,%s,%s,%s,to_tsvector(%s)) RETURNING recipeid"
    recipe_vector = dict["title"] + " " + dict["description"]
    ingredients_nomeasure = ""
    for ingredient in dict["ingredients"]:
        ingredients = ingredient.split(",")
        recipe_vector += " " + ingredients[1]
        ingredients_nomeasure += ingredients[1] + " "
    for category in dict["categories"]:
        recipe_vector += " " + category
    try:
        cursor.execute("select username from users where userid = %s", (dict["userid"],))
        username = cursor.fetchone()[0]
        recipe_vector += " " + username
        cursor.execute(str,(dict["title"],dict["description"],dict["ingredients"],ingredients_nomeasure,dict["instructions"],dict["userid"],dict["categories"],recipe_vector))
        recipeid = cursor.fetchone()[0]
        connection.commit()
        cursor.execute("refresh materialized view concurrently recipe_search")
        connection.commit()
    except Exception as e:
        print(f"Failed to add new recipe {e}")
        return None
    finally:
        cursor.close()
        connection.close()
        return recipeid

# dict has keys: title,description, ingredients, instructions, userid, categories
# ingredients & instructions are lists of strings
# imgfile is a file object of the image.
# This is NOT the LINK input for Minh's API
def addRecipeToDBWithImage(dict,imgfile):
    print("dict", dict)
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    imgfileRAW = imgfile.read()
    str = "insert into recipe (title,description,ingredients,ingredients_nomeasure,instructions,userid,categories,recipe_vector) values (%s,%s,%s,%s,%s,%s,%s,to_tsvector(%s)) returning recipeid"
    recipe_vector = dict["title"] + " " + dict["description"]
    ingredients_nomeasure = ""
    for ingredient in dict["ingredients"]:
        ingredients = ingredient.split(",")
        recipe_vector += " " + ingredients[1]
        ingredients_nomeasure += ingredients[1] + " "
        ingredient = ingredient.replace(",", " ")
    print("ingredients", dict["ingredients"])
    for category in dict["categories"]:
        recipe_vector += " " + category
    try:
        cursor.execute("select username from users where userid = %s", (dict["userid"],))
        username = cursor.fetchone()[0]
        recipe_vector += " " + username
        cursor.execute(str,(dict["title"],dict["description"],dict["ingredients"],ingredients_nomeasure,dict["instructions"],dict["userid"],dict["categories"],recipe_vector))
        
        # adding image to db
        new_recipe_ID = cursor.fetchone()[0]

        qstr_img = "insert into recipe_img (image_data, recipeid) values (%s,%s)"

        cursor.execute(qstr_img, (Binary(imgfileRAW),new_recipe_ID))

        cursor.execute("refresh materialized view concurrently recipe_search")
        connection.commit()
    except:
        print("Failed to add new recipe")
    finally:
        cursor.close()
        connection.close()

# dict has keys: content, recipeid, userid
def addCommentToDB(dict):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    query = """
    INSERT INTO recipe_comment (comment_time, comment_content, recipeid, userid)
    VALUES (%s, %s, %s, %s) RETURNING commentid;
    """
    try:
        cursor.execute(query, (dict["comment_time"], dict["comment"], dict["recipeid"], dict["userid"]))
        comment_id = cursor.fetchone()[0]
        print(f"comment id:{comment_id}")
        connection.commit()
    except Exception as e:
        print(f"Failed to add new recipe {e}")
        return None
    finally:
        cursor.close()
        connection.close()
        return comment_id

# Unsplash API Function - Adds recipe but uses unsplash to find a photo for it when User doesn't upload one
def addRecipeToDBWithImageURL(dict, img_url):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    str = "insert into recipe (title,description,ingredients,ingredients_nomeasure,instructions,userid,categories,recipe_vector) values (%s,%s,%s,%s,%s,%s,%s,to_tsvector(%s)) RETURNING recipeid"
    recipe_vector = dict["title"] + " " + dict["description"]
    ingredients_nomeasure = ""
    for ingredient in dict["ingredients"]:
        ingredients = ingredient.split(",")
        recipe_vector += " " + ingredients[1]
        ingredients_nomeasure += ingredients[1] + " "
    for category in dict["categories"]:
        recipe_vector += " " + category
    try:
        cursor.execute("select username from users where userid = %s", (dict["userid"],))
        username = cursor.fetchone()[0]
        recipe_vector += " " + username
        
        cursor.execute(str,(dict["title"],dict["description"],dict["ingredients"],ingredients_nomeasure,dict["instructions"],dict["userid"],dict["categories"],recipe_vector))
        
        # adding image to db
        new_recipe_ID = cursor.fetchone()[0] # How does this fetchone return a new_recipe_id?
        print("RecipeID AHH:", new_recipe_ID)
        qstr_img = "insert into recipe_img (image_link, recipeid) values (%s,%s)"

        cursor.execute(qstr_img, (img_url, new_recipe_ID))

        cursor.execute("refresh materialized view concurrently recipe_search")
        connection.commit()
    except Exception as e:
        print(f"Failed to add new recipe {e}")
        return False
    finally:
        cursor.close()
        connection.close()
        return new_recipe_ID

def setRecipeImage(recipeid, imgfile):
    if recipeid is None or imgfile is None:
        print("Recipe ID or image file is missing")
        return False

    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    imgfileRAW = imgfile.read()
    try:
        qstr = "insert into recipe_img (image_data,recipeid) values (%s,%s)"
        cursor.execute(qstr, (Binary(imgfileRAW), recipeid))
        connection.commit()
    except Exception as e:
        print(f"Failed to add image to recipe {e}")
        return False
    finally:
        cursor.close()
        connection.close()
        return True
    
def updateRecipeImage(recipeid, imgfile):
    if recipeid is None or imgfile is None:
        print("Recipe ID or image file is missing")
        return False

    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    imgfileRAW = imgfile.read()
    try:
        qstr = "update recipe_img set image_data = %s where recipeid = %s"
        cursor.execute(qstr, (Binary(imgfileRAW), recipeid))
        connection.commit()
    except Exception as e:
        print(f"Failed to update image to recipe {e}")
        return False
    finally:
        cursor.close()
        connection.close()
        return True
    
def getRecipePhoto(recipeid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    img_str = "select image_data, image_link from recipe_img where recipeid = %s"
    try:
        cursor.execute(img_str,(recipeid,))
        result = cursor.fetchone()
        if result[0] is not None:
            return (result[0],"img")
        elif result[1] is not None:
            print("Recipe link: " + result[1])
            return (result[1],"link")
        else:
            return ("static/resources/Logo.png", "file")
    except Exception as e:
        print("Failed to get user image, %s", e)
        return None
    finally:
        cursor.close()
        connection.close()

# dict has keys: title,description, ingredients, instructions,recipeid
def updateRecipeInDB(dict):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    recipe_vector = dict["title"] + " " + dict["description"]
    ingredients_nomeasure = ""
    for ingredient in dict["ingredients"]:
        ingredients = ingredient.split(",")
        recipe_vector += " " + ingredients[1]
        ingredients_nomeasure += ingredients[1] + " "
    for category in dict["categories"]:
        recipe_vector += " " + category
    # str was messing with str method :(
    qstr = "update recipe set title = %s, description = %s, ingredients = %s, ingredients_nomeasure = %s,instructions = %s,categories = %s, recipe_vector = to_tsvector(%s) where recipeid = %s"
    try:
        cursor.execute("select userid from recipe where recipeid = %s",(dict["recipeid"],))
        userid = cursor.fetchone()[0]
        userid = str(userid)
        cursor.execute("select username from users where userid = %s",(userid,))
        username = cursor.fetchone()[0]
        recipe_vector += " " + username
        cursor.execute(qstr,(dict["title"],dict["description"],dict["ingredients"], ingredients_nomeasure,dict["instructions"],dict["categories"],recipe_vector,dict["recipeid"]))
        connection.commit()
        cursor.execute("refresh materialized view concurrently recipe_search")
        connection.commit()
    except Exception as e:
        print("Failed to update recipe %s", e)
        return False
    finally:
        cursor.close()
        connection.close()
        return True;
    
def updateRecipeURL(recipeid, img_url):
    if recipeid is None or img_url is None:
        print("Recipe ID or image URL is missing")
        return False

    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    try:
        qstr = "update recipe_img set image_link = %s where recipeid = %s"
        cursor.execute(qstr, (img_url, recipeid))
        qstr = "update recipe_img set image_data = null where recipeid = %s"
        connection.commit()
    except Exception as e:
        print(f"Failed to update image to recipe {e}")
        return False
    finally:
        cursor.close()
        connection.close()
        return True

def deleteRecipeInDB(recipeid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if recipeid is None:
        return False
    try:
        str = "delete from recipe where recipeid = %s"
        cursor.execute(str, (recipeid,))
        connection.commit()
        cursor.execute("refresh materialized view concurrently recipe_search")
        connection.commit()
    except:
        print("Failed to delete recipe")
        return False
    finally:
        cursor.close()
        connection.close()
        return True

def getAllRecipes():
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    try:
        qstr = """select recipe.recipeid,recipe.title,recipe.description,recipe.ingredients,recipe.instructions,recipe.created_on,users.username,recipe.categories
        from recipe join users on recipe.userid = users.userid"""
        cursor.execute(qstr)
        result = cursor.fetchall()
        if result is not None:
            return result
        else:
            return []
    except:
        print("Failed to get all recipes")
        return []
    finally:
        cursor.close()
        connection.close()

def getAllRecipesCategory(category):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    try:
        qstr = """select recipe.recipeid,recipe.title,recipe.description,recipe.ingredients,recipe.instructions,recipe.created_on,users.username,recipe.categories
        from recipe join users on recipe.userid = users.userid
        where %s = any(recipe.categories)"""
        cursor.execute(qstr,(category,))
        result = cursor.fetchall()
        if result is not None:
            resultlst = []
            for i in range(len(result)):
                resultdict = {}
                for col in range(len(cursor.description)):
                    resultdict[cursor.description[col][0]] = result[i][col]
                resultlst.append(resultdict)
            return resultlst 
        else:
            return []
    except:
        print("Failed to get all recipes")
        return []
    finally:
        cursor.close()
        connection.close()

def getRecipeByID(recipeid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    try:
        qstr = """select recipe.recipeid,recipe.title,recipe.description,recipe.ingredients,recipe.instructions,recipe.created_on,users.username,recipe.userid,recipe.categories
        from recipe 
        join users on recipe.userid = users.userid
        where recipe.recipeid = %s"""
        cursor.execute(qstr,(recipeid,))
        result = cursor.fetchall()
        if result is not None:
            return result
        else:
            return []
    except:
        print("Failed to get all recipes")
        return []
    finally:
        cursor.close()
        connection.close()

def getRecipeLikes(recipeid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    if recipeid is None:
        return -1
    try:
        qstr = "select count(*) as likes from recipe_like where recipeid = %s"
        cursor.execute(qstr, (str(recipeid),))
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
        qstr = "select count(*) as comments from recipe_comment where recipeid = %s"
        cursor.execute(qstr, (str(recipeid),))
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
        qstr = "delete from recipe_like where likeid = %s"
        cursor.execute(qstr, (str(likeid),))
        connection.commit()
    except:
        print("Failed to delete recipe like")
    finally:
        cursor.close()
        connection.close()

def updateUserLikedStatus(recipeid,userid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    str = "insert into recipe_like (recipeid, userid) values(%s, %s)"
    try:
        cursor.execute("select * from recipe_like where userid = %s and recipeid = %s", (userid,recipeid))
        result = cursor.fetchone()
        if result is None:
            cursor.execute(str,(recipeid,userid))
            connection.commit()
            return "liked"
        else:
            cursor.execute("delete from recipe_like where userid = %s and recipeid = %s",(userid,recipeid))
            connection.commit()
            return "unliked"
    except:
        print("Failed to update recipe Like")
    finally:
        cursor.close()
        connection.close()
        
def checkLiked(userid,recipeid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    try:
        cursor.execute("select * from recipe_like where userid = %s and recipeid = %s", (userid,recipeid))
        result = cursor.fetchone()
        if result is None:
            return False
        else:
            return True
    except:
        print("Failed to check liked status")
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
        qstr = "delete from recipe_comment where commentid = %s"
        cursor.execute(qstr, (str(commentid),))
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
#recipe_saved functions
def updateUserSavedStatus(recipeid,userid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    str = "insert into recipe_saved (recipeid, userid) values(%s, %s)"
    try:
        cursor.execute("select * from recipe_saved where userid = %s and recipeid = %s", (userid,recipeid))
        result = cursor.fetchone()
        if result is None:
            cursor.execute(str,(recipeid,userid))
            connection.commit()
            return "saved"
        else:
            cursor.execute("delete from recipe_saved where userid = %s and recipeid = %s",(userid,recipeid))
            connection.commit()
            return "unsaved"
    except:
        print("Failed to update recipe saved")
    finally:
        cursor.close()
        connection.close()
        
def checkSaved(userid,recipeid):
    connection = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = connection.cursor()
    try:
        cursor.execute("select * from recipe_saved where userid = %s and recipeid = %s", (userid,recipeid))
        result = cursor.fetchone()
        if result is None:
            return False
        else:
            return True
    except:
        print("Failed to check saved status")
    finally:
        cursor.close()
        connection.close()

####################################################################################