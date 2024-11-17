from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    return render_template('index.html', messages=[])

@app.route('/message', methods=['POST'])
def message():
    user_message = request.form.get('message')
    return render_template('message.html', message=user_message)

if __name__ == '__main__':
    app.run(debug=True)