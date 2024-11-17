document.addEventListener('DOMContentLoaded', function() {
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

    // Initial scroll and button state
    scrollToBottom();
    toggleSubmitButton();

    // Listen for input changes
    messageInput.addEventListener('input', toggleSubmitButton);

    // Handle Enter key
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey && messageInput.value.trim()) {
            e.preventDefault();
            messageForm.submit();
        }
    });

    // Handle new content added to chat
    document.body.addEventListener('htmx:afterSwap', function(e) {
        if (e.detail.target.id === 'chatBox') {
            scrollToBottom();
        }
    });

    // Clear input after successful submission
    messageForm.addEventListener('htmx:afterRequest', function(e) {
        if (e.detail.successful) {
            messageInput.value = '';
            toggleSubmitButton();
        }
    });
}); 