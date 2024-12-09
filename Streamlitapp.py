import streamlit as st
import requests
import random
from typing import List, Dict, Any
from together import Together

# UI Components (Simulated ShadCN-like components)
class UIComponents:
    @staticmethod
    def card(title: str, content: str = None, details: Dict[str, Any] = None, image_url: str = None):
        """Create a card-like component"""
        # Prefer details if provided, otherwise use content
        display_content = content if not details else "\n".join(f"{key}: {value}" for key, value in details.items())
        html_content = f"""
        <div style="
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        background-color: white;">
        {f'<img src="{image_url}" style="max-width:100%; border-radius:8px; margin-bottom:10px;">' if image_url else ''}
        <h3 style="margin-bottom: 10px; color: #2c3e50;">{title}</h3>
        <p style="color: #34495e; margin-bottom: 5px;">Category: {details.get("Category", "N/A")}</p>
        <p style="color: #34495e; margin-bottom: 5px;">Glass: {details.get("Glass", "N/A")}</p>
        <p style="color: #34495e; margin-bottom: 5px;">Ingredients: {details.get("Ingredients", "N/A")}</p>
        <p style="color: #34495e;">Instructions: {details.get("Instructions", "N/A")}</p>
    """
        st.markdown(html_content, unsafe_allow_html=True)

    @staticmethod
    def input_field(label: str, key: str, placeholder: str = ""):
        """Create a styled input field"""
        return st.text_input(
            label, 
            key=key, 
            placeholder=placeholder,
            help=f"Enter {label.lower()}",
        )

    @staticmethod
    def action_button(label: str, on_click=None):
        """Create a styled action button"""
        return st.button(
            label, 
            help=f"Click to {label.lower()}",
            on_click=on_click
        )

class SoberShotApp:
    API_BASE_URL = "https://sobershot.onrender.com"
    TOGETHER_API_KEY = "3e1098274c44435facf8613000c684fa9f77865c52fea11958e2f59391a4407b"

    @classmethod
    def get_recommendations(cls, drink_index: int = None, top_n: int = 20) -> List[Dict[str, Any]]:
        """Fetch drink recommendations"""
        try:
            drink_index = drink_index or random.randint(0, 100)
            response = requests.post(
                f"{cls.API_BASE_URL}/recommend",
                json={"drink_index": drink_index, "top_n": top_n}
            )
            response.raise_for_status()
            return response.json().get("recommendations", [])
        except Exception as e:
            st.error(f"Recommendation error: {e}")
            return []

    @classmethod
    def search_drinks(cls, query: str) -> List[Dict[str, Any]]:
        """Search for drinks"""
        try:
            response = requests.get(
                f"{cls.API_BASE_URL}/search", 
                params={"query": query}
            )
            response.raise_for_status()
            return response.json().get("results", [])
        except Exception as e:
            st.error(f"Search error: {e}")
            return []

    @classmethod
    def get_cocktail_suggestion(cls, ingredients: str) -> str:
        """Generate cocktail suggestion using Together.ai"""
        try:
            client = Together(api_key=cls.TOGETHER_API_KEY)
            response = client.chat.completions.create(
                model="meta-llama/Llama-3-70b-chat-hf",
                messages=[{
                    "role": "user", 
                    "content": f"Suggest a cocktail recipe using: {ingredients}"
                }],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content if response.choices else "No suggestion"
        except Exception as e:
            return f"Suggestion error: {e}"

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="SoberShot 🍸", 
        page_icon="🍸", 
        layout="wide"
    )

    # Sidebar Navigation
    st.sidebar.title("SoberShot Menu")
    page = st.sidebar.radio(
        "Navigate", 
        ["Home", "Search Drinks", "Add Drink", "Cocktail Suggester"]
    )

    # Page Routing
    if page == "Home":
        home_page()
    elif page == "Search Drinks":
        search_page()
    elif page == "Add Drink":
        add_drink_page()
    else:
        cocktail_suggester_page()

def home_page():
    """Home page with drink recommendations."""
    st.title("SoberShot: Your Cocktail Companion 🍸")
    recommendations = SoberShotApp.get_recommendations()
    for drink in recommendations:
        ingredients = drink.get('ingredients', {})
        # Format ingredients and their measurements
        formatted_ingredients = ', '.join(f"{ingredient}: {measure}" for ingredient, measure in ingredients.items()) if ingredients else 'N/A'
        
        details = {
            "Category": drink.get('category', 'N/A'),
            "Glass": drink.get('glass', 'N/A'),
            "Ingredients": formatted_ingredients,
            "Instructions": drink.get('instructions', 'N/A')
        }
        UIComponents.card(
            title=drink.get('name', 'Unknown Cocktail'),
            details=details,
            image_url=drink.get('image', 'https://via.placeholder.com/200')
        )

def search_page():
    """Drink search page."""
    st.title("Cocktail Search")
    query = UIComponents.input_field("Search Drinks", "search_query", "Enter cocktail name")
    if UIComponents.action_button("Search"):
        results = SoberShotApp.search_drinks(query)
        if not results:
            st.warning("No drinks found.")
        else:
            for drink in results:
                ingredients = drink.get('ingredients', 'N/A')  # Default to 'N/A' if missing
                # Check if ingredients is a dictionary and format accordingly
                if isinstance(ingredients, dict):
                    formatted_ingredients = ', '.join(f"{ingredient}: {measure}" for ingredient, measure in ingredients.items())
                else:
                    formatted_ingredients = ingredients  # Use the string directly if not a dict

                details = {
                    "Category": drink.get('category', 'N/A'),
                    "Glass": drink.get('glass', 'N/A'),
                    "Ingredients": formatted_ingredients,
                    "Instructions": drink.get('instructions', 'N/A')
                }
                UIComponents.card(
                    title=drink.get('name', 'Unnamed Cocktail'),
                    details=details,
                    image_url=drink.get('image', 'https://via.placeholder.com/200')
                )


import json

def add_drink_page():
    """Page to add new drinks"""
    st.title("Add a New Cocktail")
    
    with st.form("add_drink_form"):
        name = UIComponents.input_field("Drink Name", "new_drink_name")
        category = UIComponents.input_field("Category", "drink_category")
        ingredients = st.text_area("Ingredients (JSON format)", key="drink_ingredients")
        glass = UIComponents.input_field("Glass Type", "drink_glass")
        instructions = st.text_area("Instructions", key="drink_instructions")
        image = st.text_area("Image URL", key="drink_image")
        
        submitted = st.form_submit_button("Add Cocktail")
        
        if submitted:
            # Try to parse ingredients as JSON
            try:
                ingredients_json = json.loads(ingredients)
            except json.JSONDecodeError:
                st.error("Failed to parse ingredients. Please ensure it is valid JSON.")
                return
            
            drink_data = {
                "name": name,
                "category": category,
                "ingredients": ingredients_json,
                "glass": glass,
                "instructions": instructions,
                "image": image
            }

            try:
                response = requests.post(
                    f"{SoberShotApp.API_BASE_URL}/add-drink",
                    json=drink_data
                )
                response.raise_for_status()
                result = response.json()
                st.success(f"Cocktail added successfully! ID: {result.get('drink', {}).get('_id')}")
            except requests.exceptions.HTTPError as e:
                error_msg = response.json().get('detail', 'Failed to add cocktail due to an unexpected error.')
                st.error(f"Failed to add cocktail: {error_msg}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")



def cocktail_suggester_page():
    """Cocktail suggestion page"""
    st.title("Cocktail Suggester")
    
    ingredients = st.text_area("Enter available ingredients", key="suggestion_ingredients")
    
    if st.button("Get Cocktail Suggestion"):
        suggestion = SoberShotApp.get_cocktail_suggestion(ingredients)
        st.write(suggestion)

if __name__ == "__main__":
    main()