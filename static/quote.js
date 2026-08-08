document.addEventListener('DOMContentLoaded', function () {
    const quoteContainer = document.getElementById('quote');
    const FALLBACK_QUOTES = [
        { quote: "The only way to do great work is to love what you do.", author: "Steve Jobs" },
        { quote: "The best way to predict the future is to invent it.", author: "Alan Kay" },
        { quote: "You are stronger than you know.", author: "Unknown" }
    ];
    let quotes = FALLBACK_QUOTES;
    let currentQuoteIndex = 0;
    let hasStartedChat = false;

    function renderQuote() {
        const q = quotes[currentQuoteIndex];
        quoteContainer.innerHTML = `<p class="quote-text">${q.quote} — ${q.author}</p>`;
    }

    function displayNextQuote() {
        if (!hasStartedChat) {
            currentQuoteIndex = (currentQuoteIndex + 1) % quotes.length;
            renderQuote();
        }
    }

    renderQuote();

    fetch('https://quoteslate.vercel.app/api/quotes/random?count=15')
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data) && data.length > 0) {
                quotes = data;
                currentQuoteIndex = 0;
                renderQuote();
            }
        })
        .catch(error => console.error('Error fetching quote batch:', error));

    const quoteInterval = setInterval(displayNextQuote, 10000);
    window.startedChat = function() {
        hasStartedChat = true;
        clearInterval(quoteInterval);
    };
});
