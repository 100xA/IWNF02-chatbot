from flask import Flask, render_template, request, jsonify
import logging
import google.generativeai as genai
from http import HTTPStatus
from google.api_core import retry
import time

app = Flask(__name__, static_url_path='/static')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyCMbqiz0Xu9mSNJfCr5NS7VI9H7FJG-PZI"
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


def get_gemini_response(user_message, max_retries=3):
    """Get response from Gemini with retry logic"""
    retry_count = 0
    while retry_count < max_retries:
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(user_message)
            return response.text
            
        except Exception as e:
            retry_count += 1
            wait_time = min(2 ** retry_count, 8)  # Exponential backoff, max 8 seconds
            
            if retry_count < max_retries:
                logger.warning(f"Attempt {retry_count} failed, retrying in {wait_time}s: {str(e)}")
                time.sleep(wait_time)
                continue
                
            logger.error("Max retries reached", exc_info=True)
            raise

@app.route('/')
def home():
 
    return render_template('index.html', messages=[])

@app.route('/message', methods=['POST'])
def message():
    try:
        user_message = request.form.get('message')
        if not user_message:
            logger.warning("Empty message received")
            return render_template('error_message.html', error = ChatError.VALIDATION_ERROR["message"], suggestion = ChatError.VALIDATION_ERROR["suggestion"])
        try: 
            ai_response = get_gemini_response(user_message)
            return render_template('message.html', message=user_message, ai_response=ai_response)
        except genai.types.generation_types.BlockedPromptException as e:
            logger.error(f"Content filtered: {str(e)}")
            return render_template('error_message.html', error = "I cannot respond to that type of message", suggestion = "Please ensure your message follows our content guidelines")
        except Exception as api_error: 
            if "429" in str(api_error):
                logger.warning(f"Rate limit hit: {str(api_error)}")
                return render_template('error_message.html',
                                     error=ChatError.RATE_LIMIT["message"],
                                     suggestion=ChatError.RATE_LIMIT["suggestion"])
            else:
                logger.error(f"API error: {str(api_error)}", exc_info=True)
                return render_template('error_message.html',
                                     error=ChatError.API_ERROR["message"],
                                     suggestion=ChatError.API_ERROR["suggestion"])
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return render_template('error_message.html',
                             error=ChatError.GENERAL_ERROR["message"],
                             suggestion=ChatError.GENERAL_ERROR["suggestion"])

if __name__ == '__main__':
    print(get_gemini_response("Hello, how are you?"))
    app.run(debug=True)


