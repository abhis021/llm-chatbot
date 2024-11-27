from flask import Flask, render_template, request, send_file
import requests
import markdown
from gtts import gTTS
import os

app = Flask(__name__)

# Define the URL of your locally hosted Ollama server
OLLAMA_URL = "http://127.0.0.1:11434/v1/engines/llama3.2/completions"

# Chatbot route that renders the chat interface and handles user input
@app.route("/", methods=["GET", "POST"])
def chat():
    user_input = ""
    response_text = ""
    audio_file = None # we'll use this to store the audio file if needed
    
    if request.method == "POST":
        user_input = request.form["user_input"]
        # Call the function to interact with Ollama model
        response_text = query_ollama(user_input)

        # Generate TTS audio from the response text and save as mp3
        audio_file = generate_audio(response_text)
    
    # Convert the Llama's response to HTML (render markdown)
    response_text_html = markdown.markdown(response_text)
    
    return render_template("index.html", 
                           user_input=user_input, 
                           response_text=response_text_html, 
                           audio_file=audio_file)

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
    
    # Function to generate TTS from text and save as audio file
def generate_audio(response_text):
    try:
        # Convert the text to speech
        tts = gTTS(text=response_text, lang='en')
        audio_filename = "static/response_audio.mp3"
        tts.save(audio_filename)
        return audio_filename
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

# Route to serve the generated audio
@app.route("/audio")
def serve_audio():
    audio_file_path = "static/response_audio.mp3"
    if os.path.exists(audio_file_path):
        return send_file(audio_file_path, mimetype='audio/mpeg')
    else:
        return "No audio file generated yet.", 404

if __name__ == "__main__":
    app.run(debug=True)
