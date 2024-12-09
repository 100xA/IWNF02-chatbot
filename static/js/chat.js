document.addEventListener('DOMContentLoaded', function () {
    const messageForm = document.getElementById('messageForm');
    const messageInput = document.getElementById('messageInput');
    const submitButton = messageForm.querySelector('button[type="submit"]');
    const chatBox = document.getElementById('chatBox');

    // Function to scroll to bottom of chat
    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Function to toggle button state
    function toggleSubmitButton() {
        submitButton.disabled = !messageInput.value.trim();
        submitButton.classList.toggle('opacity-50', !messageInput.value.trim());
        submitButton.classList.toggle('cursor-not-allowed', !messageInput.value.trim());
    }

    // Function to add thinking message
    function addThinkingMessage() {
        const thinkingDiv = document.createElement('div');
        thinkingDiv.id = 'thinking-message';
        thinkingDiv.className = 'message bg-gray-700 text-gray-100 max-w-[80%] rounded-lg p-3 mb-3';
        thinkingDiv.innerHTML = `
            <div class="font-semibold mb-1 text-sm opacity-75">AI Support Assistant</div>
            <div class="markdown-content">thinking...</div>
        `;
        chatBox.appendChild(thinkingDiv);
        scrollToBottom();
    }

    // Function to remove thinking message
    function removeThinkingMessage() {
        const thinkingMessage = document.getElementById('thinking-message');
        if (thinkingMessage) {
            thinkingMessage.remove();
        }
    }

    // Initial scroll and button state
    scrollToBottom();
    toggleSubmitButton();

    // Listen for input changes
    messageInput.addEventListener('input', toggleSubmitButton);

    // Handle Enter key
    messageInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter' && !e.shiftKey && messageInput.value.trim()) {
            e.preventDefault();
            htmx.trigger(messageForm, 'submit');
        }
    });

    // Show thinking message when request starts
    messageForm.addEventListener('htmx:beforeRequest', function (e) {
        addThinkingMessage();
    });

    // Handle new content added to chat
    document.body.addEventListener('htmx:afterSwap', function (e) {
        if (e.detail.target.id === 'chatBox') {
            removeThinkingMessage();
            scrollToBottom();
        }
    });

    // Clear input after successful submission
    messageForm.addEventListener('htmx:afterRequest', function (e) {
        if (e.detail.successful) {
            messageInput.value = '';
            toggleSubmitButton();
        }
        removeThinkingMessage();
    });
});