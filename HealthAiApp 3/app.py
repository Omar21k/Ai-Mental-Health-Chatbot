
from openai import OpenAI
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_gpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error with OpenAI: {e}")
        return None

@app.route("/")
def home_page():
    return render_template("main.html")

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/chat', methods=['POST'])
def chat():
    print("We got here")
    data = request.get_json()
    user_message = data.get('message', '')
    print(f"Received message: {user_message}")
    
    gpt_response = chat_with_gpt(user_message)
    if gpt_response is None:
        return jsonify({"reply": f"Sorry, the AI service is currently unavailable. Please try again later or api key not working.{os.getenv('OPENAI_API_KEY')}"})
    
    
    print(f"Sending response: {gpt_response}")
    return jsonify({"reply": gpt_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)