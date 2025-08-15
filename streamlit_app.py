import streamlit as st 
import requests
from requests.exceptions import ConnectionError

# Возможные адреса API (сначала docker, потом локальный)
API_ENDPOINTS = [
    "http://app:5100",       # если работает внутри docker-compose
    "http://localhost:5100"  # если локальный запуск
]

def get_api_url():
    for url in API_ENDPOINTS:
        try:
            # Проверяем health эндпоинт
            response = requests.get(f"{url}/health", timeout=1)
            if response.status_code == 200:
                return url
        except Exception:
            continue
    return None

api_url = get_api_url()

# Заголовок приложения
st.title("Titanic Survival Prediction")

# Ввод данных
st.write("Enter the passenger details:")

pclass = st.selectbox("Ticket Class (Pclass)", [1, 2, 3])

age = st.text_input("Age", value="10")
if not age.isdigit():
    st.error("Please enter a valid number for Age.")

fare = st.text_input("Fare", value="100")
if not fare.isdigit():
    st.error("Please enter a valid number for Fare.")

if st.button("Predict"):
    if not api_url:
        st.error("API server is not available")
    elif age.isdigit() and fare.isdigit():
        data = {
            "Pclass": int(pclass),
            "Age": float(age),
            "Fare": float(fare)
        }
        try:
            response = requests.post(f"{api_url}/predict_model", json=data)
            if response.status_code == 200:
                prediction = response.json()["prediction"]
                st.success(f"Prediction: {prediction}")
            else:
                st.error(f"Request failed with status code {response.status_code}")
        except ConnectionError:
            st.error("Failed to connect to the server")
    else:
        st.error("Please fill in all fields with valid numbers.")
