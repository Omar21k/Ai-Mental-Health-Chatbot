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

NLTK Python Library analyzes the user's message to identify its emotional context and classify his emotion.

4. AI Response

The backend sends the relevant conversation context to the OpenAI API to generate a conversational response, it will ask follow up questions if user message is a bit vage.

5. Quote Recommendation

Once the OpenAI API is able to classify user's emotion and grasp a hold how the user feeling it responds with not just "a" quote but THE quote tailored to user's situation.

6. Personalized Response

The chatbot returns the AI-generated response along with the selected quote and an explanation of how the quote relates to the user's situation.

7. Conversation History

Tech Stack
Frontend
HTML
CSS
JavaScript
Backend
Python
Flask
AI & Natural Language Processing
OpenAI API
NLTK
Database & Authentication
User authentication
Session management
Database persistence
Conversation history
External Services
OpenAI API
External quote service
Deployment
Render (PaaS)
Development Tools
Git
GitHub
Architecture

HealthQuote follows a full-stack frontend/backend architecture.

Frontend

The frontend provides the user interface for:

User authentication
Sending messages
Viewing chatbot responses
Viewing conversation history
Interacting with chatbot settings
Backend

The Flask backend is responsible for:

User authentication
Session management
Processing user messages
Emotion classification
Communication with external APIs
Database operations
Conversation history retrieval
AI/NLP Pipeline

HealthQuote combines NLP-based emotion classification with generative AI.

A user submits a message.
The backend processes the request.
NLTK analyzes the emotional context of the message.
The application uses the conversation context when communicating with the OpenAI API.
A relevant quote is retrieved through an external quote service.
HealthQuote returns the conversational response, quote, and explanation.
The conversation is stored for future retrieval.
