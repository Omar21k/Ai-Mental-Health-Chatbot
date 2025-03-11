import openai
from nltk.sentiment import SentimentIntensityAnalyzer

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
    - Overwhelmed (Too many demands, mentally overloaded)
    - Faliure (Defeat, self-doubt, and regret)
    - Anger (Intense frustration, irritation, rage)
    - General sadness (neutral sadness)
    - Jealousy (Desire with insecurity and envy)
    - Rejected (Unwanted, dismissed, and unworthy)
    - No sadness (if none of the above)

    Only return the category name.
    """
    
    try:
        response = openai.ChatCompletion.create(  
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an emotion detection assistant."},
                {"role": "user", "content": classification_prompt}
            ]
        )
        emotion = response.choices[0].message.content.strip()
        
        
        if emotion == "Deep sadness":
            prompt = f"User is a teenager/young adult. The user is deeply sad and possibly grieving. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and A comforting and deeply empathetic conversatioal response."
        elif emotion == "Frustration":
            prompt = f"User is a teenager/young adult. The user is frustrated and upset. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and a calm response, validating their feelings, and offering constructive advice."
        elif emotion == "Disappointment":
            prompt = f"User is a teenager/young adult. The user is disappointed. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and Offer reassurance and help them see potential positives or ways to improve."
        elif emotion == "Emptiness":
            prompt = f"User is a teenager/young adult. The user feels empty, as if something is missing in their life or lacking purpose. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and respond with deep empathy and offer words that help them feel seen and understood."
        elif emotion == "Inadequacy":
            prompt = f"User is a teenager/young adult. The user feels inadequate, like they are not good enough. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and provide reassurance, remind them of their worth, and encourage them to see their strengths."
        elif emotion == "Helplessness":
            prompt = f"User is a teenager/young adult. The user feels helpless, like they have no control over their situation or is powerless. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and Offer gentle guidance, helping them find small steps they can take to regain a sense of control."
        elif emotion == "Fear":
            prompt = f"User is a teenager/young adult. The user feels afraid or anxious, like they're uncertain. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and Respond with reassurance, helping them feel safe and supported, and if possible, guide them through their fear logically."
        elif emotion == "Guilt":
            prompt = f"User is a teenager/young adult. The user is experiencing guilt, like they regret doing something or self-blaming themselves. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and offer comfort and help them reflect on their feelings without self-judgment, encouraging self-compassion and growth."
        elif emotion == "Loneliness":
            prompt = f"User is a teenager/young adult. The user feels lonely and isolated, like they're unseen. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and provide words of comfort, reminding them they are not alone and encouraging them to connect with others in meaningful ways."
        elif emotion == "Overwhelmed":
            prompt = f"User is a teenager/young adult. The user is feeling overwhelmed by their responsibilities or emotions, like they're mentally overloaded or feel suffocated. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and offer calming words and practical advice to help them regain clarity and take things one step at a time."
        elif emotion == "Faliure":
            prompt = f"User is a teenager/young adult. The user feels defeated, like they have failed and wasted their energy. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and provide encouragement, helping them reframe their experience as a learning opportunity rather than a final defeat."
        elif emotion == "Anger":
            prompt = f"User is a teenager/young adult. The user feels intense frustration or rage, like explosive outbursts or irritation. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and respond with a calming and validating message, helping them process their emotions in a constructive way."
        elif emotion == "General sadness":
            prompt = f"User is a teenager/young adult. The user is feeling generally sad. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and respond with gentle encouragement and support."
        elif emotion == "Jealousy":
            prompt = f"User is a teenager/young adult. The user is experiencing jealousy, like a desire with insecurity and envy. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and help them understand their emotions without judgment and encourage self-reflection and personal growth."
        elif emotion == "Rejected":
            prompt = f"User is a teenager/young adult. The user feels rejected and hurt, like they're unwanted or unworthy. Analyze the user's input and provide two things based on the user input: A quote suited for the situation based on the analysis and offer comforting words, reminding them of their value and helping them process their emotions in a healthy way."
        elif emotion == "No sadness":
            prompt = f"The user does not seem sad. Provide a normal, friendly response and engage them in positive conversation. User input: {user_input}"
        else:
            
            sia = SentimentIntensityAnalyzer()
            sentiment = sia.polarity_scores(user_input)
            if sentiment['compound'] <= -0.5:
                emotion = "Deep sadness"
            elif sentiment['compound'] < -0.2:
                emotion = "General sadness"
            elif sentiment['compound'] < 0:
                emotion = "Disappointment"
            else:
                emotion = "No sadness"
            prompt = f"The user seems to be feeling {emotion}. Provide an appropriate supportive response."
            
        return emotion, prompt
        
    except Exception as e:
        print(f"Error in emotion classification: {e}")
        return "No sadness", "Provide a friendly and supportive response."

def analyze_mood(text):
    """Get detailed emotion analysis."""
    emotion, prompt = classify_emotion(text)
    return emotion

def get_emotion_prompt(emotion, user_input):
    """Generate appropriate prompt based on emotional state."""
    base_instructions = """
    You are a supportive mental health AI assistant. Your responses should:
    1. Show deep empathy and understanding
    2. Validate their emotions
    3. ALWAYS ask at least one relevant follow-up question
    4. Keep responses conversational and warm
    5. Provide gentle encouragement
    6. Only include an inspirational quote if the user is expressing strong emotions or seeking motivation
    7. When including a quote, format it as: <blockquote>quote text</blockquote>
    8. Focus on active listening and understanding
    9. Never give medical advice
    10. Look for patterns in their responses to provide better support
    
    Important: Do not include quotes for casual greetings or simple questions.
    Only include quotes when they would genuinely help the emotional situation.
    """
    
    emotion_prompts = {
        "Deep sadness": "The user is experiencing deep sadness or grief. First validate their pain, then offer gentle comfort and ask about their support system.",
        "Frustration": "The user is frustrated. Acknowledge their feelings, help identify the source, and explore constructive ways to handle it.",
        "Disappointment": "The user is disappointed. Show understanding, help reframe the situation, and ask about their hopes going forward.",
        "Emptiness": "The user feels empty or disconnected. Help them explore these feelings and ask about what usually brings them joy or meaning.",
        "Inadequacy": "The user feels inadequate. Validate their worth, highlight their strengths, and ask about their achievements.",
        "Helplessness": "The user feels helpless. Break things down into smaller, manageable steps and ask about what they can control.",
        "Fear": "The user is afraid. Create a safe space, validate their concerns, and explore the root of their fears.",
        "Guilt": "The user feels guilty. Help them process without judgment and ask about self-forgiveness.",
        "Loneliness": "The user feels lonely. Show they're not alone, and ask about potential connections in their life.",
        "Overwhelmed": "The user is overwhelmed. Help them prioritize and ask about immediate pressure points.",
        "Failure": "The user feels like a failure. Reframe setbacks as learning opportunities and ask about their goals.",
        "Anger": "The user is angry. Validate their feelings while exploring healthy expression and ask about triggers.",
        "General sadness": "The user is feeling down. Offer gentle support and ask about what might help lift their spirits.",
        "Jealousy": "The user is feeling jealous. Explore these feelings without judgment and ask about their own journey.",
        "Rejected": "The user feels rejected. Reinforce their inherent worth and ask about their support network.",
        "No sadness": "Engage in supportive conversation and ask about their general wellbeing."
    }
    
    specific_prompt = emotion_prompts.get(emotion, emotion_prompts["No sadness"])
    return f"{base_instructions}\n\nContext: {specific_prompt}\n\nUser input: {user_input}\n\nProvide a response that includes:\n1. A relevant quote\n2. Empathetic understanding\n3. At least one thoughtful follow-up question"

def get_gpt_response(user_input, emotion):
    """Get GPT response based on emotional state."""
    prompt = get_emotion_prompt(emotion, user_input)
    
    try:
        response = openai.ChatCompletion.create(  
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an empathetic mental health support assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error getting GPT response: {e}")
        return None
