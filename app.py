from flask import Flask, render_template, request, jsonify
import logging
import google.generativeai as genai
from http import HTTPStatus
import time

app = Flask(__name__, static_url_path='/static')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyCMbqiz0Xu9mSNJfCr5NS7VI9H7FJG-PZI"
genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_response(user_message, max_retries=3):
    """Get a response from the Gemini API."""
    retry_count = 0
    while retry_count < max_retries:
        try:
            # Configure the model
            model = genai.GenerativeModel("gemini-pro")
            
            # Generate response 
            response = model.generate_content(user_message)
            return response.text
        except Exception as e:
            retry_count += 1
            logger.error(f"Attempt {retry_count} failed: {str(e)}")

            if "429" in str(e) and retry_count < max_retries: # Rate limit error
                wait_time = 2 ** retry_count
                logger.info(f"Rate limit exceeded. Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
                continue
            if retry_count == max_retries:
                logger.error(f"Max retries reached. Giving up on message: {user_message}")
                raise Exception(f"Failed to get a response after {max_retries} retries")
            raise

@app.route('/')
def home():
 
    return render_template('index.html', messages=[])

@app.route('/message', methods=['POST'])
def message():
    try:
        user_message = request.form.get('message')
        if not user_message:
            raise ValueError("Message cannot be empty")
            
        ai_response = "This is a placeholder AI response."
        return render_template('message.html', 
                             message=user_message, 
                             ai_response=ai_response)
                             
    except Exception as e:
        # Log the full error for developers
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        
        # Return a user-friendly error message
        return render_template('error_message.html', 
                             message=user_message,
                             error="I apologize, but I'm having trouble responding right now. Please try again in a moment.")

if __name__ == '__main__':
    print(get_gemini_response("Hello, how are you?"))
    app.run(debug=True)


