"""
A recipe.py can return the list of recipes which are matched the ingreidents
that selected by the users. If the user has a blacklist of ingredients, the
system also can filter the recipes. The system also can provide some 
suggestions with the ingredients which are depended on the user selected 
the ingredients. 

Team name: 3900-M14A-SICCC
Project Name: Project 1 - Recipe Recommendation System
Author: Cameron Khuu, Carla Phan, Christopher Tsang, Sylvia Huang, Xin Tian Luo
Date: 31/July/2022
"""
from src.helper import dbConnection, retrieveRecipe, retrieveRecipeList

def recipeMatch(ingredientsList, blacklist):
    """ Sends front end a list of recipes that satisfy the list 
        of ingredients that the user selected by alphabetically.

        Algorithm: linear search. 
        
        The time complexity of "if" statement is O(1) and the time complexity
        of "for" loop is O(n). 

        The time complexity of "dbConnection" is O(1) and the time comlexity 
        of "retrieveRecipeList" is O(n).
        
        Thus, O(n*n*n) = O(n^3).

        Final Time Complexisty: O(n^3)

        Parameters:
            ingredientsList (str): list of ingredients user selected
            blacklist (list): list of blacklisted ingredients

        Return:
            recipeList (list): list of recipes id's satisfying the ingredients
    """
    recipeList = []
    db = dbConnection()
    info = retrieveRecipeList(db)
    if blacklist != []:
        info = getFilteredRecipes(info, blacklist)
    for recipe in info:
        ingredientString = recipe[8]
        ingredients = ingredientString.split(', ')
        missingIngList = ingredients.copy()
        matching = 0
        for i in ingredientsList:
            for j in ingredients:
                if i in j:
                    matching += 1
                    missingIngList.remove(j)
        if matching == len(ingredients) or matching == len(ingredients) - 1:
            missingIng = ''
            partialMatch = False
            if matching == len(ingredients) - 1:
                ing = missingIngList.pop()
                ing = ing.split(' ')
                ing.pop(0)
                missingIng = " ".join(ing)
                partialMatch = True
            ingDict = {
                    "recipeID": recipe[0],
                    "title": recipe[7],
                    "servings": recipe[1],
                    "timeToCook": recipe[2],
                    "mealType": recipe[3],
                    "photo": recipe[4],
                    "calories": recipe[5],
                    "cookingSteps": recipe[6],
                    "ingredients": recipe[8],
                    "missingIngredient": missingIng,
                    "partialMatch": partialMatch,
            }
            recipeList.append(ingDict)

    return recipeList


def getFilteredRecipes(recipes, blacklist):
    """ Helper function for recipeMatch.

        Algorithm: linear search.

        The time complexity of the "for" loop is O(n). The time complexisty
        of "RecipeHasBlacklist" is O(n^2). Thus, O(n^2*n) = O(n^3).
        
        Final Time Complexisty: O(n^3)

        Parameters: 
            recipes (list): list of all existing recipes 
            blacklist (list): list of blacklisted ingredients user selected
    
        Return:
            recipeList (list): list of recipes without ingredients from 
                        blacklist
"""
    filteredRecipeList = []
    for recipe in recipes:
        ingredientString = recipe[8]
        ingredients = ingredientString.split(',')
        if RecipeHasBlacklist(ingredients, blacklist) is False:
            filteredRecipeList.append(recipe)
    return filteredRecipeList


def RecipeHasBlacklist(recipe, blacklist):
    """Helper function for getFilteredRecipes.

        Algorithm: linear search.

        The time complexity of the "for" loop is O(n). There are two "for"
        loop, so O(n*n) = O(n^2).
        
        Final Time Complexisty: O(n^2)

        Parameters:
            recipe(list): list of ingredients in recipe 
            blacklist (list): list of blacklisted ingredients user selected
    
        Return:
            recipeList (boolean): true if recipe contains any blacklisted 
                    ingredient, false otherwise 
    """
    for ingredient in recipe:
        for unwanted in blacklist:
            if unwanted in ingredient:
                return True
    return False


def recipeDetails(recipeID):
    """ Retrieves recipe details by given a recipe id.

        Algorithm: No algorithm.

        The time complexity of the "retrieveRecipe" is O(n). 
        
        Final Time Complexisty: O(n)

        Parameters:
            recipeID (int): recipe id as an integer

        Returns:
            dict {
                recipeID (int): id of recipe
                title (str): title of recipe
                servings (int): serving size of recipe
                timeToCook (int): cooking time
                mealType (str): meal type
                photo (binary): photo of meal
                calories (int): calories of meal
                cookingSteps (str): cooking steps of recipe
                ingredients (str): ingredients of recipe
            }
    """
    db = dbConnection()
    info = retrieveRecipe(db, recipeID)

    return {
        "recipeID": info[0],
        "title": info[7],
        "servings": info[1],
        "timeToCook": info[2],
        "mealType": info[3],
        "photo": info[4],
        "calories": info[5],
        "cookingSteps": info[6],
        "ingredients": info[8]
    }


def ingredientsSuggestions(ingredientsList, blacklist):
    """ Sends front end a list of ingredients that satisfy the list 
        of ingredients that the user selected by top five ingredients
        in specific conditions. If the user did not select any ingredients,
        the system will not return any ingredients.

        1. If there are at least one ingredients in the blacklist, this recipe
           will not be considered and these ingredients will not show in the 
           the list of ingreidents' suggestion.
        2. The most frequency ingredients in all recipes which do not include
           the ingredients in the user's selection ingredients list.
        3. If the previous condition is matched and get the same frequency for
           some ingredients, the ingredients will be ordered by alphabetical. 

        Algorithm: linear search.

        The time complexity of the "for" loop is O(n). There are two "for"
        loop, so it is O(n^2). The time complexisty of sorting dictionary
        is O(n^2). The time complexisty of 
        "getIngredientsSuggestions" is also O(n^2). 
        
        Final Time Complexisty: O(n^2)

        Parameters:
            ingredientsList (str): list of ingredients user selected
            blacklist (list): blacklist of ingredients user selected

        Return:
            getIngredientsSuggestions (list): list of ingredients are 
                            satisfying the ingredients from the 
                            getIngredientsSuggestions function
    """
    num_select = len(ingredientsList)
    if num_select < 1:
        return []
    db = dbConnection()
    info = retrieveRecipeList(db)
    igds_frequency = {}
    for recipe in info:
        ingredients = [" ".join(i.split(' ')[1:]) \
                            for i in recipe[8].split(', ')]
        match = 0
        missing_igds = []
        for igd in ingredients:
            if igd in ingredientsList:
                match += 1
            elif len(blacklist) > 0 and igd in blacklist:
                match = 0
                missing_igds = []
                break
            else:
                missing_igds.append(igd)
        if match == num_select:
            for miss in missing_igds:
                if len(igds_frequency) > 0 and \
                    igds_frequency.get(miss) is not None:
                        igds_frequency[miss] = igds_frequency[miss] + 1
                else:
                    igds_frequency[miss] = 1

    igds_frequency_sort = sorted(igds_frequency.items(), 
                        key=lambda kv: kv[1], reverse=True)
    return getIngredientsSuggestions(igds_frequency_sort, len(info))


def getIngredientsSuggestions(igds_frequency_sort, pre_frequency):
    """Helper function for ingredientsSuggestions. To select the top 5 
       ingredients and return to the frontend.

        Algorithm: linear search.

        The time complexity of the "for" loop is O(n). There is two "for"
        loop, so the time complexisty is O(n^2).
        
        Final Time Complexisty: O(n^2)

        Parameters:
            igds_frequency_sort (list): list of suggestion ingredients
            pre_frequency (int): the maximum number of frequency
        
        Return:
            igds_suggestions (list): list of top 5 suggestion ingreidents
    """
    igdsSuggestions = []
    tmp_igds = []  
    for igds, fqy in igds_frequency_sort:
        if len(igdsSuggestions) >= 5:
            break
        if len(tmp_igds) == 0:
            tmp_igds.append(igds)
            pre_frequency = fqy 
        else:
            if pre_frequency == fqy:
                tmp_igds.append(igds)
            else:
                tmp_igds_sort = sorted(tmp_igds)
                for item in tmp_igds_sort:
                    if len(igdsSuggestions) < 5:
                        igdsSuggestions.append(item)
                    else:
                        break
                tmp_igds = [igds]
                pre_frequency = fqy
    
    if len(igdsSuggestions) < 5:
        tmp_igds_sort = sorted(tmp_igds)
        igdsSuggestions = igdsSuggestions + \
            tmp_igds_sort[:5-len(igdsSuggestions)]
    
    return igdsSuggestions