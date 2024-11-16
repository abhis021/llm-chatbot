# from flask import Flask, render_template, request
# import requests

# app = Flask(__name__)

# # Define the URL of your locally hosted Ollama server
# OLLAMA_URL = "http://127.0.0.1:11434/v1/engines/llama3.2/completions"

# # Chatbot route that renders the chat interface and handles user input
# @app.route("/", methods=["GET", "POST"])
# def chat():
#     if request.method == "POST":
#         user_input = request.form["user_input"]
#         # Call the function to interact with Ollama model
#         response_text = query_ollama(user_input)
#         return render_template("./index.html", user_input=user_input, response_text=response_text)
#     return render_template("./index.html")

# # Function to query the Ollama server and get the response from llama3.2:latest
# def query_ollama(input_text):
#     url = "http://127.0.0.1:11434/v1/completions"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": "AAAAC3NzaC1lZDI1NTE5AAAAIPx0jESDcnDySiz7wPYgUhaRO5qmAEZTyed+aOw0803c"  # If needed
#     }
#     data = {
#         "model": "llama3.2",
#         "prompt": input_text,
#         "max_tokens": 150
#     }

#     try:
#         response = requests.post(url, json=data, headers=headers)
#         response.raise_for_status()  # This will raise an error for 4xx/5xx responses
#         return response.json().get("choices", [{}])[0].get("text", "No response")
#     except requests.exceptions.RequestException as e:
#         print(f"Error interacting with Ollama: {e}")
#         return "Error: Unable to communicate with the model."

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request
import requests
import markdown

app = Flask(__name__)

# Define the URL of your locally hosted Ollama server
OLLAMA_URL = "http://127.0.0.1:11434/v1/engines/llama3.2/completions"

# Chatbot route that renders the chat interface and handles user input
@app.route("/", methods=["GET", "POST"])
def chat():
    user_input = ""
    response_text = ""
    
    if request.method == "POST":
        user_input = request.form["user_input"]
        # Call the function to interact with Ollama model
        response_text = query_ollama(user_input)
    
    # Convert the Llama's response to HTML (render markdown)
    response_text_html = markdown.markdown(response_text)
    
    return render_template("index.html", user_input=user_input, response_text=response_text_html)

# Function to query the Ollama server and get the response from llama3.2:latest
def query_ollama(input_text):
    url = "http://127.0.0.1:11434/v1/completions"
    headers = {
        "Content-Type": "application/json",
        # You may or may not need the Authorization header depending on your setup
        "Authorization": "AAAAC3NzaC1lZDI1NTE5AAAAIPx0jESDcnDySiz7wPYgUhaRO5qmAEZTyed+aOw0803c"  # If needed
    }
    data = {
        "model": "llama3.2",
        "prompt": input_text,
        "max_tokens": 150
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # This will raise an error for 4xx/5xx responses
        return response.json().get("choices", [{}])[0].get("text", "No response")
    except requests.exceptions.RequestException as e:
        print(f"Error interacting with Ollama: {e}")
        return "Error: Unable to communicate with the model."

if __name__ == "__main__":
    app.run(debug=True)
