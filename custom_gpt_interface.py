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
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Main", "Results", "Instructions"])

    with tab1:
        # Make the title smaller to reduce white space
        st.markdown("# Custom GPT for Electrical Engineering Calculations")
        st.markdown("This interface helps you interact with the Custom GPT model for conductor sizing and voltage drop calculations.")

        # Compact Layout for Inputs
        with st.container():
            # Project Details (Top Section)
            st.markdown("### Project Details")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                project_name = st.text_input("Project Name:")
            with col2:
                job_number = st.text_input("Job Number:")
            with col3:
                load_tag_number = st.text_input("Load Tag Number:")
            with col4:
                checked_by = st.text_input("Checked By:")
            with col5:
                date = st.date_input("Date:")

        with st.container():
            # General Settings (Below Project Details)
            st.markdown("### General Settings")
            col1, col2, col3 = st.columns(3)
            with col1:
                units = st.selectbox("Select Units:", ["Imperial", "Metric"], index=1)
            with col2:
                number_of_phases = st.selectbox("Enter Number of Phases:", [1, 3], index=1)
            with col3:
                insulation_type = st.selectbox("Select Insulation Type:", ["Thermoset", "PVC", "XLPE", "Thermoplastic"], index=0)

        with st.container():
            # Load and Electrical Specifications and Conductor and Installation Details
            st.markdown("### Load and Electrical Specifications / Conductor and Installation Details")
            col1, col2 = st.columns(2)
            with col1:
                load_current = st.number_input("Enter Load Current (A):", min_value=0.0, value=10.0, step=0.1)
                supply_voltage = st.number_input("Enter Supply Voltage (V):", min_value=0.0, value=208.0, step=1.0)
                power_factor = st.number_input("Enter Power Factor (0-1):", min_value=0.0, max_value=1.0, value=1.0, step=0.01)
            with col2:
                number_of_runs_per_phase = st.number_input("Enter Number of Runs per Phase:", min_value=1, value=1, step=1)
                total_conductors = st.number_input("Enter Total Number of Power Conductors in Raceway:", min_value=1, value=1, step=1)
                max_voltage_drop = st.number_input("Enter Max Allowable Voltage Drop (per unit or %):", min_value=0.0, value=0.05, step=0.01)
                ambient_temperature = st.number_input("Enter Maximum Design Ambient Temperature (°C):", min_value=-50.0, value=40.0, step=1.0)

        # Generate prompt for GPT
        prompt = (
            f"Project Name: {project_name}, Job Number: {job_number}, Load Tag Number: {load_tag_number}, Checked By: {checked_by}, Date: {date}. "
            f"What conductor size is needed for a {load_current}A load at {supply_voltage}V using {insulation_type} insulation? "
            f"The units are {units}, number of phases is {number_of_phases}, number of runs per phase is {number_of_runs_per_phase}, "
            f"power factor is {power_factor}, total number of power conductors in raceway is {total_conductors}, "
            f"maximum allowable voltage drop is {max_voltage_drop}, and the ambient temperature is {ambient_temperature}°C."
        )

        # Get GPT response
        if st.button("Get Conductor Size Recommendation"):
            response = get_gpt_response(prompt)
            if "Error" in response:
                st.error(response)
            else:
                st.write("### Recommended Conductor Size:")
                st.success(response)

    with tab2:
        st.markdown("# Results")
        st.write("This tab will display the results of the conductor sizing calculations.")
        # Future implementation could include saving results and displaying them here

    with tab3:
        st.markdown("# Instructions")
        st.write("""
        **Instructions for Using This Application:**
        
        1. Fill in the project details such as Project Name, Job Number, Load Tag Number, etc.
        2. Enter the general settings, including units, number of phases, and insulation type.
        3. Provide the load and electrical specifications as well as conductor installation details.
        4. Click the "Get Conductor Size Recommendation" button to get the calculated recommendation.
        5. Navigate to the **Results** tab to view or save past calculations (future feature).
        """)

if __name__ == "__main__":
    main()
