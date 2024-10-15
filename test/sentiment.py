from transformers import BertForSequenceClassification, BertTokenizer
import torch
import gradio as gr

def predict(text):
    model = BertForSequenceClassification.from_pretrained("VerificadoProfesional/SaBERT-Spanish-Sentiment-Analysis")
    tokenizer = BertTokenizer.from_pretrained("VerificadoProfesional/SaBERT-Spanish-Sentiment-Analysis")  
    threshold = 0.5
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1).squeeze().tolist()
    
    predicted_class = torch.argmax(logits, dim=1).item()
    if probabilities[predicted_class] <= threshold and predicted_class == 1:
        predicted_class = 0

    # return bool(predicted_class), probabilities
    return predicted_class

# text = "te odio"
# predicted_label,probabilities = predict(model,tokenizer,text)
# print(f"Text: {text}")
# print(f"Predicted Class: {predicted_label}")
# print(f"Probabilities: {probabilities}")

# Create a Gradio interface
iface = gr.Interface(
    fn = predict,
    inputs = gr.Textbox(label="Enter text to analyze"),
    outputs = gr.Textbox(label="Sentiment"),
    title="Spanish Sentiment Analysis",
    description="Enter Spanish text and get the sentiment analysis."
)

iface.launch()