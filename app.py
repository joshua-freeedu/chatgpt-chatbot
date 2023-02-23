import streamlit as st
import openai
import uuid
import time
import os

# Set up the OpenAI API key
openai.api_key = os.environ["JOSHUA_FREEEDU_OPENAI_API_KEY"]

# Initialize the conversation history
st.session_state["conversation_history"] = []

# Define a function to generate a response from OpenAI's GPT model
def generate_response(prompt, conversation_history):

    # Generate the initial response
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.7,
        n=1,
        stop=None,
    )

    # Extract the response text from the API response
    response_text = response.choices[0].text.strip()

    # Update the conversation history
    conversation_history.append("User: " + prompt)
    conversation_history.append("Chatbot: " + response_text)
    st.session_state["conversation_history"] = conversation_history

    conversation_history_str =""
    for text in conversation_history:
        conversation_history_str += f"\n {text}"

    # Wait for a moment to avoid rate limiting issues
    time.sleep(0.5)
    # Return the response text and conversation history
    return response_text, conversation_history_str


# Define the Streamlit app
def main():
    st.title("ChatGPT Chatbot")
    # Initialize the conversation prompt
    conversation_prompt = ""

    # Load the conversation history from localStorage
    conversation_history = st.session_state.get("conversation_history", "")

    # Add a text input for the user to enter their message
    user_message = st.text_input("You", value="", key="user_message")

    # Add a button to submit the user's message and generate a response
    if st.button("Send"):
        # Append the user's message to the conversation prompt
        conversation_prompt += user_message.strip() + "\n"
        # Generate a response from OpenAI's GPT model
        bot_response, conversation_history = generate_response(conversation_prompt, st.session_state["conversation_history"])

    # Display the conversation history
    st.text_area("Chat", value=conversation_history, height=400, disabled=True)

# Run the chatbot
if __name__ == "__main__":
    main()