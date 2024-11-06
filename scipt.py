import streamlit as st
from arcgis.gis import GIS
from skopt import gp_minimize

# ArcGIS OAuth 2.0 Credentials
client_id = "nyy7ScY1ieQBifwB"
client_secret = "41b69f18826f49ba8ca95070f9d877bc"

# Authenticate with ArcGIS
try:
    gis = GIS("https://www.arcgis.com", client_id=client_id, client_secret=client_secret)
    st.write("Authenticated with ArcGIS Online.")
except Exception as e:
    st.error("Error with ArcGIS OAuth Authentication: " + str(e))

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

# Create an ArcGIS Map Centered on the Input Region
if region:
    try:
        # Create a map centered on the specified region
        map_region = region if region else "USA"
        map = gis.map(map_region)
        map.zoom = 5

        # Get the item associated with the map for embedding
        map_item_url = map.item.homepage if map.item else "Error: Unable to retrieve map URL"

        # Display the map
        st.subheader("Predicted Spread Map")
        if map_item_url != "Error: Unable to retrieve map URL":
            st.components.v1.iframe(map_item_url, width=700, height=500)
        else:
            st.error("Error displaying the map: Unable to retrieve map URL.")
    except Exception as e:
        st.error("Error displaying the map: " + str(e))
else:
    st.warning("Please enter a region to view the map.")