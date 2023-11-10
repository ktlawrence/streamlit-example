import streamlit as st
import openai
# Access the API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]
st.title('Chat with AI')
user_input = st.text_input("Talk to the AI")
if st.button('Send'):
   try:
       response = openai.chat.completions.create(
           model="gpt-3.5-turbo",
           messages=[
               {"role": "system", "content": "You are a helpful assistant."},
               {"role": "user", "content": f"{user_input}"}
           ]
       )
       # Check if the response has the expected structure
       st.text_area("AI Response:", value=response['choices'][0]['message']['content'], height=200)

   except Exception as e:
       st.error(f"An unexpected error occurred: {e}")
