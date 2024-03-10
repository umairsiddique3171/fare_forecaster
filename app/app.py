import streamlit as st
import pickle
import json
import numpy as np
from utils import scale, predict, load_model , set_background


import warnings
warnings.filterwarnings("ignore")


# set background
set_background('background_img.jpg')


# set title
st.title("Fare Forecaster")


# getting input form user
col1, col2, col3 = st.columns(3)
    
with col1:
    trip_duration = st.text_input('Expected Trip Duration (minutes)')
    
with col2:
    distance_travelled = st.text_input('Commute Distance (km)')

with col3:
    surge_applied = st.text_input('Peak Time (7-9 am / 5-8 pm) (yes/no)')


# load predictor
model = load_model("linear_regression_model.p")

# load scaler
scaler = load_model("min_max_scaler_model.p")

# prediction
if st.button('Results'):
    input_ref = ["Expected Trip Duration","Expected Distance to be travelled","Peak_Hours"]
    input_list = [trip_duration, distance_travelled, surge_applied]
    missing_values = [input_ref[i] for i, val in enumerate(input_list) if val is None or val == '']

    if missing_values:
        st.write("## Missing Values")
        for missing_value in missing_values:
            st.write(f"### Column '{missing_value}' missing.")
        st.write("## Please refresh and enter the values again")
    
    else: 
        if surge_applied.lower() == 'yes':
            surge_applied = 1
        else : 
            surge_applied = 0

        user_input = [float(trip_duration),float(distance_travelled),int(surge_applied)]
        scaled_data = scale(user_input,scaler)
        result = predict(scaled_data,model)

        # show results
        st.write("## Result")
        st.write(f"### Expected Fare : {result:.2f} Rupees")

        