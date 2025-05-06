document.getElementById("sendButton").addEventListener("click", function () {
    const userInput = document.getElementById("userInput").value;

    if (userInput.trim() === "") return;

    // Append user message to chatbot body
    const userMessageDiv = document.createElement("div");
    userMessageDiv.classList.add("user-message");
    userMessageDiv.innerHTML = `<p>${userInput}</p>`;
    document.getElementById("chatbotBody").appendChild(userMessageDiv);

    // Clear input field
    document.getElementById("userInput").value = "";

    // Scroll to the latest message
    const chatbotBody = document.getElementById("chatbotBody");
    chatbotBody.scrollTop = chatbotBody.scrollHeight;

    // Show typing indicator
    const typingIndicator = document.createElement("div");
    typingIndicator.classList.add("bot-message", "typing-indicator");
    typingIndicator.id = "typingIndicator";
    typingIndicator.innerHTML = `<span></span><span></span><span></span>`;
    chatbotBody.appendChild(typingIndicator);
    chatbotBody.scrollTop = chatbotBody.scrollHeight;

    // Simulate a delay before sending the request to the backend
    setTimeout(() => {
        fetch("api/chatbot/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"), // Django's CSRF token
            },
            body: JSON.stringify({ message: userInput }),
        })
            .then((response) => response.json())
            .then((data) => {
                // Remove typing indicator
                const typingDiv = document.getElementById("typingIndicator");
                if (typingDiv) {
                    typingDiv.remove();
                }

                // Append bot response to chatbot body
                const botMessageDiv = document.createElement("div");
                botMessageDiv.classList.add("bot-message");
                botMessageDiv.innerHTML = `<p>${data.response}</p>`;
                chatbotBody.appendChild(botMessageDiv);

                // Scroll to the latest message
                chatbotBody.scrollTop = chatbotBody.scrollHeight;
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    }, 1000); // Adjust the delay time (1 second here) for the typing effect
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}