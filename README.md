# Llama Voice Chat

Llama Voice Chat is a Flask-based web application that allows users to chat with a language model and transcribe audio files using the Groq API. This application is designed to provide a seamless and interactive experience for users looking to leverage AI-driven language models for various tasks.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Chat with a large language model using Groq API.
- Transcribe audio files (m4a, mp3, wav) to text using Groq API.
- Simple and intuitive web interface.

## Requirements

- Python 3.7+
- Flask
- Groq API Key

## Installation

### Clone the Repository

```bash
git clone https://github.com/AimpactSpace/Llama-Voice-Chat.git
cd Llama-Voice-Chat

Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies:

bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies
bash
pip install -r requirements.txt
Set Up Environment Variables
Create a .env file in the root directory of the project and add your Groq API key:

env
GROQ_API_KEY=your_groq_api_key
Usage
Run the Application
bash
flask run
By default, the application will be available at http://127.0.0.1:5000/.

Chat with the Model
Open your browser and navigate to http://127.0.0.1:5000/.
Use the chat interface to interact with the language model.
Transcribe Audio Files
Use the /transcribe endpoint to upload and transcribe audio files.
Example using curl:

bash
curl -X POST -F 'file=@path_to_audio_file.wav' http://127.0.0.1:5000/transcribe
Project Structure
bash

Llama-Voice-Chat/
├── uploads/                    # Directory to store uploaded audio files
├── templates/
│   └── index.html              # HTML template for the chat interface
├── app.py                      # Main application file 
├── requirements.txt            # Project dependencies
├── .env                        # Environment variables
└── README.md                   # Project documentation


## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
