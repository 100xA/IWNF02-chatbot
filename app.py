from flask import Flask, render_template, request, jsonify
import markdown2
import logging
import google.generativeai as genai
from http import HTTPStatus
from google.api_core import retry
import time
from os import environ
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

app = Flask(__name__, static_url_path='/static')

# Load environment variables
load_dotenv()

SUPPORT_KEYWORDS ={
  'technical': [
        'error', 'bug', 'issue', 'problem', 'broken', "doesn't work", 
        'help', 'how to', 'how do I', 'stuck', 'trouble'
    ],
    'account': [
        'login', 'password', 'account', 'sign in', 'signup', 'register',
        'authentication', 'forgot', 'reset'
    ],
    'billing': [
        'payment', 'charge', 'bill', 'invoice', 'subscription', 'price',
        'refund', 'cost', 'plan'
    ],
    'product': [
        'feature', 'function', 'use', 'using', 'install', 'setup',
        'configure', 'settings', 'upgrade'
    ]
}


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY environment variable is not set")
    raise ValueError("GEMINI_API_KEY environment variable is required")

genai.configure(api_key=GEMINI_API_KEY)

class ChatError: 
    API_ERROR = {
        "message": "I apologize, but I'm having trouble connecting to the AI service right now.",
        "suggestion": "Please try again in a moment. If the issue persists, check your internet connection or try refreshing the page."
    }
    RATE_LIMIT = {
        "message": "We're experiencing high traffic at the moment.",
        "suggestion": "Please wait a few seconds and try again."
    }
    VALIDATION_ERROR = {
        "message": "Please enter a message before sending.",
        "suggestion": "Type your message in the input field and try again."
    }
    GENERAL_ERROR = {
        "message": "Something unexpected happened.",
        "suggestion": "Please try again. If the problem continues, you may want to refresh the page."
    }


def is_support_message(message):
    """Check if the message is a support message"""
    message = message.lower()

    # Check each category for keywords
    for category, keywords in SUPPORT_KEYWORDS.items():
        if any(keyword in message for keyword in keywords):
            return True, category
    return False, None

def get_non_support_response(message):
    """Get a non-support response"""
    return "I'm here to help with technical, account, billing, and product support. How can I assist you today?"

def format_ai_response(response_text):
    """Convert markdown to HTML with specific features enabled"""
    extras = [
        "fenced-code-blocks",   # ```code blocks```
        "tables",               # Tables support
        "break-on-newline",     # Line breaks
        "header-ids",           # Add IDs to headers
        "strike",               # Strike-through text
        "task_list"            # Checkboxes
    ]
    
    # Convert markdown to HTML
    html = markdown2.markdown(response_text, extras=extras)
    return html

def get_gemini_response(user_message, max_retries=3):
    """Get response from Gemini with markdown formatting"""
    is_support, category = is_support_message(user_message)
    
    if not is_support:
        return format_ai_response(get_non_support_response(user_message))
    
    prompt = f"""Respond to this {category}-related support query using markdown formatting for clarity:
    
    {user_message}
    
    Format your response with:
    - Clear headers for sections
    - Bullet points or numbered lists where appropriate
    - Bold for important terms
    - Code blocks for technical commands or examples
    - Tables if comparing options
    
    Make the response clear and well-structured."""
    
    retry_count = 0
    while retry_count < max_retries:
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return format_ai_response(response.text)
            
        except Exception as e:
            retry_count += 1
            wait_time = min(2 ** retry_count, 8)  # Exponential backoff, max 8 seconds
            
            if retry_count < max_retries:
                logger.warning(f"Attempt {retry_count} failed, retrying in {wait_time}s: {str(e)}")
                time.sleep(wait_time)
                continue
                
            logger.error("Max retries reached", exc_info=True)
            raise

# Update the logging configuration
def setup_logger():
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Configure logging format
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    # File handler for general logs
    file_handler = RotatingFileHandler(
        'logs/app.log', 
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Error file handler
    error_file_handler = RotatingFileHandler(
        'logs/error.log',
        maxBytes=1024 * 1024,
        backupCount=10
    )
    error_file_handler.setFormatter(formatter)
    error_file_handler.setLevel(logging.ERROR)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_file_handler)

    # Ensure Flask's logger also gets the handlers
    app.logger.handlers = root_logger.handlers

@app.route('/')
def home():
 
    return render_template('index.html', messages=[])

@app.route('/message', methods=['POST'])
def message():
    try:
        user_message = request.form.get('message')
        
        # Log incoming request (sanitized)
        app.logger.info(
            f"Received message request. Length: {len(user_message) if user_message else 0}"
        )

        if not user_message:
            app.logger.warning("Empty message received")
            return render_template('error_message.html', 
                                error=ChatError.VALIDATION_ERROR["message"],
                                suggestion=ChatError.VALIDATION_ERROR["suggestion"])

        try:
            # Log AI request attempt
            app.logger.info("Requesting AI response")
            start_time = datetime.now()
            
            ai_response = get_gemini_response(user_message)
            
            # Log successful response
            duration = (datetime.now() - start_time).total_seconds()
            app.logger.info(f"AI response received in {duration:.2f} seconds")
            
            return render_template('message.html', 
                                message=user_message,
                                ai_response=ai_response)

        except genai.types.generation_types.BlockedPromptException as e:
            app.logger.error(f"Content filtered: {str(e)}")
            return render_template('error_message.html',
                                error="I cannot respond to that type of message",
                                suggestion="Please ensure your message follows our content guidelines")

        except Exception as api_error:
            if "429" in str(api_error):
                app.logger.warning(f"Rate limit hit: {str(api_error)}")
                return render_template('error_message.html',
                                    error=ChatError.RATE_LIMIT["message"],
                                    suggestion=ChatError.RATE_LIMIT["suggestion"])
            else:
                app.logger.error(f"API error: {str(api_error)}", exc_info=True)
                return render_template('error_message.html',
                                    error=ChatError.API_ERROR["message"],
                                    suggestion=ChatError.API_ERROR["suggestion"])

    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return render_template('error_message.html',
                            error=ChatError.GENERAL_ERROR["message"],
                            suggestion=ChatError.GENERAL_ERROR["suggestion"])

if __name__ == '__main__':
    print(get_gemini_response("Hello, how are you?"))
    app.run(debug=True)


