# HealthQuote <img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/3bd1ac97-9dfc-41fa-a335-854de6c83919" />


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
