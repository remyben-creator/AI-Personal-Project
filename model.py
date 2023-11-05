## most likely where I put most of the ai components
import os
import openai
import json
import random

import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_batch

#for another time once I train my own personal model
from pathlib import Path

#from langchain.chat_models import ChatOpenAI
#from langchain.schema import HumanMessage, AIMessage, ChatMessage


openai.api_key = os.environ.get("OPENAI_API_KEY")
# Define the path to the JSON file
json_directory = Path("C:\\Users\\Benjamin\\Desktop\\Personal Coding Projects\\AI Recipe App\\Training")

# Database parameters
db_params = {
    'dbname': 'recipes_db',
    'user': 'postgres',
    'password': 'Ben210remy',
    'host': 'localhost'
}

'''
# Connect to the database
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

insert_query = sql.SQL("""
    INSERT INTO recipes (title, ingredients, instructions) VALUES (%s, %s, %s)
""")

# This list will store all tuples to insert
data_to_insert = []

# Iterate over JSON files and insert data
for json_file in json_directory.glob("*.json"):
    with open(json_file, "r") as f:
        data = json.load(f)

        for recipe in data.values():
            # Ensure that 'title', 'ingredients', and 'instructions' are present
            if all(key in recipe for key in ['title', 'ingredients', 'instructions']):
                if recipe['title'] != None and recipe['ingredients'] != None and recipe['instructions'] != None:
                    data_to_insert.append((recipe['title'], recipe['ingredients'], recipe['instructions']))
                
                # data_to_insert.append((recipe['title'], recipe['ingredients'], recipe['instructions']))

try:
    psycopg2.extras.execute_batch(cur, insert_query, data_to_insert)
    conn.commit()
except Exception as e:
    print(f"An error occurred: {e}")
    conn.rollback()

# Close communication with the database
cur.close()
conn.close()


# Connect to your database
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Query to select rows from your table
cur.execute("SELECT * FROM recipes LIMIT 10;")

# Fetch the results
results = cur.fetchall()

for row in results:
    print(row)

# Close communication with the database
cur.close()
conn.close()
'''


class Model:
    # variables
    # function descriptions
    function_descriptions = [
        {
            "name": "get_random_recipe",
            "description": "Give an a random recipe based on one pulled from the database",
            "parameters": {
                "type": "object",
                "properties": {
                    #array of strings
                    "ingredients": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "A type of food e.g. carrots",
                            },
                        "description": "A list of food ingredients e.g. ['carrots', 'meat', 'skittles']",
                    },
                },
                "required": ["ingredients"],
            },
        },
        {
            "name": "more_recipe_info",
            "description": "Give more info based on one pulled from the database",
            "parameters": {
                "type": "object",
                "properties": {
                    #array of strings
                    "question": {
                        "type": "string",
                        "description": "A question about the dish e.g. what is the estimated prep time?",
                    },
                },
                "required": ["question"],
            },
        }
    ]

    def __init__(self):
        self = self
    
    def generate_response(self, user_message):
        #what the view class calls
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                },
            ],

            functions = self.function_descriptions,
            function_call = "auto", 

        )

        output = completion.choices[0].message

        return output
    
    def more_recipe_info(self, question):
        "Give more info based on one pulled from the database"
        recipe_info = {
            "question": question
        }

        return json.dumps(recipe_info)
    
    def get_random_recipe(self, ingredients):
        """Give an a random recipe based on one pulled from the database"""
            
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Query to find recipes that have any of the user's ingredients
        # Start with the base of the query
        query_base = """
        SELECT * FROM recipes 
        WHERE 
        """

            # Generate the condition for each ingredient
        conditions = []
        for ingredient in ingredients:
            condition = f"EXISTS (SELECT 1 FROM UNNEST(ingredients) AS ingredient WHERE ingredient LIKE %s)"
            conditions.append(condition)
            
        # Placeholder values to match with LIKE conditions
        like_placeholders = [f"%{ingredient}%" for ingredient in ingredients]
        print(like_placeholders)
        # Join all conditions with 'AND'
        query_conditions = ' AND '.join(conditions)

        # Final query
        final_query = query_base + query_conditions

        # Execute the query
        cur.execute(final_query, (like_placeholders))

        # Fetch the matching recipes
        matching_recipes = cur.fetchall()

        if matching_recipes:
            random_recipe = random.choice(matching_recipes)
        else:
            random_recipe = "Sorry no matching recipes!"

        # Close communication with the database
        cur.close()
        conn.close()
            
        recipe_info = {
            "ingredients": ingredients,
            "matching_recipes": random_recipe
        }

        return json.dumps(recipe_info)
    

    def make_object(self, output):
        ingredients = json.loads(output.function_call.arguments).get("ingredients")
        params = json.loads(output.function_call.arguments)
        type(params)


        chosen_function = eval('self.' + output.function_call.name)

        full_recipe = chosen_function(**params)

        return full_recipe
    
    def generate_response2(self, output, content, user_message):
        second_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                },
                {
                    "role": "function",
                    "name": output.function_call.name,
                    "content": content
                },
            ],
            functions= self.function_descriptions,
        )
        response = second_completion.choices[0].message.content
        
        return response