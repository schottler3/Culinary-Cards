import dbinteractions as db
import random
usedRecipes = []
recipeOfTheDay = ()
def setRecipeOfTheDay():
    global recipeOfTheDay, usedRecipes
    all_recipes = db.getAllRecipes()
    all_recipeslen = len(all_recipes)
    if(all_recipeslen == 0):
        recipeOfTheDay = ("No recipes found", "No recipes found", "No recipes found", "No recipes found")
        return
    randindex = random.randint(0,all_recipeslen-1)
    if len(usedRecipes) >= all_recipeslen-3:
        usedRecipes = []
    while all_recipes[randindex][0] in usedRecipes:
        print(all_recipes[randindex])
        randindex = random.randint(0,all_recipeslen-1)
    usedRecipes.append(all_recipes[randindex][0])
    recipeOfTheDay = all_recipes[randindex]
    ingredientstr = ""
    for ingredient in recipeOfTheDay[3]:
        ingredientstr += ingredient.split(",")[0] + ", "
    ingredientstr = ingredientstr[:-2:]
    recipeOfTheDay = list(recipeOfTheDay)
    recipeOfTheDay[3] = ingredientstr
    recipeOfTheDay = tuple(recipeOfTheDay)

def getRecipeOfTheDay():
    return recipeOfTheDay