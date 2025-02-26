import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
def chat_with_gpt(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
if __name__ == "__main__":
    print("Welcome to the GPT-3.5 Chatbot!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chatbot. Goodbye!")
            break
        response = chat_with_gpt(user_input)
        print(f"GPT-3.5: {response}")