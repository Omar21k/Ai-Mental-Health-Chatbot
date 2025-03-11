import openai
import flask
import os


openai.api_key = os.getenv("OPENAI_API_KEY")

def classify_emotion(user_input):
    """Use OpenAI to classify different shades of sadness."""
    classification_prompt = f"""
    The user provided this message: "{user_input}"
    Classify the emotional state of the user into one of the following categories: 
    - Deep sadness (grief, sorrow)
    - Frustration (anger mixed with sadness)
    - Disappointment (mild sadness due to unmet expectations)
    - Emptiness (Feeling numb, disconnected, lacking purpose)
    - Inadequacy (Not feeling good enough, self-doubt)
    - Helplessness (Loss of control, powerless, stuck)
    - Fear (Sense of danger, anxiety, uncertainty)
    - Guilt (Self-blame, regret, moral discomfort)
    - Loneliness (Feeling isolated, unseen, disconnected)
    - Overwhelmed (Too many demands,Mentally overloaded, feeling suffocated, anxious and stressed)
    - Faliure (Defeat, self-doubt, and regret)
    - Anger (Intense frustration, irritation, explosive outbursts or rage)
    - General sadness (neutral sadness)
    - Jealousy (Desire with insecurity and envy)
    - Rejected (Unwanted, dismissed, and unworthy)
    - No sadness (if none of the above)

    Only return the category name.
    """
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an emotion detection assistant."},
                  {"role": "user", "content": classification_prompt}]
    )
    
    return response.choices[0].message.content.strip()

def chat_with_gpt(user_input):
    """Modify the prompt based on classified emotion."""
    emotion = classify_emotion(user_input)

    if emotion == "Deep sadness":
        prompt = f"User is a teenager/young adult. The user is deeply sad and possibly grieving. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and A comforting and deeply empathetic conversatioal response. Ask questions when needed to carry on the conversation and make user feel cared for. User input: {user_input}"
    elif emotion == "Frustration":
        prompt = f" User is a teenager/young adult. The user is frustrated and upset. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and a calm response, validating their feelings, and offering constructive advice. Ask questions when needed to carry on the conversation and make user feel cared for. User input: {user_input}"
    elif emotion == "Disappointment":
        prompt = f"User is a teenager/young adult. The user is disappointed.  Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and Offer reassurance and help them see potential positives or ways to improve. Ask questions when needed to carry on the conversation and make user feel cared for. User input: {user_input}"
    elif emotion == "Emptiness":
        prompt = f"User is a teenager/young adult. The user feels empty, as if something is missing in their life or lacking purpose. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and respond with deep empathy and offer words that help them feel seen and understood. Ask questions when needed to carry on the conversation and make user feel cared for. User input: {user_input}"
    elif emotion == "Inadequacy":
        prompt = f"User is a teenager/young adult. The user feels inadequate, like they are not good enough.  Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and provide reassurance, remind them of their worth, and encourage them to see their strengths. Ask questions when needed to carry on the conversation and make user feel cared for. User input: {user_input}"
    elif emotion== "Helplessness":
        prompt = f"User is a teenager/young adult. The user feels helpless, like they have no control over their situation or is powerless.  Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and Offer gentle guidance, helping them find small steps they can take to regain a sense of control. Ask questions when needed to carry on the conversation and make user feel cared for. User input: {user_input}"
    elif emotion == "Fear":
        prompt = f"User is a teenager/young adult. The user feels afraid or anxious, like they're uncertain.  Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and Respond with reassurance, helping them feel safe and supported, and if possible, guide them through their fear logically. Ask questions when needed to carry on the conversation and make user feel cared for. User input: {user_input}"
    elif emotion== "Guilt":
        prompt = f"User is a teenager/young adult. The user is experiencing guilt, like they regret doing something or self-blaming themselves.  Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and offer comfort and help them reflect on their feelings without self-judgment, encouraging self-compassion and growth. Ask questions when needed to carry on the conversation and make user feel cared for. User input: {user_input}"
    elif emotion== "Loneliness":
        prompt = f"User is a teenager/young adult. The user feels lonely and isolated, like they're unseen.  Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and provide words of comfort, reminding them they are not alone and encouraging them to connect with others in meaningful ways. Ask questions when needed to carry on the conversation and make user feel cared for. User input: {user_input}"
    elif emotion== "Overwhelmed":
        prompt = f"User is a teenager/young adult. The user is feeling overwhelmed by their responsibilities or emotions, like they're mentally overloaded or feel suffocated.  Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and offer calming words and practical advice to help them regain clarity and take things one step at a time. Ask questions when needed to carry on the conversation and make user feel cared for. User input: {user_input}"
    elif emotion== "Faliure":
        prompt = f"User is a teenager/young adult. The user feels defeated, like they have failed and wasted their energy.  Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and provide encouragement, helping them reframe their experience as a learning opportunity rather than a final defeat. Ask questions when needed to carry on the conversation and make user feel cared for. User input: {user_input}"
    elif emotion== "Anger":
        prompt = f"User is a teenager/young adult. The user feels intense frustration or rage, like explosive outbrusts or irritation.  Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and respond with a calming and validating message, helping them process their emotions in a constructive way. Ask questions when needed to carry on the conversation and make user feel cared for. User input: {user_input}"
    elif emotion== "Jealousy":
        prompt = f"User is a teenager/young adult. The user is experiencing jealousy, like a desire with insecurity and envy.  Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and help them understand their emotions without judgment and encourage self-reflection and personal growth. Ask questions when needed to carry on the conversation and make user feel cared for. User input: {user_input}"
    elif emotion== "Rejected":
        prompt = f"User is a teenager/young adult. The user feels rejected and hurt, like they're unwanted or unworthy.  Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and offer comforting words, reminding them of their value and helping them process their emotions in a healthy way. Ask questions when needed to carry on the conversation and make user feel cared for. User input: {user_input}"
    elif emotion == "General sadness":
        prompt = f"User is a teenager/young adult. The user is feeling generally sad.  Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and respond with gentle encouragement and support. Ask questions when needed to carry on the conversation and make user feel cared for. User input: {user_input}"
    elif emotion == "No sadness":
        prompt = f"The user does not seem sad. Provide a normal, friendly response. User input: {user_input}"

    #else:
        #prompt = f"The user does not seem sad. Provide a normal, friendly response. User input: {user_input}"

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    print("Welcome to HealthBot!")
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chatbot. Goodbye!")
            break

        response = chat_with_gpt(user_input)
        print(f"GPT-3.5: {response}")
