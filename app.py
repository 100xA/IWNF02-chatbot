from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    return render_template('index.html', messages=[])

@app.route('/message', methods=['POST'])
def message():
    user_message = request.form.get('message')
    ai_response = "This is a placeholder AI response. We'll implement real AI responses in the next step."
    return render_template('message.html', message=user_message, ai_response=ai_response)

if __name__ == '__main__':
    app.run(debug=True)