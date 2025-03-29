from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session
from flask_cors import CORS
from flask_session import session
import os
import ssl
import nltk
import openai
from dotenv import load_dotenv 
import database 
from models.mood import analyze_mood, get_gpt_response
from models.user import verify_user
from models.chat import chat_manager  

load_dotenv()
database.create_database() 
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-key-123')  
CORS(app)
session(app)
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_gpt(user_message, username=None, include_description=False):
    try:
        conversation_history = database.grabber(username)

        prompt = f"""
        You are a supportive mental health chatbot. Provide empathetic and caring responses.
        If a prompt is vague, ask empathetic follow-up questions.

        Conversation History:
        {conversation_history}

        User: {user_message}
        Bot:
        """
        emotion = analyze_mood(user_message) if user_message else "neutral" 
        response = openai.chatcompletions.create(  # Updated to use direct openai call
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an empathetic mental health support assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error with chat: {e}")
        return None



@app.route("/")
def home_page():
    return render_template('landing_page.html')

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if database.verify(username, password):
            session['username'] = username
            return redirect(url_for('chat_page'))
        else:
            return render_template("loginPage.html", error="Invalid credentials")
    return render_template("loginPage.html")

@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if database.register(username, password):
            return redirect(url_for('login_page'))
        return render_template("signupPage.html", error="Username already exists")
    
    return render_template("signupPage.html")

@app.route('/chat')
def chat_page():
    username = session.get('username')
    initial_response = "Hi! I'm here to listen and support you. How are you feeling today?"
    initial_quote = chat_manager.get_default_quote()
    
    # Allow access even without login: for isuse cuz something it doesn't work
    if not username:
        username = "Guest"
    
    return render_template("main.html", initial_response=initial_response, quote=initial_quote, username=username)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    username = session.get('username', 'Guest')
    
    # Get emotion first
    emotion = analyze_mood(user_message)
    gpt_response = chat_with_gpt(user_message, username=username)
    
    if gpt_response is None:
        error_message = "Sorry, the AI service is currently unavailable."
        return jsonify({"reply": error_message})
    
   
    response_data = {
        "reply": gpt_response,
        "emotion": emotion  
    }
    
    if username != 'Guest':
        try:
            database.logger(username, user_message, gpt_response)
        except Exception as e:
            print(f"Logging error: {e}")
    
    return jsonify(response_data)

@app.route('/quote', methods=['POST'])
def quote():
    data = request.get_json()
    user_message = data.get('message', '')
    print(f"Received message for quote: {user_message}")
    
    # use the  mood file for quote reply
    mood = analyze_mood(user_message)
    quote_prompt = chat_manager.generate_quote_prompt(user_message, mood)
    
    quote_response = chat_with_gpt(quote_prompt)
    if quote_response is None:
        error_message = "Sorry, the AI service is currently unavailable. Please try again later."
        print(error_message)
        return jsonify({"quote": error_message})
    
    print(f"Sending quote response: {quote_response}")
    return jsonify({"quote": quote_response})

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5001, debug=True)