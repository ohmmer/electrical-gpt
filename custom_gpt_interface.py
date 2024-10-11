import streamlit as st
import requests
import os
import streamlit.components.v1 as components

# Constants
GPT_API_URL = "https://api.openai.com/v1/completions"
API_KEY = os.getenv('OPENAI_API_KEY')

# Custom CSS for color coding
st.markdown("""
<style>
    /* Blue cells for Project Information */
    div[data-testid="stTextInput"] > div > div > input {
        background-color: #E6F3FF !important;
    }
    /* Yellow cells for Input Data */
    div[data-testid="stSelectbox"] > div > div > select,
    div[data-testid="stNumberInput"] > div > div > input {
        background-color: #FFFFE0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Rest of the code remains the same...

def main():
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Main", "Results", "Instructions", "Settings", "About"])

    with tab1:
        st.markdown("# Custom GPT for Electrical Engineering Calculations")
        st.write("This interface helps you interact with the Custom GPT model for conductor sizing and voltage drop calculations.")

        # Project Details (Blue)
        st.markdown("<h3>Project Details</h3>", unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            project_name = st.text_input("Project Name:", key='project_name', help='Project Information')
        with col2:
            job_number = st.text_input("Job Number:")
        with col3:
            load_tag_number = st.text_input("Load Tag Number:")
        with col4:
            checked_by = st.text_input("Checked By:")
        with col5:
            date = st.date_input("Date:")

        # General Settings (Yellow)
        st.markdown("<h3>General Settings</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            units = st.selectbox("Select Units:", ["Imperial", "Metric"], index=1)
        with col2:
            number_of_phases = st.selectbox("Enter Number of Phases:", [1, 3], index=1)
        with col3:
            insulation_type = st.selectbox("Select Insulation Type:", ["Thermoset", "PVC", "XLPE", "Thermoplastic"], index=0)

        # Load and Electrical Specifications and Conductor and Installation Details (Yellow)
        st.markdown("<h3>Load and Electrical Specifications / Conductor and Installation Details</h3>", unsafe_allow_html=True)
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

        # Generate prompt for GPT and button (rest of the code remains the same)
        # ...

    # Other tabs (Results, Instructions, Settings, About) remain the same
    # ...

if __name__ == "__main__":
    main()
