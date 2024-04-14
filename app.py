from flask import Flask, request, render_template
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk

app = Flask(__name__)

# Define states for dialogue management
class State:
    GREETING = 0
    ASKING_NAME = 1
    ASKING_AGE = 2
    GOODBYE = 3

# Function to handle incoming messages and generate responses
def respond_to_message(message, state):
    message = message.strip().lower()
    
    if state == State.GREETING:
        if "hello" in message:
            return "Hi there! What's your name?", State.ASKING_NAME
        elif "bye" in message:
            return "Goodbye! Have a great day!", State.GOODBYE
        else:
            return "Hi! How can I assist you?", state
            
    elif state == State.ASKING_NAME:
        name = extract_name(message)
        if name:
            return f"Nice to meet you, {name}! How old are you?", State.ASKING_AGE
        else:
            return "Sorry, I didn't catch your name. What's your name?", state
            
    elif state == State.ASKING_AGE:
        age = extract_age(message)
        if age:
            return f"Got it! You're {age} years old. How can I help you further?", State.GREETING
        else:
            return "Sorry, I didn't get that. Can you please tell me your age?", state
            
    elif state == State.GOODBYE:
        return "Goodbye! Have a great day!", state

# Function to extract name from message using NLTK
def extract_name(message):
    words = word_tokenize(message)
    tags = pos_tag(words)
    for word, tag in tags:
        if tag == "NNP":  # Proper noun
            return word
    return None

# Function to extract age from message using NLTK
def extract_age(message):
    words = word_tokenize(message)
    for word in words:
        if word.isdigit():
            return word
    return None

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        message = request.form["message"]
        state = int(request.form["state"])
        
        response, new_state = respond_to_message(message, state)
        
        return render_template("index.html", response=response, state=new_state)
    else:
        return render_template("index.html", response="Hi! How can I assist you?", state=State.GREETING)

if __name__ == "__main__":
    app.run(debug=True)
