# Ai-Mental-Health-Chatbot

## Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/Health_Ai_App.git
    cd Health_Ai_App
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your OpenAI API key:

    ```plaintext
    OPENAI_API_KEY=your_openai_api_key
    ```

5. Run the Flask application:

    ```sh
    python app.py
    ```

6. Open your browser and go to `http://127.0.0.1:5000/` to see the application.

## Usage

- Type a message in the input field and press Enter or click the send button to interact with the chatbot.

## License

This project is licensed under the MIT License.

## API Keys




app.py: save code:

import openai
from flask_httpauth import HTTPBasicAuth
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv 
import database 

from models.mood import analyze_mood
from models.info import app_description

database.create_database() 
user_id = "1" #Replace with function to classify user
load_dotenv()

app = Flask(__name__)
auth = HTTPBasicAuth()
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error with OpenAI: {e}")
        return None

users = {
    "john": "hello",
    "susan": "bye"
}

@auth.verify_password
def verify_password(username, password):
    actual_password = users.get(username)
    if actual_password == password: 
        return username
   

@app.route("/")
@auth.login_required
def home_page():
    print(auth.current_user())
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
    
    gpt_response = chat_with_gpt(user_message)
    if gpt_response is None:
        return jsonify({"reply": f"Sorry, the AI service is currently unavailable. Please try again later or api key not working.{os.getenv('OPENAI_API_KEY')}"})
    
    
    print(f"Sending response: {gpt_response}")
    database.logger(user_id, user_message, gpt_response)
    return jsonify({"reply": gpt_response})   

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5001, debug=True)

