import streamlit as st
import requests
import json

# Configure the API URL
API_URL = "https://demo-unified.cloudjiffy.net"  # Removed trailing slash for consistency

def main():
    st.title("Scenario Management System")
    st.subheader("Add New Scenario")

    # Create form for scenario input
    with st.form("scenario_form"):
        # Basic Information
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Scenario Name")
            type = st.selectbox("Scenario Type", ["sales", "customer"], placeholder="Select Type", index=None)  
            persona_name = st.text_input("Persona Name")
            
        voice_dict = {"Male": "default-gf-lgx1tbshlcmqoc9wy4a__stua", "Female": "default-gf-lgx1tbshlcmqoc9wy4a__neelam"}

        with col2:
            image_url = st.text_input("Image URL")
            voice_id = st.selectbox("Voice ID", list(voice_dict.keys()), placeholder="Select Voice ID", index=None)
            difficulty_level = st.selectbox("Difficulty Level", ["easy", "medium", "hard"], placeholder="Select Level", index=None)

        # Persona Description
        persona = st.text_area("AI Persona Description")

        # Prompt fields
        prompt = st.text_area("Prompt")
        # master_prompt = st.text_area("Master Prompt", help="Enter the master prompt for this scenario")

        # Custom Metrics
        st.markdown("### Custom Metrics (optional)")
        c1, c2 = st.columns(2)
        with c1:
            custom_metric1 = st.text_input("Custom Metric 1")
            custom_metric2 = st.text_input("Custom Metric 2")
            custom_metric3 = st.text_input("Custom Metric 3")
        with c2:
            custom_metric4 = st.text_input("Custom Metric 4")
            custom_metric5 = st.text_input("Custom Metric 5")

        submitted = st.form_submit_button("Add Scenario")

        if submitted:
            # Validate required fields client-side
            if not name or not type or not difficulty_level:
                st.error("Name, Type, and Difficulty Level are required fields")
                return

            # Prepare data for API request
            data = {
                "name": name,
                "difficulty_level": difficulty_level,
                "prompt": prompt,
                # "master_prompt": master_prompt,
                "type": type,  # maps to roleplay_type in FastAPI
                "persona": persona,
                "persona_name": persona_name,
                "image_url": image_url,
                "custom_metric1": custom_metric1 or None,
                "custom_metric2": custom_metric2 or None,
                "custom_metric3": custom_metric3 or None,
                "custom_metric4": custom_metric4 or None,
                "custom_metric5": custom_metric5 or None,
            }

            if voice_id:
                data["voice_id"] = voice_dict[voice_id]

            try:
                response = requests.post(
                    f"{API_URL}/scenarios_tem", 
                    json=data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 201:
                    st.success("Scenario created successfully!")
                    st.json(response.json())
                else:
                    st.error(f"Error creating scenario: {response.text}")
                    st.write(f"Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")

if __name__ == "__main__":
    main()
