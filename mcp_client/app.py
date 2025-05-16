import streamlit as st
import requests
import json
from typing import Dict, List
import pandas as pd

# Server URL
SERVER_URL = "http://localhost:8000"

def main():
    st.title("Application-Capability Analysis System")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Natural Language Query", "Application Analysis", "Capability Analysis"]
    )
    
    if page == "Natural Language Query":
        show_natural_language_query()
    elif page == "Application Analysis":
        show_application_analysis()
    else:
        show_capability_analysis()

def show_natural_language_query():
    st.header("Ask Questions About Your Data")
    
    # Text input for the question
    question = st.text_area(
        "Enter your question about applications and capabilities:",
        height=100
    )
    
    if st.button("Analyze"):
        if question:
            try:
                response = requests.post(
                    f"{SERVER_URL}/analyze",
                    json={"question": question}
                )
                if response.status_code == 200:
                    st.write("### Analysis Result")
                    st.write(response.json()["response"])
                else:
                    st.error(f"Error: {response.json()['detail']}")
            except Exception as e:
                st.error(f"Error connecting to server: {str(e)}")
        else:
            st.warning("Please enter a question")

def show_application_analysis():
    st.header("Application Analysis")
    
    try:
        # Get list of applications
        response = requests.get(f"{SERVER_URL}/applications")
        if response.status_code == 200:
            applications = response.json()["applications"]
            
            # Create a DataFrame for better display
            df = pd.DataFrame(applications)
            
            # Display applications in a table
            st.write("### Applications Catalog")
            st.dataframe(df)
            
            # Application details
            st.write("### Application Details")
            selected_app = st.selectbox(
                "Select an application to view details:",
                options=[app["application_id"] for app in applications],
                format_func=lambda x: f"{x} - {next((app['Application name'] for app in applications if app['application_id'] == x), '')}"
            )
            
            if selected_app:
                app_response = requests.get(f"{SERVER_URL}/application/{selected_app}")
                if app_response.status_code == 200:
                    app_data = app_response.json()
                    
                    # Display application details
                    st.write("#### Application Information")
                    st.json(app_data["application"])
                    
                    # Display consumed capabilities
                    st.write("#### Consumed Capabilities")
                    st.dataframe(pd.DataFrame(app_data["consumed_capabilities"]))
                    
                    # Display provided capabilities
                    st.write("#### Provided Capabilities")
                    st.dataframe(pd.DataFrame(app_data["provided_capabilities"]))
                else:
                    st.error(f"Error: {app_response.json()['detail']}")
        else:
            st.error(f"Error: {response.json()['detail']}")
    except Exception as e:
        st.error(f"Error connecting to server: {str(e)}")

def show_capability_analysis():
    st.header("Capability Analysis")
    
    try:
        # Get list of capabilities
        response = requests.get(f"{SERVER_URL}/capabilities")
        if response.status_code == 200:
            capabilities = response.json()["capabilities"]
            
            # Create a DataFrame for better display
            df = pd.DataFrame(capabilities)
            
            # Display capabilities in a table
            st.write("### Capabilities Catalog")
            st.dataframe(df)
            
            # Capability details
            st.write("### Capability Details")
            selected_cap = st.selectbox(
                "Select a capability to view details:",
                options=[cap["capability_id"] for cap in capabilities],
                format_func=lambda x: f"{x} - {next((cap['name'] for cap in capabilities if cap['capability_id'] == x), '')}"
            )
            
            if selected_cap:
                cap_response = requests.get(f"{SERVER_URL}/capability/{selected_cap}")
                if cap_response.status_code == 200:
                    cap_data = cap_response.json()
                    
                    # Display capability details
                    st.write("#### Capability Information")
                    st.json(cap_data["capability"])
                    
                    # Display consuming applications
                    st.write("#### Consuming Applications")
                    st.dataframe(pd.DataFrame(cap_data["consuming_applications"]))
                    
                    # Display providing applications
                    st.write("#### Providing Applications")
                    st.dataframe(pd.DataFrame(cap_data["providing_applications"]))
                else:
                    st.error(f"Error: {cap_response.json()['detail']}")
        else:
            st.error(f"Error: {response.json()['detail']}")
    except Exception as e:
        st.error(f"Error connecting to server: {str(e)}")

if __name__ == "__main__":
    main() 