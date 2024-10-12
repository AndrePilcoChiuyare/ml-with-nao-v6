# Import necessary libraries
from transformers import MarianMTModel, MarianTokenizer
# import gradio as gr

# Define the model name
model_name = 'Helsinki-NLP/opus-mt-es-en'

# Load the tokenizer and model
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate(text):
    # Tokenize the input text
    tokenized_text = tokenizer.prepare_seq2seq_batch([text], return_tensors='pt')
    
    # Perform the translation
    translation = model.generate(**tokenized_text)
    
    # Decode the translated text
    translated_text = tokenizer.decode(translation[0], skip_special_tokens=True)
    
    return translated_text

input = input("Input text: ")
output = translate(input)

print(output)

# # Create a Gradio interface
# iface = gr.Interface(
#     fn=translate, 
#     inputs=gr.Textbox(label="Enter text to translate"), 
#     outputs=gr.Textbox(label="Translated text"),
#     title="Spanish to English Translator",
#     description="Enter Spanish text and get the English translation."
# )

# # Launch the Gradio interface
# iface.launch()