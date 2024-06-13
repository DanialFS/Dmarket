const chatMessages = document.getElementById('chat-messages');
function initialGreeting() {
    sendQuestionToServer('привет');
}

// Call the initialGreeting function when the page is loaded
document.addEventListener('DOMContentLoaded', initialGreeting);
document.getElementById('questionForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    var question = document.getElementById('questionInput').value;

    // Display user's question
    displayMessage(question, false);

    // Send the question to the server and get the response
    sendQuestionToServer(question);

    // Clear input after sending message
    document.getElementById('questionInput').value = '';
});

// Add event listeners to quick question buttons
document.querySelectorAll('.quickQuestionBtn').forEach(button => {
    button.addEventListener('click', function() {
        const question = this.textContent.trim(); // Get the button text as a question
        // Display the question in the chat
        displayMessage(question, false);
        // Send the question to the server and get the response
        sendQuestionToServer(question);
    });
});

function sendQuestionToServer(question) {
    fetch('', {  // Changed the URL to match the one in urls.py
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ question: question }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Display bot's response
        displayMessage(data.response, true);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to display messages in the chat
function displayMessage(message, isResponse) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    if (isResponse) {
        messageElement.classList.add('response');
    }

    // Find links in the message and replace them with <a> elements
    const linkRegex = /{% url '([^']+)' %}/g;
    message = message.replace(linkRegex, '<a href="$1">$1</a>');

    // Insert the processed message into the chat element
    messageElement.innerHTML = message;
    chatMessages.appendChild(messageElement);
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;

    document.getElementById('notificationSound').play();
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
