import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Set page configuration
st.set_page_config(page_title="House Price Predictor", layout="wide")

# Load the model and feature list
@st.cache_resource
def load_assets():
    model = joblib.load('house_price_model.pkl')
    features = joblib.load('model_features.pkl')
    return model, features

try:
    model, model_features = load_assets()
    
    st.title("🏡 House Price Prediction App")
    st.markdown("Enter the house details below to estimate the market Sale Price.")

    # Create input fields for key features found in the notebook
    # For a full implementation, we iterate through model_features
    # Here we highlight the most impactful ones mentioned in your project outcome
    
    st.sidebar.header("Key House Attributes")
    
    # Using a form to group inputs
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        user_input = {}
        
        # We fill the input dictionary with default values for all model features
        for feat in model_features:
            user_input[feat] = 0  # Default initialization

        with col1:
            st.subheader("Structure & Quality")
            user_input['OverallQual'] = st.slider("Overall Quality (1-10)", 1, 10, 5)
            user_input['GrLivArea'] = st.number_input("Above Ground Living Area (sq ft)", value=0)
            user_input['YearBuilt'] = st.number_input("Year Built", value=2000)
            user_input['TotalBsmtSF'] = st.number_input("Total Basement Area (sq ft)", value=0)

        with col2:
            st.subheader("Space & Facilities")
            user_input['GarageCars'] = st.selectbox("Garage Car Capacity", [0, 1, 2, 3, 4], index=2)
            user_input['FullBath'] = st.selectbox("Full Bathrooms", [1, 2, 3, 4], index=1)
            user_input['LotArea'] = st.number_input("Lot Area (sq ft)", value=0)
            user_input['Fireplaces'] = st.number_input("Number of Fireplaces", value=0)

        submit_button = st.form_submit_button("Predict Price")

    if submit_button:
        # Prepare the data in the correct order for the model
        input_df = pd.DataFrame([user_input])[model_features]
        
        # Perform prediction
        prediction = model.predict(input_df)
        
        st.success(f"### Estimated Sale Price:  ${prediction[0]:,.2f}")
        
        # Displaying key metrics impact
        st.info("Note: This prediction is based on the Random Forest model trained on the Ames Housing dataset.")

except Exception as e:
    st.error(f"Error loading model or features: {e}")
    st.info("Ensure 'house_price_model.pkl' and 'model_features.pkl' are in the same directory as app.py")