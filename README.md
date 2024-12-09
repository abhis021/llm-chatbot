# llm-chatbot
* An llm chatbot using ollama in the backend.
* This is a chatbot which utilizes serving capabilities of Ollama.

Works using Flask as the web development framework.

The flask is utilized to create a simple web page with a chatbot interface.

The audio playback is integrated in the webpage.

The response is tokenized and converted in to markdown format and
then converted the audio into mp3.

The latency of this system depends on the system running the implementation.


# Currently the implementation works with :

## Linux

* Python 3.11
* Ollama
* llama3.2
* flask
* gTTS

Has some latency while fetching response, hopefully it will reduce on more powerful hardware.

## Windows

* Python 3.11
* Ollama
* llama3.2
* flask
* gTTS

Has some latency while fetching response, the hardware is powerful and uses GPU acceleration wherever possible.