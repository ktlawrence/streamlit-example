import streamlit as st
import openai
client =openai.OpenAI()
# Initialize the OpenAI client
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title('Chat with AI')

# Custom CSS to style the conversation
st.markdown("""
<style>
    .previous-convo {
        color: black;
        background-color: #ffff99;  /* Yellow background for previous conversations */
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .current-convo {
        color: black;
        background-color: #e0e0e0;  /* Light gray background for current conversation */
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
        style_class = 'previous-convo' if index < len(st.session_state['history']) - 1 else 'current-convo'
        st.markdown(f"<div class='{style_class}'>{message['content']}</div>", unsafe_allow_html=True)

# User input
user_input = st.text_input("Talk to the AI", key="user_input")

# Send button
if st.button('Send'):
    st.session_state['history'].append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=st.session_state['history']
        )
        
        # Extract the AI response and update the history
        if response.choices:
            message_content = response.choices[0].message.content
            st.session_state['history'].append({"role": "assistant", "content": message_content})
            st.experimental_rerun()  # Refresh to display new messages
        else:
            st.error("No response received from OpenAI.")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Reset conversation button
if st.button('Reset Conversation'):
    st.session_state['history'] = []
    st.experimental_rerun()
