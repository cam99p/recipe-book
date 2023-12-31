"""
A ingredients_category.py can sort the list of categories and the list of 
ingreidents by alphabetical. 

Team name: 3900-M14A-SICCC
Project Name: Project 1 - Recipe Recommendation System
Author: Cameron Khuu, Carla Phan, Christopher Tsang, Sylvia Huang, Xin Tian Luo
Date: 31/July/2022
"""
from src.helper import dbConnection


def sortingCategories():
    """ Sorting categories function to sort the list of categories 
        by alphabetically.
        
        Algorithm: linear search.

        The time complexity of the "for" loop is O(n). 
        
        Final Time Complexisty: O(n)

        Parameters:
            NONE
            
        Returns:
            categories (list): the list of categories after sorting
    """
    db = dbConnection()
    cur = db.cursor()
    qry = """
    select * 
    from categories
    order by name;
    """
    cur.execute(qry)
    info = cur.fetchall()
    cur.close()
    
    result = []
    for cate in info:
        cat, = cate 
        result.append(cat)

    return result


def sortingAllIngredients():
    """ Sorting ingredients function to sort the list of ingredients
        in all categories by alphabetically.

        Algorithm: linear search.

        The time complexity of the "for" loop is O(n). 

        Final Time Complexisty: O(n)

        Parameters:
            NONE
            
        Returns:
            ingredients (list): the list of ingredients after sorting
    """
    db = dbConnection()
    cur = db.cursor()
    qry = """
    select * 
    from ingredients
    order by categories, name;
    """
    cur.execute(qry)
    info = cur.fetchall()
    cur.close()
    
    result = []
    for ing in info:
        ingredient, = ing
        result.append(ingredient)

    return result


def sortingIngredients(cate):
    """ Sorting ingredients function to sort the list of ingredients
        in one category by alphabetically.

        Algorithm: linear search.

        The time complexity of the "for" loop is O(n). 

        Final Time Complexisty: O(n)

        Parameters:
            cate (str): the name of the categories

        Returns:
            ingredients (list): the list of ingredients after sorting
    """
    db = dbConnection()
    cur = db.cursor()
    qry = f"""
    select * 
    from ingredients
    where categories = %s
    order by name;
    """
    cur.execute(qry, [cate])
    info = cur.fetchall()
    cur.close()
    
    result = []
    for ing in info:
        veg, _, _, _ = ing 
        result.append(veg)
    
    return result
    
def sortIngredientsInCategories():
    """ Sorts all categories and ingredients in the categories and 
        returns a dictionary.
        
        Algorithm: linear search.

        The time complexity of the "for" loop is O(n). The time complexity of
        "sortingIngredients" is O(n). Thus, the overall of time complexity is
        O(n*n) = O(n^2).

        Final Time Complexisty: O(n^2)

        Parameters:
            NONE
            
        Returns:
            result (dict) : dictionary of all ingredients and categories sorted
    """
    result = {}
    listOfCategories = sortingCategories()
    for cate in listOfCategories:
        listOfIngredients = sortingIngredients(cate)
        result[cate] = listOfIngredients
    return result
