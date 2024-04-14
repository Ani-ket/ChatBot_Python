from flask import Flask, request, render_template
import random

app = Flask(__name__)

# Define states for dialogue management
class State:
    GREETING = 0
    ASKING_NAME = 1
    ASKING_AGE = 2
    GOODBYE = 3

# Automated responses for greetings
GREETING_RESPONSES = [
    "Hi there! How can I assist you today?",
    "Hello! What can I help you with?",
    "Hey! Feel free to ask me anything."
]

# Automated responses for farewells
GOODBYE_RESPONSES = [
    "Goodbye! Have a great day!",
    "See you later! Take care.",
    "Farewell! Come back anytime."
]

# Automated responses for simple inquiries
INQUIRY_RESPONSES = {
    "time": "It's time to chat! 😉",
    "weather": "The forecast is looking sunny with a chance of great conversation!",
    "help": "I'm here to assist you. Just let me know what you need help with."
}

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        message = request.form["message"]
        state = int(request.form["state"])
        
        response, new_state = respond_to_message(message, state)
        
        return render_template("index.html", response=response, state=new_state)
    else:
        return render_template("index.html", response=random.choice(GREETING_RESPONSES), state=State.GREETING)

def respond_to_message(message, state):
    message = message.strip().lower()
    
    if state == State.GREETING:
        if "bye" in message:
            return random.choice(GOODBYE_RESPONSES), State.GOODBYE
        else:
            return random.choice(GREETING_RESPONSES), state
            
    elif state == State.GOODBYE:
        return random.choice(GOODBYE_RESPONSES), state
    
    # Handle simple inquiries
    for inquiry, response in INQUIRY_RESPONSES.items():
        if inquiry in message:
            return response, state
    
    return "I'm sorry, I didn't understand that. How can I assist you?", state

if __name__ == "__main__":
    app.run(debug=True)
