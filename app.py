
from openai import OpenAI
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv 
import database 

database.create_database() 

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

users = {
    "samir": "rad",
    "omar": "cool", 
    "faraja":"awesome"
}

@auth.verify_password
def verify_password(username, password):
    actual_password = users.get(username) 
    if username not in users: 
        users[username] = password
        return username
    if actual_password == password: 
        return username 
    
user_id = verify_password()

def chat_with_gpt(user_id, user_message):
    try:
        conversation_history = database.grabber(user_id)
        prompt = f"""
        You are a supportive mental health chatbot. Provide empathetic and caring responses. Your auidences age varies from teens to young adults. If a prompt is very vague please ask empathetic follow-up questions.
        
        Conversation History:
        {conversation_history}

        User: {user_message}
        Bot:
        """
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error with OpenAI: {e}")
        return None



@app.route("/")
@auth.login_required
def home_page():
    return render_template("main.html")

@app.route('/static/<path:filename>')
@auth.login_required
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/chat', methods=['POST'])
@auth.login_required
def chat():
    print("We got here")
    data = request.get_json()
    user_message = data.get('message', '')
    print(f"Received message: {user_message}")
    
    gpt_response = chat_with_gpt(user_id, user_message)
    if gpt_response is None:
        return jsonify({"reply": f"Sorry, the AI service is currently unavailable. Please try again later or api key not working.{os.getenv('OPENAI_API_KEY')}"})
    
    
    print(f"Sending response: {gpt_response}")
    database.logger(user_id, user_message, gpt_response)
    return jsonify({"reply": gpt_response})   

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000, debug=True)
