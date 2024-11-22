from flask import Flask, render_template, request, jsonify
import logging

app = Flask(__name__, static_url_path='/static')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    app.run(debug=True)


