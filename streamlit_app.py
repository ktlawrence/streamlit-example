import streamlit as st
import openai
# Access the API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]
st.title('Chat with AI')
user_input = st.text_input("Talk to the AI")
if st.button('Send'):
   try:
       response = openai.ChatCompletion.create(
           model="gpt-3.5-turbo",
           messages=[
               {"role": "system", "content": "You are a helpful assistant."},
               {"role": "user", "content": f"{user_input}"}
           ]
       )
       # Check if the response has the expected structure
       if 'choices' in response and response['choices']:
           st.text_area("AI Response:", value=response['choices'][0]['message']['content'], height=200)
       else:
           st.error("Received an unexpected response format from OpenAI.")
   except openai.error.OpenAIError as e:
       st.error(f"An error occurred with the OpenAI API: {e}")
   except Exception as e:
       st.error(f"An unexpected error occurred: {e}")
