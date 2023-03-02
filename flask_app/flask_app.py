from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import openai
import os

app = Flask(__name__)
# CORS(app)

# Set up the OpenAI API key
openai.api_key = os.environ["FREEEDU_OPENAI_API_KEY"]

@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/chat")
def send_message():
# def send_message(user_message, chat_history):
    # Get the message and history from the POST request
    user_message = request.get_json().get("messages")
    print(user_message)
    # Generate a response from OpenAI's GPT model
    bot_response = generate_response(user_message)

    # Add the new user message and the bot's response to the chat history
    # chat_history.loc[len(chat_history)] = [user_message, bot_response]

    # # Update the session's chat history
    # user[user_id].get("chat_history") = chat_history

    message = {"answer": bot_response}
    return jsonify(message)

def parse_chat(chat_history, count_from_last = 10):
    chat = []
    role = {"User":"user", "Aidee":"assistant"}
    if len(chat_history) > count_from_last:
        for i in range((len(chat_history)-1) - (count_from_last-1), len(chat_history)):
            chat.append({"role":role[chat_history[i]['name']],
                         "content":chat_history[i]['message']})
    else:
        for i in range(len(chat_history)):
            chat.append({"role":role[chat_history[i]['name']],
                         "content":chat_history[i]['message']})
    return chat

def generate_response(user_message):
    chat = parse_chat(user_message)
    context = {"role":"system",
               "content":"You are 'Aidee', an assistant chatbot for a person learning about AI. Be as friendly as possible, " \
                 "and help the user understand topics carefully, and respond to any general question they might have. " \
                 "Do not respond to queries that violate standard moderation policies, and issue a warning to the user."}
    new_prompt = []
    new_prompt.append(context)
    for c in chat:
        new_prompt.append(c)
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
    response_text = response['choices'][0]['message']['content']
    # Return the response text and updated chat history
    return response_text

if __name__ == "__main__":
    app.run(debug=True)