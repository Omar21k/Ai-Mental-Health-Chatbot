import openai
from nltk.sentiment import SentimentIntensityAnalyzer

import requests

_TAG_CACHE = {"tags": None}

def get_available_tags():
    if _TAG_CACHE["tags"] is None:
        try:
            resp = requests.get("https://quoteslate.vercel.app/api/tags", timeout=5)
            resp.raise_for_status()
            _TAG_CACHE["tags"] = resp.json()
        except Exception as e:
            print(f"Error fetching QuoteSlate tags: {e}")
            _TAG_CACHE["tags"] = []
    return _TAG_CACHE["tags"]

EMOTION_KEYWORDS = {
    "Deep sadness": ["grief", "sad", "loss", "sorrow", "healing"],
    "Frustration": ["frustration", "anger", "patience", "perseverance"],
    "Disappointment": ["disappointment", "hope", "resilience"],
    "Emptiness": ["purpose", "meaning", "life"],
    "Inadequacy": ["confidence", "worth", "growth"],
    "Helplessness": ["strength", "courage", "control"],
    "Fear": ["fear", "courage", "bravery"],
    "Guilt": ["forgiveness", "guilt", "growth"],
    "Loneliness": ["loneliness", "friendship", "connection"],
    "Overwhelmed": ["calm", "peace", "balance"],
    "Faliure": ["failure", "success", "perseverance"],
    "Anger": ["anger", "patience", "calm"],
    "General sadness": ["sadness", "hope", "encouragement"],
    "Jealousy": ["jealousy", "envy", "growth"],
    "Rejected": ["rejection", "worth", "resilience"],
}

def find_matching_tags(emotion, available_tags):
    if not available_tags:
        return []
    keywords = EMOTION_KEYWORDS.get(emotion, ["life"])
    matched = []
    for kw in keywords:
        for tag in available_tags:
            if kw in tag.lower() and tag not in matched:
                matched.append(tag)
    return matched[:3]

def fetch_real_quote(emotion):
    """Fetch a real, attributed quote from QuoteSlate matched to the emotion."""
    tags = find_matching_tags(emotion, get_available_tags())
    params = {"count": 1}
    if tags:
        params["tags"] = ",".join(tags)
    try:
        resp = requests.get("https://quoteslate.vercel.app/api/quotes/random", params=params, timeout=5)
        if resp.status_code == 400:
            resp = requests.get("https://quoteslate.vercel.app/api/quotes/random", params={"count": 1}, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            data = data[0]
        return {"quote": data["quote"], "author": data["author"]}
    except Exception as e:
        print(f"Error fetching quote: {e}")
        return None

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

    If the message is a greeting, small talk, or contains no real emotional content, always classify it as "No sadness."
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

def get_emotion_prompt(emotion, user_input, quote_data):
    if quote_data:
        quote_instruction = """
    1. Open by presenting the quote exactly as given, formatted as: <blockquote>quote text — Author Name</blockquote>
    2. Explain specifically how this quote relates to what the user just shared — be concrete, not generic
    3. Offer genuine comfort and validation tied to their specific situation
    4. End with one warm, relevant follow-up question
    5. Never give medical advice
        """
        quote_text = f'"{quote_data["quote"]}" — {quote_data["author"]}'
    else:
        quote_instruction = """
    1. Offer genuine comfort and validation tied to their specific situation
    2. End with one warm, relevant follow-up question
    3. Never give medical advice
        """
        quote_text = "None available — do not mention a quote or reference one."

    base_instructions = f"""
    You are a supportive mental health AI assistant. Your response must:
    {quote_instruction}
    """
    emotion_context = {
        "Deep sadness": "The user is experiencing deep sadness or grief.",
        "Frustration": "The user is frustrated.",
        "Disappointment": "The user is disappointed.",
        "Emptiness": "The user feels empty or disconnected.",
        "Inadequacy": "The user feels inadequate.",
        "Helplessness": "The user feels helpless.",
        "Fear": "The user is afraid.",
        "Guilt": "The user feels guilty.",
        "Loneliness": "The user feels lonely.",
        "Overwhelmed": "The user is overwhelmed.",
        "Faliure": "The user feels like a failure.",
        "Anger": "The user is angry.",
        "General sadness": "The user is feeling down.",
        "Jealousy": "The user is feeling jealous.",
        "Rejected": "The user feels rejected.",
    }.get(emotion, "The user is going through something difficult.")

    return f"""{base_instructions}

    Context: {emotion_context}
    Quote to use: {quote_text}
    User input: {user_input}
    """

def get_gpt_response(user_input, emotion):
    quote_data = fetch_real_quote(emotion)
    prompt = get_emotion_prompt(emotion, user_input, quote_data)

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
