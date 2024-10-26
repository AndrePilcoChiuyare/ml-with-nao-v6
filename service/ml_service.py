from transformers import BertForSequenceClassification, BertTokenizer
from flask import Flask, request, jsonify
import torch
from voice_recognition import recognize_from_microphone  # Importing the function from the voice_recognition.py file

app = Flask(__name__)

# Initialize model and tokenizer
model_name = "VerificadoProfesional/SaBERT-Spanish-Sentiment-Analysis"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)
model.eval()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1).squeeze().tolist()
    predicted_class = torch.argmax(logits, dim=1).item()
    threshold = 0.5
    if probabilities[predicted_class] <= threshold and predicted_class == 1:
        predicted_class = 0

    sentiment = "Positive" if predicted_class == 1 else "Negative"
    return jsonify({'sentiment': sentiment})

# Route for speech recognition
@app.route('/recognize', methods=['GET'])
def recognize():
    text = recognize_from_microphone()  # Calling the imported function
    return jsonify({'recognized_text': text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)