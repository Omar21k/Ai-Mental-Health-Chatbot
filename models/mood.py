import openai
from nltk.sentiment import SentimentIntensityAnalyzer

import requests
import random

_TAG_CACHE = {"tags": None}

def get_available_tags():
    if _TAG_CACHE["tags"] is None:
        try:
            resp = requests.get("https://quoteslate.vercel.app/api/tags", timeout=8)
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

FALLBACK_QUOTES = [
    {"quote": "The only way out is through.", "author": "Robert Frost"},
    {"quote": "You are stronger than you know.", "author": "Unknown"},
    {"quote": "This too shall pass.", "author": "Persian Proverb"},
    {"quote": "Every storm runs out of rain.", "author": "Maya Angelou"},
]

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
    """Fetch a real, attributed quote from QuoteSlate matched to the emotion.
    Always returns something — falls back to local quotes if the API is unreachable
    or rate-limited."""
    tags = find_matching_tags(emotion, get_available_tags())

    def _try_request(params):
        resp = requests.get("https://quoteslate.vercel.app/api/quotes/random", params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            data = data[0]
        return {"quote": data["quote"], "author": data["author"]}

    if tags:
        try:
            return _try_request({"count": 1, "tags": ",".join(tags)})
        except Exception as e:
            print(f"Tagged quote fetch failed: {e}")

    try:
        return _try_request({"count": 1})
    except Exception as e:
        print(f"Untagged quote fetch failed: {e}")

    return random.choice(FALLBACK_QUOTES)

def classify_emotion(user_input, history_text=""):
    """Use OpenAI to classify different shades of sadness."""
    classification_prompt = f"""
    Conversation so far:
    {history_text}

    The user's latest message: "{user_input}"

    Classify the emotional state of the user's LATEST message, using the conversation 
    so far for context, into one of the following categories:
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
    Be conservative: only choose a specific emotion category if the message expresses a clear, 
    substantial feeling or situation. Brief, mild, or ambiguous statements (e.g., "I'm a bit tired", 
    "not bad I guess", "long day") should be classified as "No sadness" — these need a 
    supportive follow-up question first, not a full emotional response.
    If the conversation history shows this topic has already been discussed and the user is now 
    asking a follow-up question or requesting advice, still classify based on their underlying 
    emotional state, not "No sadness" just because it's a follow-up.
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
        word_count = len(user_input.split())
        continuation_keywords = ["advice", "help", "what should i do", "any tips",
                                  "how do i", "any suggestions", "what do you think", "should i"]
        is_continuation_request = any(kw in user_input.lower() for kw in continuation_keywords)
        if word_count < 6 and emotion != "No sadness" and not (history_text and is_continuation_request):
            emotion = "No sadness"
        valid_emotions = {
            "Deep sadness", "Frustration", "Disappointment", "Emptiness", "Inadequacy",
            "Helplessness", "Fear", "Guilt", "Loneliness", "Overwhelmed", "Faliure",
            "Anger", "General sadness", "Jealousy", "Rejected", "No sadness"
        }

        if emotion not in valid_emotions:
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

        return emotion

    except Exception as e:
        print(f"Error in emotion classification: {e}")
        return "No sadness"

def analyze_mood(text, history_text=""):
    """Get detailed emotion analysis."""
    return classify_emotion(text, history_text)

def get_emotion_prompt(emotion, user_input, quote_data, history_text=""):
    already_quoted = "<blockquote>" in history_text

    if quote_data and not already_quoted:
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
    1. Do NOT include a quote or ask "tell me more" if the conversation history shows this topic 
       has already been discussed — instead, directly engage with what the user is asking now
    2. If the user is asking for advice, give genuine, concrete, practical suggestions
    3. Offer continued comfort and validation tied to their specific situation
    4. Never give medical advice
        """
        quote_text = "None — do not mention a quote."

    base_instructions = f"""
    You are a supportive mental health AI assistant having an ongoing conversation. Your response must:
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
    Conversation so far:
    {history_text}

    User's latest message: {user_input}
    """

def get_gpt_response(user_input, emotion, history_text=""):
    already_quoted = "<blockquote>" in history_text
    quote_data = None if already_quoted else fetch_real_quote(emotion)
    prompt = get_emotion_prompt(emotion, user_input, quote_data, history_text)

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
