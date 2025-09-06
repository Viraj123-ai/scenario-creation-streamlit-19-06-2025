import streamlit as st
import requests
import json

# Configure the API URL
API_URL = "https://demo-unified.cloudjiffy.net/"  

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
            
        voice_dict = {"default-gf-lgx1tbshlcmqoc9wy4a__stua": "default-gf-lgx1tbshlcmqoc9wy4a__stua", "default-gf-lgx1tbshlcmqoc9wy4a__neelam": "default-gf-lgx1tbshlcmqoc9wy4a__neelam"}
        # tts_dict = {
        #     "Retired Old Man": "b2c_retired_old_man",
        #     "Retired Old Lady": "b2c_retired_old_lady",
        #     "Startup Founder": "startup_founder",
        #     "Skeptical Manager": "skeptical_manager",
        #     "B2C Buyer": "b2c_buyer",
        #     "Sharp CEO": "sharp_ceo",
        #     "Software Developer": "software_developer",
        #     "Curious Customer": "curious_customer"
        # }

        with col2:
            image_url = st.text_input("Image URL")
            voice_id = st.selectbox("Voice ID", list(voice_dict.keys()), placeholder="Select Voice ID", index=None)
            # tts_instruction_label = st.selectbox("TTS Instructions", list(tts_dict.keys()), placeholder="Select Instruction", index=None)
            difficulty_level = st.selectbox("Difficulty Level", ["easy", "medium", "hard"], placeholder="Select Level", index=None)

        # Persona Description
        persona = st.text_area("AI Persona Description")

        # Prompt
        prompt = st.text_area("Prompt")

        # Master Prompt - New field added
        # master_prompt = st.text_area("Master Prompt", 
        #                            help="Enter the master prompt for this scenario")

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
                # "master_prompt": master_prompt,  # Added master_prompt field
                "type": type,
                "persona": persona,
                "persona_name": persona_name,
                "image_url": image_url
            }

            if voice_id:
                data["voice_id"] = voice_dict[voice_id]

            # if tts_instruction_label:
            #     data["tts_instructions"] = tts_dict[tts_instruction_label]

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
