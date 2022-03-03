from flask_app import app

from flask import render_template, redirect, request, session, flash

from flask_app.models.user import User

from flask_app.models.recipe import Recipe

@app.route('/recipes')
def recipes():
    if 'user_id' not in session:
        return redirect('/')
    # get all recipes from database
    recipes = Recipe.get_all_recipes()
    print(recipes)
    for i in recipes:
        if i.under_30 == 1:
            i.under_30 = "yes"
        else: i.under_30 = "No"
    return render_template('recipes.html', recipes = recipes)

@app.route('/recipes/new')
def new_recipe():
    
    return render_template('new_recipe.html')

@app.route('/recipes/create', methods = ['POST'])
def create_recipes():
    # validate data
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    # then create recipes
    data = {
        'name': request.form['recipe_name'],
        'description': request.form['recipe_description'],
        'instructions': request.form['recipe_instructions'],
        'under_30': request.form['under_30'],
        'date': request.form['recipe_date'],
        'user_id': session['user_id']
    }
    Recipe.create_recipe(data)
    return redirect('/recipes')

@app.route('/recipes/<int:recipe_id>')
def single_recipe(recipe_id):

    data = {
        'id': recipe_id
    }
    
    recipe = Recipe.get_recipe_by_id(data)
    return render_template('/single_recipe.html', recipe = recipe)

@app.route('/recipes/<int:recipe_id>/edit')
def edit_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    
    recipe = Recipe.get_recipe_by_id(data)
    
    if session['user_id'] != recipe.user.id:
        return redirect('/recipes')
    
    print(type(recipe.date))
    recipe.date = str(recipe.date)[0:10]
    return render_template('/recipe_edit.html', recipe = recipe)

@app.route('/recipes/<int:recipe_id>/update', methods =['POST'])
def update_recipe(recipe_id):
    
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/{recipe_id}/edit')
    
    else:
        data = {
            'recipe_id': recipe_id,
            'recipe_name': request.form['recipe_name'],
            'recipe_description': request.form['recipe_description'],
            'recipe_instructions': request.form['recipe_instructions'],
            'recipe_date': request.form['recipe_date'],
            'recipe_under_30': request.form['recipe_under_30'],
        }
    
        Recipe.update_recipe(data)
        return redirect(f'/recipes/{recipe_id}')
    
@app.route("/recipes/<int:recipe_id>/delete")
def delete_recipe(recipe_id):
    data = {
        "id": recipe_id
    }
    
    Recipe.delete_recipe(data)
    return redirect("/recipes")
