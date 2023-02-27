import streamlit as st
import openai
import uuid
import time
import os
import pandas as pd

# Set up the OpenAI API key
openai.api_key = os.environ["JOSHUA_FREEEDU_OPENAI_API_KEY"]

# Initialize the conversation history
if st.session_state.get("conversation_history") is None:
    st.session_state["conversation_history"] = pd.DataFrame(columns=["User Prompts","Bot Responses"])

# if st.session_state.get("conversation_history", pd.DataFrame()).empty:
#     st.session_state["conversation_history"] = pd.DataFrame(columns=["User Prompts","Bot Responses"])


# Define a function to generate a response from OpenAI's GPT model
def generate_response(prompt, conversation_history):
    # Concatenate the last 2 prompts and bot responses from conversation history with the new prompt
    # We only need the last 2 conversations to conserve tokens
    conversation = parse_conversation(conversation_history, display_only=False)

    new_prompt = "You are a chatbot named 'Aidee'. Respond in a cheerful and friendly chatbot manner, " \
                 "while considering our conversation history as follows: " \
                 "\n \"" + conversation + "\" \n" \
                  " Now, with consideration to that conversation history, answer this new prompt: " \
                  "\n " + prompt
    print(f"Prompt sent to ChatGPT: \n{new_prompt}")

    # Generate the response
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=new_prompt,
        max_tokens=1024,
        temperature=0.7,
        n=1,
        stop=None,
    )

    # Extract the response text from the API response
    response_text = response.choices[0].text.strip()

    # Return the response text and updated conversation history
    return response_text

def parse_conversation(conversation_history, count_from_last = 5, display_only = True):
    conversation = ""
    if display_only == False and len(conversation_history) > count_from_last:
        for i in range((len(conversation_history)-1) - (count_from_last-1), len(conversation_history)):
            conversation += "User: " + conversation_history.iloc[i,0] + "\n"
            conversation += "ChatBot: " + conversation_history.iloc[i,1] + "\n"
    else:
        for i in range(len(conversation_history)):
            conversation += f"Log #{i+1} ------------------------------------------------------ \n"
            conversation += "User: " + conversation_history.iloc[i,0] + "\n"
            conversation += "ChatBot: " + conversation_history.iloc[i,1] + "\n\n"

    return conversation

def send_message(conversation_history, user_message):
    # Initialize the conversation prompt
    conversation_prompt = ""
    # Append the user's message to the conversation prompt
    conversation_prompt += user_message.strip()
    # Generate a response from OpenAI's GPT model
    bot_response = generate_response(conversation_prompt, conversation_history)

    # Update the conversation history in session state
    conversation_history.loc[len(conversation_history)] = [conversation_prompt, bot_response]
    st.session_state["conversation_history"] = conversation_history

# Define the Streamlit app
def main():
    st.subheader("Hi, I'm Aidee! How can I help you today?")
    # Load the conversation history from localStorage
    conversation_history = st.session_state.get("conversation_history", "")

    # Add a text input for the user to enter their message
    user_message = st.text_input("You", value="", key="user_message", on_change=lambda text_value: send_message(conversation_history, text_value))

    # Add a button to submit the user's message and generate a response
    if st.button("Send"):
        send_message(conversation_history, user_message)

    # Display the conversation history
    conversation = parse_conversation(st.session_state["conversation_history"])
    st.text_area("Chat", value=conversation, height=800, disabled=True)

# Run the chatbot
if __name__ == "__main__":
    main()