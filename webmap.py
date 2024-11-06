import streamlit as st
from skopt import gp_minimize

# Title and Introduction
st.title("EpiSphere: Predicting Monkeypox Spread with ArcGIS and Bayesian Optimization")

# User Input for Variables
st.subheader("Input Parameters")
region = st.text_input("Geographic Region (e.g., San Francisco)")
population_density = st.slider("Population Density (people per sq km)", 0, 10000, 500)
healthcare_proximity = st.slider("Healthcare Proximity (distance in km)", 1, 100, 10)
vaccination_rate = st.slider("Vaccination Rate (%)", 0, 100, 50)

# Define a Bayesian Optimization Model
def spread_risk_model(params):
    pop_density, healthcare_prox, vacc_rate = params
    # Hypothetical formula for spread risk
    risk = pop_density / healthcare_prox * (1 - vacc_rate / 100)
    return -risk  # Minimize negative risk to find high-risk areas

# Run Bayesian Optimization
res = gp_minimize(spread_risk_model, [(0, 10000), (1, 100), (0, 100)], n_calls=10)
predicted_risk = -res.fun

# Display Predicted Risk Result
st.subheader("Predicted Risk of Monkeypox Spread")
st.write(f"Predicted Risk Score: {predicted_risk}")

# ArcGIS Online Map Embedding
# Replace 'your_webmap_id' with the actual Web Map ID from your saved map in ArcGIS Online
webmap_id = "6238018a7df24b9f80e74d35d9b0dffe"
arcgis_map_url = f"https://www.arcgis.com/home/webmap/viewer.html?webmap={webmap_id}"

# Display the map using an iframe
st.subheader("Predicted Spread Map")
st.components.v1.iframe(arcgis_map_url, width=700, height=500)

# Alternatively, provide a link if embedding is not working
st.markdown(f"[Open Map in ArcGIS Online]({arcgis_map_url})")