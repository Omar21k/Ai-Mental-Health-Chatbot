# HealthQuote


HealthQuote is a full-stack AI-powered mental health chatbot designed to provide users with supportive, context-aware conversations and personalized quotes based on their situation.

The application analyzes the emotional context of a user's message, generates a conversational response using the OpenAI API, and connects the user with a relevant quote through an external quote service. HealthQuote also supports user accounts and conversation history so users can return to previous conversations.

🌐 **Live Application:** [HealthQuote](https://healthquote.life/)

---

## Features

-  **AI-Powered Chatbot**  
  Uses the OpenAI API to generate context-aware conversational responses.

-  **Emotion Classification**  
  Uses NLTK to classify the emotional context of user messages and help tailor responses.

-  **Personalized Quotes**  
  Connects to an external quote service to provide not just "a" quote but THE tailored exactly to the user's situation.

-  **Quote Explanations**  
  Explains how the selected quote relates to the user's situation rather than simply displaying a quote.

-  **User Authentication**  
  Allows users to create accounts and securely access their conversations.

-  **Conversation History**  
  Stores conversation data and allows users to retrieve previous conversations across sessions.


-  **Live Deployment**  
  Deployed as a live web application using Render.

---

## How It Works

The general flow of HealthQuote is:

```text
User
  ↓
Frontend
  ↓
Flask Backend
  ↓
Emotion Classification (NLTK)
  ↓
OpenAI API
  ↓
Quote Service
  ↓
Context-Aware Response + Relevant Quote
  ↓
Conversation History
 ```


1. User Input

The user sends a message through the HealthQuote web interface.

2. Backend Processing

The request is sent to the Flask backend, which handles the application logic and user session.

3. Emotion Classification

NLTK analyzes the user's message to identify its emotional context.

4. AI Response

The backend sends the relevant conversation context to the OpenAI API to generate a conversational response.

5. Quote Recommendation

HealthQuote connects to an external quote service to retrieve a quote relevant to the user's situation.

6. Personalized Response

The chatbot returns the AI-generated response along with the selected quote and an explanation of how the quote relates to the user's situation.

7. Conversation History

For authenticated users, conversations are stored and can be retrieved across sessions.
