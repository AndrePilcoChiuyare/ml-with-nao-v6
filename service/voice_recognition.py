import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import time

load_dotenv()

def recognize_from_microphone():
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('api_key'), region=os.environ.get('region'))
    speech_config.speech_recognition_language="es-PE"
    
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    print('Habla ahora')
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        return "No se pudo reconocer el discurso."
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        return "Error: Reconocimiento de voz cancelado."
    return ""
