
# Beverage Recommendation System 🍸

This repository contains the implementation of **SoberShot**, a Beverage Recommendation System built as the final project for the CIS*6020 course. The project provides a collaborative filtering-based approach to recommend drinks based on user preferences, drink similarities, and contextual factors.

---

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
- [Usage](#usage)
- [APIs](#apis)
- [Contributors](#contributors)
- [License](#license)

---

## Introduction
The **SoberShot** system helps users decide what to drink based on:
- Alcohol preferences
- Glass types
- Ingredients
- Popularity among other drinkers

The project leverages machine learning, deep learning, and data engineering principles to create a highly customizable recommendation system.
---

## Features
1. **Drink Recommendations**:
   - Collaborative filtering-based drink suggestions.
   - Variability to ensure diverse recommendations.

2. **Search Functionality**:
   - Search drinks by name or category.

3. **Add Drinks**:
   - Add custom drinks to the database.

4. **Cocktail Suggester**:
   - AI-powered cocktail recipe generation using available ingredients.

5. **Interactive UI**:
   - Built using Streamlit for seamless user interaction.

6. **REST APIs**:
   - Backend powered by FastAPI, supporting functionalities like adding drinks and fetching recommendations.

---

## Technologies Used
- **Programming Languages**: Python
- **Frameworks**:
  - FastAPI (Backend APIs)
  - Streamlit (Frontend UI)
- **Machine Learning**:
  - TensorFlow (Neural Network)
  - Scikit-learn (Preprocessing, PCA)
- **Database**:
  - MongoDB (Drink storage)
- **Hosting**:
  - Render.com (API hosting)
- **Libraries**:
  - pandas, numpy, matplotlib, seaborn (Data processing & visualization)
  - Together API (Cocktail suggestions)

---

## Setup

### Prerequisites
1. Python 3.8 or later
2. MongoDB database (Cloud or Local)
3. Clone this repository 
```bash
https://github.com/HarshTiwari1710/Sobershot
```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Backend:
    ```bash
    uvicorn app:app --reload
    ```
5. Start the Frontend:
    ```bash
    streamlit run Streamlitapp.py
    ```
---




## Usage/Examples

The api has been hosted on the platform named [render.com](https://render.com/)

```bash
API URL: https://sobershot.onrender.com
```
To test API On render Please visit the link below:
```bash
https://sobershot.onrender.com/docs#/
```
You will see a Swagger UI for testing and you can test the Hosted API there which is connected to the Streamlit frontend

1. Root Endpoint:

- URL: /
- Method: GET
- Returns: API status message.
2. Add Drink:
- URL: /add-drink
- Method: POST
``` json
{
    "name": "Drink Name",
    "category": "Category",
    "ingredients": {"Ingredient": "Measurement"},
    "glass": "Glass Type",
    "instructions": "Mixing Instructions",
    "image": "Image URL"
}
```
Returns: Success or error message.

3. Search Drinks:
- URL: /search
- Method: GET
- Query Parameter: query
- Returns: List of matching drinks.
4. Recommend Drinks:
- URL: /recommend
- Method: POST
``` json
{
    "drink_index": 10,
    "top_n": 5
}
```
Returns: List of recommended drinks.

## Contributions
- Harsh Tiwari
- Master's in Data Science, University of Guelph
- GitHub: [HarshTiwari1710](https://github.com/HarshTiwari1710)