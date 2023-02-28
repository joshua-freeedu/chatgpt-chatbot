from flask import Blueprint, jsonify, request
from flask_app import generate_response, conversation_history

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

@chatbot_bp.route('', methods=['POST'])
def chatbot():
    user_message = request.json['message']
    bot_response = generate_response(user_message, conversation_history)
    return jsonify({'response': bot_response})
