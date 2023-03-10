import streamlit as st
import openai
import uuid
import time
import os
import pandas as pd

# Set up the OpenAI API key
openai.api_key = os.environ["FREEEDU_OPENAI_API_KEY"]

# Initialize the conversation history
if st.session_state.get("conversation_history") is None:
    st.session_state["conversation_history"] = pd.DataFrame(columns=["User Prompts","Bot Responses"])

# if st.session_state.get("conversation_history", pd.DataFrame()).empty:
#     st.session_state["conversation_history"] = pd.DataFrame(columns=["User Prompts","Bot Responses"])

# Load the conversation history from localStorage
conversation_history = st.session_state.get("conversation_history", "")

def parse_conversation(conversation_history, count_from_last = 10, display_only = True):
    conversation = ""
    if display_only == False and len(conversation_history) > count_from_last:
        for i in range((len(conversation_history)-1) - (count_from_last-1), len(conversation_history)):
            conversation += "User: " + conversation_history.iloc[i,0] + "\n"
            conversation += "Aidee: " + conversation_history.iloc[i,1] + "\n"
    # elif display_only == False:
    #     for i in range(len(conversation_history)):
    #         conversation += "User: " + conversation_history.iloc[i,0] + "\n"
    #         conversation += "Aidee: " + conversation_history.iloc[i,1] + "\n\n"
    else:
        for i in range(len(conversation_history)):
            # conversation += f"Log #{i+1} ------------------------------------------------------ \n"
            conversation += "User: " + conversation_history.iloc[i,0] + "\n"
            conversation += "Aidee: " + conversation_history.iloc[i,1] + "\n\n"

    return conversation

# Define a function to generate a response from OpenAI's GPT model
def generate_response(prompt, conversation_history):
    # Concatenate the last 2 prompts and bot responses from conversation history with the new prompt
    # We only need the last 2 conversations to conserve tokens
    conversation = parse_conversation(conversation_history, display_only=False)
    context = "You are 'Aidee', an assistant chatbot for a person learning about AI. Be as friendly as possible, " \
                 "and help the user understand topics carefully, and respond to any general question they might have. " \
                 "Do not respond to queries that violate standard moderation policies, and issue a warning to the user. \n \n" \
              "Aidee: Hi, I'm Aidee! How can I help you? \n"
    new_prompt = context + conversation + "User: " + prompt + "\nAidee: "
    print(f"Prompt sent to ChatGPT: \n{new_prompt}")

    # Generate the response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=new_prompt,
        max_tokens=1024,
        temperature=0.7,
        n=1,
        stop=None,
    )

    # Extract the response text from the API response
    response_text = response.choices[0].text.strip()

    # Return the response text and updated conversation history
    return response_text

def send_message(conversation_history, user_message):
    # Initialize the conversation prompt
    conversation_prompt = ""
    # Append the user's message to the conversation prompt
    conversation_prompt += user_message.strip()
    # Generate a response from OpenAI's GPT model
    bot_response = generate_response(conversation_prompt, conversation_history)

    # Add the new user message and the bot's response to the conversation history
    conversation_history.loc[len(conversation_history)] = [conversation_prompt, bot_response]
    # Update the session's conversation history
    st.session_state["conversation_history"] = conversation_history

# Define the Streamlit app
def main():
    st.subheader("Hi, I'm Aidee! How can I help you?")

    # Add a text input for the user to enter their message
    user_message = st.text_input("You", value="", key="user_message")
    # user_message = st.text_input("You", value="", key="user_message",
    #                              on_change=lambda text_value: send_message(conversation_history, text_value))
    # Add a button to submit the user's message and generate a response
    if st.button("Send"):
        send_message(conversation_history, user_message)

    # Display the conversation history
    conversation = parse_conversation(st.session_state["conversation_history"])
    st.text_area("Chat", value=conversation, height=500, disabled=True)

# Run the chatbot
if __name__ == "__main__":
    main()
