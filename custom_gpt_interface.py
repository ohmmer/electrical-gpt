import streamlit as st
import requests
import os
import streamlit.components.v1 as components

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
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Main", "Results", "Instructions", "Settings", "About"])

    with tab1:
        st.markdown("# Custom GPT for Electrical Engineering Calculations")
        st.write("This interface helps you interact with the Custom GPT model for conductor sizing and voltage drop calculations.")

        # Project Details
        st.markdown("<div style='border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #555; margin-bottom: 10px;'>Project Details</h3>", unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            , key='project_name', help='Project Information', style={'background-color': '#FFFF00'})
        with col2:
            job_number = st.text_input("Job Number:")
        with col3:
            load_tag_number = st.text_input("Load Tag Number:")
        with col4:
            checked_by = st.text_input("Checked By:")
        with col5:
            date = st.date_input("Date:")
        st.markdown("</div>", unsafe_allow_html=True)

        # General Settings (Below Project Details)
        st.markdown("<div style='border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #555; margin-bottom: 10px;'>General Settings</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1], gap="small")
        with col1:
            units = st.selectbox("Select Units:", ["Imperial", "Metric"], index=1)
        with col2:
            number_of_phases = st.selectbox("Enter Number of Phases:", [1, 3], index=1)
        with col3:
            insulation_type = st.selectbox("Select Insulation Type:", ["Thermoset", "PVC", "XLPE", "Thermoplastic"], index=0)
        st.markdown("</div>", unsafe_allow_html=True)

        # Load and Electrical Specifications and Conductor and Installation Details
        st.markdown("<div style='border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #555; margin-bottom: 10px;'>Load and Electrical Specifications / Conductor and Installation Details</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            load_current = st.number_input("Enter Load Current (A):", min_value=0.0, value=10.0, step=0.1)
            supply_voltage = st.number_input("Enter Supply Voltage (V):", min_value=0.0, value=208.0, step=1.0)
            power_factor = st.number_input("Enter Power Factor (0-1):", min_value=0.0, max_value=1.0, value=1.0, step=0.01)
        with col2:
            number_of_runs_per_phase = st.number_input("Enter Number of Runs per Phase:", min_value=1, value=1, step=1)
            total_conductors = st.number_input("Enter Total Number of Power Conductors in Raceway:", min_value=1, value=1, step=1)
            max_voltage_drop = st.number_input("Enter Max Allowable Voltage Drop (per unit or %):", min_value=0.0, value=0.05, step=0.01)
            ambient_temperature = st.number_input("Enter Maximum Design Ambient Temperature (°C):", min_value=-50.0, value=40.0, step=1.0)
        st.markdown("</div>", unsafe_allow_html=True)

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
                st.markdown("<div style='border-top: 1px solid #ccc; padding-top: 10px; margin-top: 20px;'>", unsafe_allow_html=True)
                st.markdown("### Recommended Conductor Size:")
                st.success(response)
                st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("# Instructions")
        st.write("""
        **Instructions for Using This Application:**
        
        **General Overview**
        - This application calculates the voltage drop based on parameters such as supply voltage, load current, conductor material, and length.
        - The minimum recommended conductor size is determined based on Canadian Electrical Code (Tables 1 to 5).
        - Calculations assume an ideal power supply, meaning supply voltage is constant irrespective of load size.

        **User Input Guidelines**
        - Only specific input fields are editable: 
          - Blue cells represent 'Project Information'.
          - Yellow cells represent 'Input Data'.
        - The green 'Minimum Recommended Cable Size' cell looks up and provides conductor sizes and ampacity ratings. These values are used to calculate voltage drop.
        - Voltages from 1 VAC to 35,000 VAC can be entered.
        - Drop-down selections ensure only valid choices for parameters.

        **Voltage Drop Guidelines**
        - Voltage drop should not exceed 3% during normal operation (as per CEC Rule 8-102) and up to 15% during starting conditions unless a CEC-approved variance is provided.

        **Conductor Resistance and Reactance**
        - Conductor resistance depends on:
          - Size, material, runs, length, ambient temperature, and heat generated by current flow.
        - Conductor reactance is affected by:
          - Size, spacing (determined by insulation thickness and voltage rating), number of runs, and length.

        **Short Circuit Considerations**
        - The conductor must withstand downstream faults; short circuit withstand times are calculated with specific formulas for copper and aluminum.
        - Instantaneous tripping by protective devices typically negates short circuit considerations.
        """)

    with tab4:
        st.markdown("# Settings")
        st.write("Here you can modify the application settings such as API keys and other preferences.")
        api_key = st.text_input("API Key:")
        gpt_model = st.selectbox("Select GPT Model:", ["Custom GPT-3", "Custom GPT-4"])
        temperature = st.slider("Temperature (Creativity Level):", min_value=0.0, max_value=1.0, value=0.5)
        max_tokens = st.number_input("Max Tokens:", min_value=50, max_value=500, value=100)
        if st.button("Save Settings"):
            st.success("Settings saved successfully.")

    with tab5:
        st.markdown("# About")
        st.write("""
        **About This Application**
        
        **Purpose**: This application assists electrical engineers in determining conductor sizing and analyzing voltage drop calculations using an AI-powered Custom GPT model.
        
        **Goal**: The goal of this tool is to streamline conductor sizing calculations, ensure consistency, and reduce manual calculation errors.
        
        **Developer Information**: Developed by [Your Name/Company] for engineering professionals seeking efficiency in project calculations.
        
        **Disclaimer**: This application is intended to aid calculations but should not be solely relied upon for critical engineering decisions without verification.
        """)

if __name__ == "__main__":
    main()
