import openai
openai.api_key = "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"
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