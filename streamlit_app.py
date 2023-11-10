import streamlit as st
import openai

# Initialize the OpenAI client
client = openai.OpenAI()

# Access the API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title('Chat with AI')

# Use session state to store conversation history
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Display previous conversations
if st.session_state['history']:
    st.write("Previous Conversations:")
    for index, message in enumerate(st.session_state['history']):
        # Use a combination of index and content for a unique key
        key = f"msg_{index}_{message['content'][:10]}"  # using the first 10 characters of content
        st.text_area("", value=message['content'], height=100, key=key)

# User input
user_input = st.text_input("Talk to the AI")

# Send button
if st.button('Send'):
    st.session_state['history'].append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state['history']
        )
        
        # Extract the AI response and update the history
        if response.choices:
            message_content = response.choices[0].message.content
            st.session_state['history'].append({"role": "assistant", "content": message_content})
            st.text_area("AI Response:", value=message_content, height=200)
        else:
            st.error("No response received from OpenAI.")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Reset conversation button
if st.button('Reset Conversation'):
    st.session_state['history'] = []
