from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
# from routes import chatbot_bp

import openai
import os
import pandas as pd

app = Flask(__name__)
CORS(app)

# Set up the OpenAI API key
openai.api_key = os.environ["FREEEDU_OPENAI_API_KEY"]

# @app.get("/")
# def index_get():
#     return render_template("base.html")

@app.post("/chat")
def send_message():
# def send_message(user_message, chat_history):
    # Get the message and history from the POST request
    user_message = request.get_json().get("messages")

    # Generate a response from OpenAI's GPT model
    bot_response = generate_response(user_message)

    # Add the new user message and the bot's response to the chat history
    # chat_history.loc[len(chat_history)] = [user_message, bot_response]

    # # Update the session's chat history
    # user[user_id].get("chat_history") = chat_history

    message = {"answer": bot_response}
    return jsonify(message)

def parse_chat(chat_history, count_from_last = 10):
    chat = ""
    if len(chat_history) > count_from_last:
        for i in range((len(chat_history)-1) - (count_from_last-1), len(chat_history)):
            chat += chat_history[i]['name'] + ": " + chat_history[i]['message'] + "\n"
    else:
        for i in range(len(chat_history)):
            chat += chat_history[i]['name'] + ": " + chat_history[i]['message'] + "\n"

    return chat

def generate_response(user_message):
    chat = parse_chat(user_message)
    context = "You are 'Aidee', an assistant chatbot for a person learning about AI. Be as friendly as possible, " \
                 "and help the user understand topics carefully, and respond to any general question they might have. " \
                 "Do not respond to queries that violate standard moderation policies, and issue a warning to the user. \n \n"
    new_prompt = context + chat + "Aidee: "
    print(f"Prompt sent to ChatGPT: \n{new_prompt}")

    # Generate the response
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=new_prompt,
        max_tokens=1024,
        temperature=0.7,
        n=1,
        stop=None,
    )

    # Extract the response text from the API response
    response_text = response.choices[0].text.strip()
    # Return the response text and updated chat history
    return response_text

if __name__ == "__main__":
    app.run(debug=True)