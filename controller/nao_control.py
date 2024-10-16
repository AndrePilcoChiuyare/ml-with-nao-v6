import requests
from naoqi import ALProxy
import time
import os

# NAO Robot Configuration
NAO_IP = "127.0.0.1"  # Replace with your NAO's IP address
NAO_PORT = 9559

# Initialize NAO proxies
try:
    motion_proxy = ALProxy("ALMotion", NAO_IP, NAO_PORT)
    posture_proxy = ALProxy("ALRobotPosture", NAO_IP, NAO_PORT)
    speech_proxy = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
    audio_proxy = ALProxy("ALAudioPlayer", NAO_IP, NAO_PORT)
except Exception as e:
    print("Could not create proxies to NAO:", e)
    exit(1)

# Wake up NAO
def wake_up_nao():
    try:
        motion_proxy.wakeUp()
        posture_proxy.goToPosture("StandInit", 0.5)
        speech_proxy.say("Hola! Estoy listo para escucharte.")
    except Exception as e:
        print("Error al despertar a NAO:", e)

# Make NAO dance
def nao_dance():
    try:
        # Path to the audio file (ensure the file exists at the specified location)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        audio_file_path = os.path.join(script_dir, "..", "audio", "sampleaudio.ogg")

        # Play the audio file (soundId is returned)
        sound_id = audio_proxy.playFile(audio_file_path)
    except Exception as e:
        print("Error de NAO al bailar:", e)

# Function to get sentiment from ML service
def get_sentiment(text):
    try:
        response = requests.post('http://localhost:5000/predict', json={'text': text})
        if response.status_code == 200:
            return response.json().get('sentiment', 'Unknown')
        else:
            return 'Error: ' + response.text
    except Exception as e:
        return 'Error: ' + str(e)

# Obtener texto reconocido por voz del servicio de reconocimiento
def get_recognized_text():
    try:
        response = requests.get('http://localhost:5000/recognize')
        if response.status_code == 200:
            return response.json().get('recognized_text', '')
        else:
            return 'Error: ' + response.text
    except Exception as e:
        return 'Error: ' + str(e)

# Main function
def main():
    wake_up_nao()
    while True:
        try:
            
            print("\nOpciones:")
            print("1. Cuentame como te sientes... (presiona 'S').")
            print("2. Salir (presiona 'E').")
            
            # Esperar entrada del usuario
            user_choice = raw_input("Selecciona una opcion: ").strip().lower()

            if user_choice == 's':
                print("\nHas seleccionado 'S'. Estoy preparandome para escucharte.")
                print("Listo, cuentame tu vida...")
                speech_proxy.say("Listo, cuentame tu vida..")
                user_input = get_recognized_text()
                if user_input and user_input != "No se pudo reconocer el discurso.":
                    print("Texto reconocido: ", user_input)
                    
                    sentiment = get_sentiment(user_input)
                    print("Sentimiento:", sentiment)

                    if sentiment == "Positive":
                        nao_dance()
                    else:
                        speech_proxy.say("Pobrecito")
                else:
                    print("No entendi :(")
                    speech_proxy.say("No entendi...")

            elif user_choice == 'e':
                print("\nHas seleccionado 'E' para salir. Adios!")
                speech_proxy.say("Adios!")
                break

            else:
                print("Opcion invalida. Por favor selecciona 'S' para escucharte o 'E' para salir.")

        except Exception as e:
            print("Un error inesperado ha ocurrido:", e)

    # Rest NAO
    try:
        posture_proxy.goToPosture("Sit", 0.5)
        motion_proxy.rest()
    except Exception as e:
        print("Error al poner de NAO al descansar:", e)

if __name__ == "__main__":
    main()