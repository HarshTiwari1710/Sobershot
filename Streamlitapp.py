import streamlit as st
import requests
import pandas as pd
import numpy as np
import random

# Set page configuration
st.set_page_config(page_title="SoberShot", page_icon="🍸", layout="wide")

# Custom CSS for enhanced styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f6f8f9 0%, #e5ebee 100%);
    color: #2c3e50;
}

/* Refined Button and Input Styles */
.stButton>button {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 25px;
    padding: 10px 20px;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background-color: #2980b9;
    transform: scale(1.05);
}

.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    border-radius: 15px;
    border: 2px solid #bdc3c7;
    padding: 12px;
    background-color: #ecf0f1;
    transition: border-color 0.3s ease;
}

.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
    border-color: #3498db;
    outline: none;
    box-shadow: 0 0 5px rgba(52, 152, 219, 0.5);
}

/* Enhanced Card Design */
.stCard {
    background-color: white;
    border-radius: 15px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin: 10px 0;
    transition: transform 0.3s ease;
}

.stCard:hover {
    transform: translateY(-5px);
}

/* Image Styling */
img {
    border-radius: 15px;
    border: 2px solid #e0e0e0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

img:hover {
    transform: scale(1.05);
}

/* Navigation Styling */
.stSidebar {
    background-color: #2c3e50;
    color: white;
}

.stSidebar .css-1d391kg, .stSidebar .css-1aumxhk {
    background-color: #34495e;
    color: white;
}

/* Typography */
.stMarkdown h1, .stMarkdown h2 {
    color: #2c3e50;
    font-weight: bold;
    border-bottom: 2px solid #3498db;
    padding-bottom: 10px;
}

/* Specific Caption Styling */
figcaption {
    color: #000000 !important; /* Change this color as needed */
}
/* Targeting the text input field */
    .stTextInput input {
        color: #3498db; /* Change the text color */
    }
    /* Targeting the label of the text input field for additional styling if needed */
    .stTextInput label {
        color: #3498db; 
    }
    .stTextArea label {
        color: #3498db;
    }

</style>
""", unsafe_allow_html=True)



API_BASE_URL = "https://sobershot.onrender.com"

def get_recommendations(drink_index=None, top_n=20):
    try:
        # Generate a random drink index if none is provided
        if drink_index is None:
            drink_index = random.randint(0, 100)  # Adjust max value based on your API's dataset size

        response = requests.post(
            f"{API_BASE_URL}/recommend",  # Ensure this endpoint is correctly set to accept POST with these parameters
            json={"drink_index": drink_index, "top_n": top_n}
        )
        response.raise_for_status()
        return response.json()["recommendations"]
    except Exception as e:
        # Log the error and return an empty list
        st.error(f"Error fetching recommendations: {e}")
        return []

def search_drinks(query):
    """Search for drinks via API"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/search", 
            params={"query": query}
        )
        response.raise_for_status()
        return response.json()["results"]
    except Exception as e:
        st.error(f"Error searching drinks: {e}")
        return []

def add_drink():
    """Page for adding a new drink"""
    st.title("Add a New Drink")
    
    with st.form("add_drink_form"):
        name = st.text_input("Drink Name")
        category = st.text_input("Category")
        ingredients = st.text_area("Ingredients (Comma-separated)")
        glass = st.text_input("Glass Type")
        instructions = st.text_area("Preparation Instructions")
        image_url = st.text_input("Image URL")
        
        submitted = st.form_submit_button("Add Drink")
        
        if submitted:
            try:
                ingredients_dict = {
                    f"ingredient_{i+1}": ing.strip() 
                    for i, ing in enumerate(ingredients.split(','))
                }
                
                payload = {
                    "name": name,
                    "category": category,
                    "ingredients": ingredients_dict,
                    "glass": glass,
                    "instructions": instructions,
                    "image": image_url
                }
                
                response = requests.post(f"{API_BASE_URL}/docs#/default/add_drink_add_drink_post", json=payload)
                response.raise_for_status()
                st.success("Drink added successfully!")
            except Exception as e:
                st.error(f"Error adding drink: {e}")

def search_page():
    """Page for searching drinks"""
    st.title("Drink Search")
    
    query = st.text_input("Search for drinks")
    
    if query:
        results = search_drinks(query)
        
        if results:
            st.write(f"Found {len(results)} drinks:")
            for drink in results:
                with st.container():
                    st.subheader(drink['name'])
                    st.write(f"**Category:** {drink.get('category', 'N/A')}")
                    st.write(f"**Glass:** {drink.get('glass', 'N/A')}")
                    if drink.get('image'):
                        st.image(drink['image'], width=200)
        else:
            st.warning("No drinks found.")

def home_page():
    """Home page with automatic recommendations"""
    st.title("Welcome to SoberShot 🍸")
    
    # Automatic recommendations on page load
    st.subheader("Featured Recommendations")
    
    # Assume the get_recommendations function fetches a list of drinks
    recommendations = get_recommendations()
    
    if recommendations:
        # Dynamic column layout based on the number of recommendations
        cols = st.columns(len(recommendations))
        for i, drink in enumerate(recommendations):
            with cols[i]:
                # Create a card for each drink
                st.image(drink.get('image', 'https://via.placeholder.com/200'), width=200)
                st.markdown(f"<p style='color:#000000; text-align:center; margin-bottom:10px;'>{drink['name']}</p>", unsafe_allow_html=True)
                with st.expander("Details"):
                    st.markdown(f"**Category:** {drink.get('category', 'N/A')}")
                    st.markdown("**Ingredients:**")
                    # Assuming ingredients are returned as a list
                    ingredients = drink.get('ingredients', [])
                    for ingredient in ingredients:
                        st.write(f"- {ingredient}")
                    st.markdown(f"**Glass:** {drink.get('glass', 'N/A')}")
                    st.markdown(f"**Instructions:** {drink.get('instructions', 'N/A')}")
    else:
        st.warning("No recommendations available at the moment.")


def main():
    """Main app navigation"""
    st.sidebar.title("SoberShot Navigation")
    
    page = st.sidebar.radio("Go to", 
        ["Home", "Search Drinks", "Add a Drink"]
    )
    
    if page == "Home":
        home_page()
    elif page == "Search Drinks":
        search_page()
    else:
        add_drink()

if __name__ == "__main__":
    main()