import streamlit as st
import openai
# Load your API key from an environment variable or secure source
openai.api_key = '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'
st.title('Chat with AI')
# Create a text box for user input
user_input = st.text_input("Talk to the AI")
# When the user submits a question

if st.button('Send'):
   # Call the OpenAI API with the new chat.completions.create method
   response = openai.chat.completions.create(
       model="gpt-3.5-turbo",
       messages=[
           {"role": "system", "content": "You are a helpful assistant."},
           {"role": "user", "content": f"{user_input}"}
       ]
   )
   # Display the model's response
   st.text_area("AI Response:", value=response['choices'][0]['message']['content'], height=200)
