from flask import Flask, render_template, request, jsonify
from gradio_client import Client

app = Flask(__name__)

# Initialize Gradio client
gradio_client = Client("https://f412ebc29f3e7fd571.gradio.live/")

# Store conversation history
conversation_history = []

# Define the main route
@app.route('/')
def index():
    return render_template('index.html')

# Define the chatbot API endpoint
@app.route('/chatbot', methods=['POST'])
def chatbot():
    if request.method == 'POST':
        # Get user input from the form
        user_input = request.form['user_input']

        # Update conversation history
        conversation_history.append({'user': user_input})

        # Make a request to the chatbot API
        result = gradio_client.predict(user_input, api_name="/chat")

        # Update conversation history with chatbot response
        conversation_history.append({'bot': result})

        # Return the conversation history as JSON
        return jsonify({'conversation': conversation_history})

if __name__ == '_main_':
    app.run(debug=True)