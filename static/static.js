function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return;

    // Display user message
    displayMessage(userInput, 'user');

    // Send message to backend
    fetch("http://localhost:5001/chat", {  
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userInput }),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.error) {
            displayMessage("Sorry, I encountered an error: " + data.error, 'bot');
        } else {
            displayMessage(data.reply, 'bot');
        }
    })
    .catch((error) => {
        console.error("Error:", error);
        displayMessage("Sorry, I encountered an error. Please try again.", 'bot');
    });

    // Clear input field
    document.getElementById("user-input").value = "";
}