import streamlit as st
import requests
import json
from typing import Optional

# Base API details
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "872aedbe-d9e0-4a9c-95aa-25d133efbbc4"
FLOW_ID = "4c83ce2f-69f7-492b-b487-2b2f6fba3a2f"
APPLICATION_TOKEN = ""  # Replace with your actual token
ENDPOINT = ""  # You can set a specific endpoint name in the flow settings

# Tweak dictionary (optional)
TWEAKS = {
    "ChatInput-GaqTa": {},
    "ParseData-mu0DE": {},
    "Prompt-UFOcP": {},
    "SplitText-URuco": {},
    "ChatOutput-dAv3H": {},
    "AstraDB-AvJhE": {},
    "AstraDB-ZLYeD": {},
    "File-IQ7O6": {},
    "Google Generative AI Embeddings-Ammm6": {},
    "Google Generative AI Embeddings-lVDK5": {},
    "GoogleGenerativeAIModel-muC2d": {},
    "AstraDBChatMemory-DoWge": {},
    "AstraDBCQLToolComponent-IBh2C": {},
    "AstraDBCQLToolComponent-uQWgS": {}
}

def run_flow(
    message: str,
    endpoint: str,
    output_type: str = "chat",
    input_type: str = "chat",
    tweaks: Optional[dict] = None,
    application_token: Optional[str] = None
) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Streamlit UI
st.title("Langflow Chatbot")
st.markdown("Interact with the Langflow-powered chatbot.")

# Input field for user message
user_message = st.text_input("Your Message:", placeholder="Type your message here...")

# Button to send the message
if st.button("Send"):
    if not user_message:
        st.warning("Please enter a message to send.")
    else:
        st.markdown("#### Response:")
        try:
            # Call the Langflow API
            response = run_flow(
                message=user_message,
                endpoint=ENDPOINT or FLOW_ID,
                tweaks=TWEAKS,
                application_token=APPLICATION_TOKEN
            )
            # Parse and display the response
            st.write(response['outputs'][0]['outputs'][0]['results']['message']['data']['text'])
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
