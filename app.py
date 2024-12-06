from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from pymongo import MongoClient
import pandas as pd
import numpy as np
import tensorflow as tf
import json
import pickle

app = FastAPI()

MONGO_URL = "mongodb+srv://harsh:1234@sobershot.rj7jt.mongodb.net/?retryWrites=true&w=majority&appName=SoberShot"
client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=50000)
db = client["drinks"]  # Database name
collection = db["drinks_data"]

# Load pre-trained model and data
model_path = "beverage_recommendation_model.h5"  # Path to your trained Keras model
data_path = "drinks_df.pkl"

try:
    # Load the Keras model
    model = tf.keras.models.load_model(model_path)
    
    # Load the drinks DataFrame
    with open(data_path, "rb") as file:
        drinks_df = pickle.load(file)
        
    # Load feature matrix (preprocessed data)
    feature_matrix_path = "feature_matrix.npy"
    feature_matrix = np.load(feature_matrix_path)
    
except Exception as e:
    raise RuntimeError(f"Failed to load model or data: {e}")


class AddDrinkRequest(BaseModel):
    name: str
    category: str
    ingredients: Dict[str, str]
    glass: str
    instructions: str
    image: str
# Define input schema for API
class RecommendRequest(BaseModel):
    drink_index: int  # Index of the drink for recommendations
    top_n: Optional[int] = 10# Number of recommendations to return (default: 5)

# Endpoint to check API status
@app.get("/")
def root():
    return {"message": "Beverage Recommendation API is running!"}

@app.post("/add-drink")
def add_drink(drink: AddDrinkRequest):
    """
    Add a new drink to the MongoDB database.
    """
    # Check if drink already exists
    if collection.find_one({"name": drink.name}):
        raise HTTPException(status_code=400, detail="Drink already exists")

    # Prepare the drink data
    drink_data = {
        "name": drink.name,
        "category": drink.category,
        "ingredients": drink.ingredients,
        "glass": drink.glass,
        "instructions": drink.instructions,
        "image": drink.image  # Image is stored as a string
    }

    # Insert the drink into the collection
    result = collection.insert_one(drink_data)

    # Add the inserted document's ID to the response
    drink_data["_id"] = str(result.inserted_id)

    return {"message": "Drink added successfully", "drink": drink_data}

@app.get("/search")
def search_drinks(query: str):
    """
    Search for drinks by name or category.
    """
    # Search for matching documents
    results = list(collection.find({"$or": [
        {"name": {"$regex": query, "$options": "i"}},
        {"category": {"$regex": query, "$options": "i"}}
    ]}))

    if not results:
        raise HTTPException(status_code=404, detail="No drinks found matching your query")
    
    # Format the results to match the desired structure
    formatted_results = []
    for result in results:
        formatted_result = {
            "name": result.get("name"),
            "category": result.get("category"),
            "ingredients": result.get("ingredients", {}),  # Default to an empty dict if missing
            "glass": result.get("glass"),
            "instructions": result.get("instructions"),
            "image": result.get("image", "")  # Default to an empty string if missing
        }
        formatted_results.append(formatted_result)

    # Debug step: Log the formatted results
    print("Formatted Results:", formatted_results)
    
    return {"results": formatted_results}

# Recommendation endpoint
@app.post("/recommend")
def recommend_drinks(request: RecommendRequest):
    try:
        drink_index = request.drink_index
        top_n = request.top_n
        
        # Predict similarities using the model
        similarities = model.predict(feature_matrix)
        drink_similarities = similarities[drink_index]
        
        # Get indices of the most similar drinks (excluding the drink itself)
        similar_indices = np.argsort(-drink_similarities)[1:top_n + 1]
        
        # Fetch details for recommended drinks
        recommended_drinks = drinks_df.iloc[similar_indices]
        recommendations = []
        
        for _, drink in recommended_drinks.iterrows():
            drink_details = {
                "name": drink.get("name"),
                "category": drink.get("category"),
                "ingredients": drink.get("ingredient_dict"),
                "glass": drink.get("glass"),
                "instructions": drink.get("instructions"),
                "image": drink.get("Image")
            }
            recommendations.append(drink_details)
        
        return {"recommendations": recommendations}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")