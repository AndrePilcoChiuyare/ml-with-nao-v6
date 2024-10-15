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
        speech_proxy.say("Hello! I'm ready to analyze your sentiment.")
    except Exception as e:
        print("Error waking up NAO:", e)

# Make NAO dance
def nao_dance():
    try:
        # Path to the audio file (ensure the file exists at the specified location)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        audio_file_path = os.path.join(script_dir, "..", "audio", "sampleaudio.ogg")

        # Play the audio file (soundId is returned)
        sound_id = audio_proxy.playFile(audio_file_path)
    except Exception as e:
        print("Error making NAO dance:", e)

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
            
            print("\nOptions:")
            print("1. Speak and analyze sentiment (press 'S').")
            print("2. Exit (press 'E').")
            
            # Esperar entrada del usuario
            user_choice = raw_input("Select an option: ").strip().lower()

            if user_choice == 's':
                print("\nYou have selected 'S'. Getting ready to listen.")
                print("You can talk now...")
                user_input = get_recognized_text()
                if user_input:
                    print("Recognized text: ", user_input)
                    
                    
                    sentiment = get_sentiment(user_input)
                    print("Sentiment:", sentiment)

                    
                    if sentiment == "Positive":
                        nao_dance()
                else:
                    print("No text could be recognized.")

            elif user_choice == 'e':
                print("\nYou have selected 'E'. Exiting the program...")
                break

            else:
                print("Invalid option. Please select 'S' to talk or 'E' to exit.")

        except Exception as e:
            print("An unexpected error has occurred:", e)

    # Rest NAO
    try:
        posture_proxy.goToPosture("Sit", 0.5)
        motion_proxy.rest()
    except Exception as e:
        print("Error putting NAO to rest:", e)

if __name__ == "__main__":
    main()