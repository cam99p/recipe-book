from src.caloriesRecipes import getCaloriesRecipes, calorieCalculation
import pytest


def test_simple_calories_match():
    calories = 360
    assert len(getCaloriesRecipes(calories, "", "", [])) == 11

def test_simple_calories_ingredients_mealType_match():
    ingredients = ['olive oil', 'bacon', 'egg']
    calories = 723
    mealType = "breakfast"
    assert len(getCaloriesRecipes(calories, ingredients, mealType, [])) == 0
    
def test_no_calories_match():
    calories = 10
    assert len(getCaloriesRecipes(calories, "", "", [])) == 1

def test_no_calories_ingredients_mealType_match():
    ingredients = ['olive oil', 'bacon', 'egg']
    calories = 700
    mealType = "dinner"
    assert len(getCaloriesRecipes(calories, ingredients, mealType, [])) == 0

def test_minimal_calories_match():
    calories = 99
    assert len(getCaloriesRecipes(calories, "", "", [])) == 5

def test_minimal_calories_ingredients_mealType_match():
    ingredients = ['bacon']
    calories = 99
    mealType = "Dinner"
    assert len(getCaloriesRecipes(calories, ingredients, mealType, [])) == 0

def test_multiple_calories_match():
    calories = 10000
    assert len(getCaloriesRecipes(calories, "", "", [])) == 27

def test_calorieCalc_normal():
    ingredientsDict = {"olive oil": "3g",  "bacon": "100g", "egg": 2}
    assert calorieCalculation(ingredientsDict) == 660


def test_multiple_calories_ingredients_mealType_match():
    ingredients = ['bacon', 'egg', 'flour', 'thyme', 'avocado']
    calories = 10000
    mealType = "Breakfast"
    assert len(getCaloriesRecipes(calories, ingredients, mealType, [])) == 10