from flask import Flask, request, jsonify, render_template
import os
from datetime import datetime
from groq import Groq
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Set up upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'m4a', 'mp3', 'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to handle sending messages and receiving responses
def chat_with_model(client, messages, model="llama-3.1-8b-instant"):
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )
    return chat_completion

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get('messages', [])
    
    # Add an initial system message to instruct the model
    if not any(message['role'] == 'system' for message in messages):
        messages.insert(0, {
            "role": "system",
            "content": "You are an expert large language model"
        })
    
    chat_completion = chat_with_model(client, messages)
    
    # Extract the model's response message
    model_response = chat_completion.choices[0].message.content
    
    # Append model's response to the conversation history
    messages.append({
        "role": "assistant",
        "content": model_response,
    })
    
    return jsonify(messages=messages)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            with open(filepath, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-large-v3",
                )
            
            os.remove(filepath)  # Remove the file after transcription
            
            return jsonify({'transcription': transcription.text})
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)
