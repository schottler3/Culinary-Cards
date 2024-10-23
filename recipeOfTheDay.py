import dbinteractions as db
import random
from datetime import datetime
recipeOfTheDay = ()
#https://stackoverflow.com/questions/620305/convert-year-month-day-to-day-of-year-in-python
def setRecipeOfTheDay():
    global recipeOfTheDay
    all_recipes = db.getAllRecipes()
    all_recipeslen = len(all_recipes)
    if all_recipeslen > 0:
        randindex = datetime.now().timetuple().tm_mday % all_recipeslen
        recipeOfTheDay = all_recipes[randindex]
        ingredientstr = ""
        for ingredient in recipeOfTheDay[3]:
            ingredientstr += ingredient.split(",")[1] + ", "
        ingredientstr = ingredientstr[:-2:]
        recipeOfTheDay = list(recipeOfTheDay)
        recipeOfTheDay[3] = ingredientstr
        recipeOfTheDay = tuple(recipeOfTheDay)

def getRecipeOfTheDay():
    return recipeOfTheDay