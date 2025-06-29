from flask import Flask, request, jsonify, send_from_directory
from pymongo import MongoClient
from bson import ObjectId, json_util
from dotenv import load_dotenv
import os
import nltk
from nltk.chat.util import Chat, reflections
from flask_cors import CORS

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
conversations = db.conversations

# Simple NLTK chatbot
chatbot = Chat([
    (r'hi|hello', ['Hello!', 'Hey there!']),
    (r'how are you?', ['I\'m good!', 'All systems go!']),
    (r'(.*) your name?', ['I\'m a Flask chatbot!']),
], reflections)

@app.route('/')
def index():
    return "Welcome to the Chatbot API"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    bot_response = chatbot.respond(user_message) or "I didn't understand that"
    conversation = {
        "user": user_message,
        "bot": bot_response
    }
    conversations.insert_one(conversation)
    return jsonify({"response": bot_response})

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
