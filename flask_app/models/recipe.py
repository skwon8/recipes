from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

from flask_app.models.user import User

# ============================================
# Recipe class
# ============================================


class Recipe():

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None

# ============================================
# Creating Recipe
# ============================================
    @classmethod
    def create_recipe(cls, data):

        query = "INSERT INTO recipes (name, description, instructions, under_30, date, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under_30)s, %(date)s, %(user_id)s);"

        result = connectToMySQL("recipes").query_db(query, data)

        return result

# ============================================
# Get all Recipes to main page
# ============================================
    @classmethod
    def get_all_recipes(cls):

        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"

        results = connectToMySQL("recipes").query_db(query)

        recipes = []

        for item in results:
            new_recipe = Recipe(item)

            user_data = {
                'id': item['users.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'password': item['password'],
                'created_at': item['users.created_at'],
                'updated_at': item['users.updated_at'],
            }

            new_recipe.user = User(user_data)

            recipes.append(new_recipe)

        return recipes

# ============================================
# Show Recipe to User
# ============================================
    @classmethod
    def get_recipe_by_id(cls, data):

        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"

        result = connectToMySQL("recipes").query_db(query, data)

        recipe = Recipe(result[0])

        user_data = {
            'id': result[0]['users.id'],
            'first_name': result[0]['first_name'],
            'last_name': result[0]['last_name'],
            'email': result[0]['email'],
            'password': result[0]['password'],
            'created_at': result[0]['users.created_at'],
            'updated_at': result[0]['users.updated_at'],
        }
        
        recipe.user = User(user_data)

        return recipe
    
# ============================================
# Updating Recipes
# ============================================
    @classmethod
    def update_recipe(cls, data):
        
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30 = %(under_30)s, date = %(date)s WHERE id = %(recipe_id)s;"
        
        result = connectToMySQL("recipes").query_db(query, data)
        
# ============================================
# Delete Recipes
# ============================================
    @classmethod
    def delete_recipe(cls, data):
        
        query = "DELETE FROM recipes WHERE id = %(id)s;"

        result = connectToMySQL("recipes").query_db(query, data)

# ============================================
# Staticmethod for Creating Recipes
# ============================================
    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data['recipe_name']) < 3:
            is_valid = False
            flash("Recipe name must be at least 3 characters long.")

        if len(data['recipe_description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters long.")

        if len(data['recipe_instructions']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters long.")

        if "under_30" not in data:
            flash("You have to choose yes or no.")
            is_valid = False

        if data['recipe_date'] == '':
            is_valid = False
            flash("Recipe Date CANNOT be Blank!")

        return is_valid
