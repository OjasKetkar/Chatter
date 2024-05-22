from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from os import getenv

app = Flask(__name__)

# Initialize OpenAI client with the API key
client = OpenAI(
    base_url="ENTER_OPENROUTER_URL",
    api_key="ENTER_OPENROUTER_API_KEY",
)

# Store conversation history
conversation_history = []

# Define the main route
@app.route('/')
def index():
    return render_template('index.html')

# Define the chatbot API endpoint
@app.route('/chat', methods=['POST'])
def chatbot():
    if request.method == 'POST':
        # Get user input from the form
        user_input = request.form['user_input']

        # Update conversation history
        conversation_history.append({'user': user_input})

        # Make a request to the chatbot API
        completion = client.chat.completions.create(
            # extra_headers={
            #     "HTTP-Referer": "$YOUR_SITE_URL",  # Optional, for including your app on openrouter.ai rankings.
            #     "X-Title": "$YOUR_APP_NAME",  # Optional. Shows in rankings on openrouter.ai.
            # },
            model="nousresearch/nous-capybara-7b:free",
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
        )
        bot_response = completion.choices[0].message.content

        # Update conversation history with chatbot response
        conversation_history.append({'bot': bot_response})

        # Return the conversation history as JSON
        return jsonify({'conversation': conversation_history})

if __name__ == '__main__':
    app.run(host = "0.0.0.0" ,debug=True)
