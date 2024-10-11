import streamlit as st
import requests
import os

# Constants
GPT_API_URL = "https://api.openai.com/v1/completions"
API_KEY = os.getenv('OPENAI_API_KEY')

# Helper function to interact with Custom GPT
def get_gpt_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "YOUR_CUSTOM_GPT_MODEL_NAME",
        "prompt": prompt,
        "max_tokens": 100
    }
    response = requests.post(GPT_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("choices")[0].get("text").strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit interface
def main():
    st.title("Custom GPT for Electrical Engineering Calculations")
    st.write("This interface helps you interact with the Custom GPT model for conductor sizing and voltage drop calculations.")

    # User input fields
    load_current = st.number_input("Enter Load Current (A):", min_value=0.0, step=0.1)
    supply_voltage = st.number_input("Enter Supply Voltage (V):", min_value=0.0, step=1.0)
    insulation_type = st.selectbox("Select Insulation Type:", ["Thermoset", "PVC", "XLPE", "Thermoplastic"])

    # Generate prompt for GPT
    prompt = f"What conductor size is needed for a {load_current}A load at {supply_voltage}V using {insulation_type} insulation?"

    # Get GPT response
    if st.button("Get Conductor Size Recommendation"):
        response = get_gpt_response(prompt)
        st.write("### Recommended Conductor Size:")
        st.write(response)

if __name__ == "__main__":
    main()
