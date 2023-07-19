import os
import streamlit as st

from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.callbacks.base import BaseCallbackHandler

# Class to stream response to the frontend as the LLM comes up with it
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

# Function to create and return a conversation chain object
def get_conversation_chain(memory, openai_api_key, stream_handler):
    llm = ChatOpenAI(temperature=0.0, openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler])

    chain = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )

    return chain


# Main function to run the Streamlit app
def main():
    load_dotenv()   # Load environment variables from .env file if present

    st.title("🤖 LLM ChatBot")  # Title for the Streamlit app

    # Create and initialize the conversation memory if not present in session state
    if "memory" not in st.session_state:
        st.session_state["memory"] = ConversationBufferMemory(return_messages=True)

    # Create two columns for API Key input and Conversation clear button
    col1, col2 = st.columns([0.75, 0.25])
    openai_api_key = col1.text_input('OpenAI API Key', value=os.environ.get("OPENAI_API_KEY", ""), placeholder='OpenAI API Key', type='password', label_visibility="collapsed")
    clear_conversation_button = col2.button("Clear Conversation")
    user_input = st.chat_input("Say something")

    # Clear conversation history if the "Clear Conversation" button is clicked
    if clear_conversation_button:
        # flush the memory
        memory = st.session_state["memory"]
        memory.clear()
        user_input = None


    # Create a container for displaying the chat message history
    with st.container():
        # Write chat message history from the memory
        for msg in st.session_state["memory"].load_memory_variables({})["history"]:
            if msg.type == "ai":
                # Display assistant's messages with the "assistant" tag
                with st.chat_message("assistant"):
                    st.write(msg.content)
            else:
                # Display user's messages with the "user" tag
                with st.chat_message("user"):
                    st.write(msg.content)


        # Display a warning if the API key is not provided or is incorrect
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')

        # If the user entered some input and the API key is valid, process the user's input
        if user_input and openai_api_key.startswith('sk-'):
            # Display the user's input in the chat
            with st.chat_message("user"):
                st.write(user_input)

            # Display the assistant's response in the chat
            with st.chat_message("assistant"):
                stream_handler = StreamHandler(st.empty())
                memory = st.session_state["memory"]
                chain = get_conversation_chain(memory, openai_api_key, stream_handler)
                _ = chain.run(user_input)
        

if __name__ == "__main__":
    main()