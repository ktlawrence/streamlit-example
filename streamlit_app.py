import streamlit as st
import openai

# Function to handle sending and receiving messages
def submit_response():
    user_input = st.session_state.user_input
    if user_input:  # Check if there's input to avoid empty requests
        with st.spinner('Waiting for AI response...'):
            try:
                # Add user input to history
                st.session_state['history'].append({"role": "user", "content": user_input})

                # Get response from OpenAI
                response = openai.Completion.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state['history']
                )

                # Extract the AI response and update the history
                if response.choices:
                    message_content = response.choices[0]["message"]["content"]
                    st.session_state['history'].append({"role": "assistant", "content": message_content})
                    st.session_state.user_input = ""  # Clear input field after sending
                    st.experimental_rerun()  # Refresh to display new messages
                else:
                    st.error("No response received from OpenAI.")

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

# Initialize the OpenAI client
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title('Chat with AI')

# Custom CSS to style the conversation
st.markdown("""
<style>
    .previous-convo {
        color: black;
        background-color: #ffff99;  /* Yellow background */
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .ai-response {
        color: black;
        background-color: #e0e0e0;  /* Light gray background */
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Use session state to store conversation history
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Display previous conversations
if st.session_state['history']:
    st.markdown("### Previous Conversations:")
    for index, message in enumerate(st.session_state['history']):
        message_class = 'previous-convo' if message['role'] == 'user' else 'ai-response'
        st.markdown(
            f"<div class='{message_class}'>{message['content']}</div>",
            unsafe_allow_html=True
        )

# User input with Enter key submission
st.text_input(
    "Talk to the AI", 
    key="user_input",
    on_change=submit_response,
    value=""  # Initializing as empty
)

# Reset conversation button
if st.button('Reset Conversation'):
    st.legacy_caching.clear_cache()
    st.session_state['history'] = []
    st.experimental_rerun()
