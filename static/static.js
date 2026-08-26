let conversationHistory = [];

function displayMessage(message, sender) {
    const chatContainer = document.getElementById('chat-container');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    if (sender === 'user') {
        messageDiv.textContent = message;
    } else {
        messageDiv.innerHTML = message;
    }
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function fetchQuote(userMessage) {
    console.log('Fetching quote for message:', userMessage);
    fetch('/quote', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Received quote response:', data);
        const quoteContainer = document.getElementById('quote');
        quoteContainer.innerHTML = `<p class="quote-text">${data.quote}</p>`;
    })
    .catch(error => console.error('Error fetching quote:', error));
}

// Emotion to emoji mapping
const emotionEmojis = {
    "Deep sadness": "😢",
    "Frustration": "😤",
    "Disappointment": "😔",
    "Emptiness": "😶",
    "Inadequacy": "😟",
    "Helplessness": "😰",
    "Fear": "😨",
    "Guilt": "😣",
    "Loneliness": "🥺",
    "Overwhelmed": "😫",
    "Faliure": "😩",
    "Anger": "😠",
    "General sadness": "😕",
    "Jealousy": "😒",
    "Rejected": "💔",
    "No sadness": "😊"
};

function updateMoodEmoji(emotion) {
    const emojiElement = document.getElementById('mood-emoji');
    const newEmoji = emotionEmojis[emotion] || "😊";
    
    gsap.to(emojiElement, {
        opacity: 0,
        y: -20,
        duration: 0.3,
        onComplete: () => {
            emojiElement.textContent = newEmoji;
            gsap.to(emojiElement, {
                opacity: 1,
                y: 0,
                duration: 0.3,
                ease: "back.out"
            });
        }
    });
}

async function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return;
    displayMessage(userInput, 'user');
    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: userInput, history: conversationHistory }),
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log('Received response with emotion:', data.emotion);
        if (data.error) {
            displayMessage("Sorry, I encountered an error. Please try again.", 'bot');
        } else {
            if (data.emotion) {
                console.log('Updating emoji for emotion:', data.emotion);
                updateMoodEmoji(data.emotion);
            }
            await displayBotReplyInBubbles(data.reply);
            conversationHistory.push({ role: 'user', content: userInput });
            conversationHistory.push({ role: 'bot', content: data.reply });
            if (conversationHistory.length > 20) {
                conversationHistory = conversationHistory.slice(-20);
            }
        }
    } catch (error) {
        console.error("Error:", error);
        displayMessage("Sorry, I encountered an error. Please try again.", 'bot');
    }
    document.getElementById("user-input").value = "";
}

document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});
