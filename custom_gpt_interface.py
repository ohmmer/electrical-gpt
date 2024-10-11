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
            project_name = st.text_input("Project Name:")
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
        
        1. The spreadsheet will calculate the voltage drop based on the supply voltage, load current, conductor material, and conductor length.
        2. The spreadsheet provides a minimum recommended conductor size based on the requirements of Tables 1 to 5 of the Canadian Electrical Code.
        3. The calculation assumes that the supply transformer is infinitely large and therefore the supply voltage is not affected by the load size.
        4. Only the blue (Project Information) cells and yellow (Input Data) cells are available for user data entry.
        5. The green cells will 'look up' the 'Minimum Recommended Cable Size' and associated 'Ampacity Rating'. The information from the 'Minimum Recommended Cable Size' green cell can then be placed in the corresponding yellow 'Cable Size' cell. The data in the yellow 'Cable Size' cell is used to calculate the voltage drop.
        6. Voltages from 1 VAC to 35,000 VAC can be entered.
        7. Drop-down cells are used to limit input data choices to only those provided.
        8. Voltage drop at the load should be limited to 3% on running per CEC Rule 8-102 and 15% on starting unless an approved variance to the CEC has been issued.
        9. The calculated conductor resistance is based on conductor size, conductor material, number of runs, conductor length, ambient temperature, and heat generated by current flow.
        10. The conductor reactance is based on conductor size, conductor spacing (a function of insulation thickness primarily due to voltage rating), number of runs, and conductor length.
        11. Insulation types are Thermoplastics and Thermosets. Thermoplastics include PVC, TFE / FEP (Teflon), ETFE (Tefzel), PP (Polypropylene), and PE (Polyethylene). Thermosets include XLPE / XLP (Crosslinked Polyethylene), CPE (Chlorinated Polyethylene), and EPR (Ethylene Propylene Rubber).
        12. Bolted 3-phase fault level at the supply or 'upstream' bus.
        13. Thru-fault current carried by conductor.
        14. The conductor must be sized to withstand the short circuit current thru fault levels where the fault is electrically downstream of the cable. The short circuit withstand times are based on the following formulas:
           - CU: t = 0.0297 x LOG((T2 + 234)/(T1 +234)) x (kcmil)^2 / (Conductor thru-fault current)^2
           - AL: t = 0.0125 x LOG((T2 + 228)/(T1 +228)) x (kcmil)^2 / (Conductor thru-fault current)^2
           - Where t = seconds, T1 = Insulation temperature rating (75°C for Thermoplastic and 90°C for Thermoset), T2 = Insulation SC temperature rating (150°C for Thermoplastic and 250°C for Thermoset)
        15. For the purposes of this calculation, short circuit withstand time is assumed to be not critical if the conductor protective device includes "instantaneous" tripping for high fault currents.
        16. The determination of conductor short circuit withstand time is critical with short runs of conductor where the upstream conductor instantaneous protection is disabled for coordination purposes with downstream protective devices. It is recommended that in cases like this where a protection and coordination study has not been completed, the conductor be sized for a short circuit withstand time of 0.2 seconds (12 cycles) or greater.
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
        
        This application assists electrical engineers in determining conductor sizing and analyzing voltage drop calculations using an AI-powered Custom GPT model.
        
        **Purpose**: The goal of this tool is to streamline conductor sizing calculations, ensure consistency, and reduce manual calculation errors.
        
        **Developer Information**: Developed by [Your Name/Company] for engineering professionals seeking efficiency in project calculations.
        
        **Disclaimer**: This application is intended to aid calculations but should not be solely relied upon for critical engineering decisions without verification.
        """)

if __name__ == "__main__":
    main()
