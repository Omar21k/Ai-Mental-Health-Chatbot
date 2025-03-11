document.addEventListener('DOMContentLoaded', function () {
    const quoteContainer = document.getElementById('quote');
    const quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "The best way to predict the future is to invent it. - Alan Kay",
        "Life is 10% what happens to us and 90% how we react to it. - Charles R. Swindoll",
        "Your time is limited, don't waste it living someone else's life. - Steve Jobs",
        "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt"
    ];

    let currentQuoteIndex = 0;
    let hasStartedChat = false;

    function displayNextQuote() {
        if (!hasStartedChat) {
            currentQuoteIndex = (currentQuoteIndex + 1) % quotes.length;
            quoteContainer.innerHTML = `<p class="quote-text">${quotes[currentQuoteIndex]}</p>`;
        }
    }


    quoteContainer.innerHTML = `<p class="quote-text">${quotes[0]}</p>`;

    // Only start the quote rotation if no chat has occurred
    const quoteInterval = setInterval(displayNextQuote, 10000);

    window.startedChat = function() {
        hasStartedChat = true;
        clearInterval(quoteInterval);
    };
});