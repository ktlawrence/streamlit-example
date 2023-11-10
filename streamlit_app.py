import streamlit as st
import openai

# Initialize the OpenAI client
client = openai.OpenAI()

# Access the API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title('Chat with AI')
user_input = st.text_input("Talk to the AI")

if st.button('Send'):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{user_input}"}
            ]
        )
        # Debugging: Print or display the response to understand its structure
        st.write("Response:", response)

        # Assuming the response is a dictionary with a 'choices' key
        if 'choices' in response and response['choices']:
            st.text_area("AI Response:", value=response['choices'][0]['message']['content'], height=200)
        else:
            st.error("Received an unexpected response format from OpenAI.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
