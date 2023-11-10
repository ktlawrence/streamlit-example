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
        
        # Accessing the response content
        if response.choices:
            message_content = response.choices[0].message.content
            st.text_area("AI Response:", value=message_content, height=200)
        else:
            st.error("No response received from OpenAI.")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
