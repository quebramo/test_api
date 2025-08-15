import streamlit as st 
import requests
from requests.exceptions import ConnectionError

# Используем имя сервиса из docker-compose
ip_api = "app_api"
port_api = "8000"

st.title("Titanic Survival Prediction")

pclass = st.selectbox("Ticket Class (Pclass)", [1, 2, 3])
age = st.text_input("Age", value="10")
fare = st.text_input("Fare", value="100")

if st.button("Predict"):
    if age.isdigit() and fare.isdigit():
        data = {
            "Pclass": int(pclass),
            "Age": float(age),
            "Fare": float(fare)
        }
        try:
            response = requests.post(f"http://{ip_api}:{port_api}/predict_model", json=data)
            if response.status_code == 200:
                prediction = response.json()["prediction"]
                st.success(f"Prediction: {prediction}")
            else:
                st.error(f"Request failed with status code {response.status_code}")
        except ConnectionError:
            st.error("Failed to connect to the API")
    else:
        st.error("Please enter valid numbers.")
