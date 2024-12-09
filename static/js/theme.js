// Theme handling
document.addEventListener('DOMContentLoaded', function () {
    const themeToggleButton = document.getElementById('theme-toggle');
    const darkIcon = document.getElementById('theme-toggle-dark-icon');
    const lightIcon = document.getElementById('theme-toggle-light-icon');

    // Function to set theme
    function setTheme(isDark) {
        if (isDark) {
            // Light theme using standard Tailwind colors
            document.documentElement.classList.add('dark');
            darkIcon.classList.add('hidden');
            lightIcon.classList.remove('hidden');
            document.body.classList.remove('bg-gray-900');
            document.body.classList.add('bg-white');

            const chatContainer = document.querySelector('#chatBox').parentElement;
            chatContainer.classList.remove('bg-gray-800');
            chatContainer.classList.add('bg-gray-100', 'border', 'border-gray-200');

            const inputContainer = document.querySelector('form').parentElement;
            inputContainer.classList.remove('bg-gray-800', 'border-gray-700');
            inputContainer.classList.add('bg-gray-100', 'border-gray-200');

            const inputField = document.querySelector('#messageInput');
            inputField.classList.remove('bg-gray-700', 'border-gray-600', 'text-white', 'placeholder-gray-400');
            inputField.classList.add('bg-white', 'border-gray-300', 'text-gray-800', 'placeholder-gray-500',
                'focus:border-blue-500', 'focus:ring-blue-500');

            const messages = document.querySelectorAll('.message');
            messages.forEach(message => {
                if (message.classList.contains('ml-auto')) { // User message
                    if (isDark) {
                        message.classList.remove('bg-blue-500', 'hover:bg-blue-600');
                        message.classList.add('bg-blue-600', 'text-white');
                    } else {
                        message.classList.remove('bg-blue-600');
                        message.classList.add('bg-blue-500', 'text-gray-800', 'hover:bg-blue-600');
                    }
                } else { // AI message
                    if (isDark) {
                        message.classList.remove('bg-gray-100', 'text-gray-800');
                        message.classList.add('bg-gray-700', 'text-gray-100');
                    } else {
                        message.classList.remove('bg-gray-700', 'text-gray-100');
                        message.classList.add('bg-gray-100', 'text-gray-800');
                    }
                }
            });
        } else {
            document.documentElement.classList.remove('dark');
            lightIcon.classList.add('hidden');
            darkIcon.classList.remove('hidden');

            // Dark theme colors
            document.body.classList.remove('bg-white');
            document.body.classList.add('bg-gray-900');

            const chatContainer = document.querySelector('#chatBox').parentElement;
            chatContainer.classList.remove('bg-gray-100', 'border', 'border-gray-200');
            chatContainer.classList.add('bg-gray-800');

            const inputContainer = document.querySelector('form').parentElement;
            inputContainer.classList.remove('bg-gray-100', 'border-gray-200');
            inputContainer.classList.add('bg-gray-800', 'border-gray-700');

            const inputField = document.querySelector('#messageInput');
            inputField.classList.remove('bg-white', 'border-gray-300', 'text-gray-800', 'placeholder-gray-500',
                'focus:border-blue-500', 'focus:ring-blue-500');
            inputField.classList.add('bg-gray-700', 'border-gray-600', 'text-white', 'placeholder-gray-400');

            const messages = document.querySelectorAll('.message');
            messages.forEach(message => {
                if (message.classList.contains('ml-auto')) {
                    message.classList.remove('bg-blue-500', 'hover:bg-blue-600');
                    message.classList.add('bg-blue-600');
                } else {
                    message.classList.remove('bg-white', 'text-gray-800', 'border', 'border-gray-200');
                    message.classList.add('bg-gray-700', 'text-gray-100');
                }
            });
        }
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    }

    // Initialize theme
    const storedTheme = localStorage.getItem('theme');
    if (storedTheme) {
        setTheme(storedTheme === 'dark');
    } else {
        setTheme(true);
    }

    // Toggle theme on button click
    themeToggleButton.addEventListener('click', () => {
        const isDark = !document.documentElement.classList.contains('dark');
        setTheme(isDark);
    });
}); 