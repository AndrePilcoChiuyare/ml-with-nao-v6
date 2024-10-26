import requests
from naoqi import ALProxy
import time
import os
import random as rd
import threading

# NAO Robot Configuration
NAO_IP = "127.0.0.1"
NAO_PORT = 9559

# Initializing NAO proxies
try:
    motion_proxy = ALProxy("ALMotion", NAO_IP, NAO_PORT)
    posture_proxy = ALProxy("ALRobotPosture", NAO_IP, NAO_PORT)
    speech_proxy = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
    audio_proxy = ALProxy("ALAudioPlayer", NAO_IP, NAO_PORT)
    behavior_proxy = ALProxy("ALBehaviorManager", NAO_IP, NAO_PORT)
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

# Make NAO dance (positive sentiment)
def nao_dance():
    try:
        rd.seed(time.time())
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Choose a dance move randomly
        music_number = rd.choice([0, 1])
        dances = [dance0, dance1]
        # Path to the audio file
        music_file = "happy" + str(music_number) + ".ogg"
        audio_file_path = os.path.join(script_dir, "..", "audio", music_file)

        # Start the dance move in a separate thread (to play audio simultaneously)
        dance_thread = threading.Thread(target=dances[music_number])
        dance_thread.start()

        # Play the audio file (soundId is returned)
        sound_id = audio_proxy.post.playFile(audio_file_path)
    except Exception as e:
        print("Error de NAO al bailar:", e)

# Make NAO suffer (negative sentiment)
def nao_suffer():
    try:
        rd.seed(time.time())
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Choose a suffering move randomly
        music_number = rd.choice([0, 1])
        suffers = [suffer0, 1]
        if music_number == 1:
            posture_proxy.goToPosture("SitRelax", 1.0)
            music_file = "sad" + str(music_number) + ".ogg"
            audio_file_path = os.path.join(script_dir, "..", "audio", music_file)
            sound_id = audio_proxy.post.playFile(audio_file_path)
            posture_proxy.goToPosture("StandInit", 0.5)
        else:
            music_file = "sad" + str(music_number) + ".ogg"
            audio_file_path = os.path.join(script_dir, "..", "audio", music_file)
            suffer_thread = threading.Thread(target=suffers[music_number])
            suffer_thread.start()
            sound_id = audio_proxy.post.playFile(audio_file_path)
    except Exception as e:
        print("Error de NAO al sufrir:", e)

# Positive move (dance for happy0 song)
def dance0():
    try:
        time.sleep(0.5)

        arm_names = ["LShoulderPitch", "RShoulderPitch"]
        elbow_names = ["LElbowRoll", "RElbowRoll"]
        arm_angles = [0.0, 0.0]
        fractionMaxSpeed = 0.3
        motion_proxy.setAngles(arm_names, arm_angles, fractionMaxSpeed)
        elbow_angles = [-1.0, 1.0]

        for _ in range(6):
            motion_proxy.setAngles(elbow_names, elbow_angles, fractionMaxSpeed)

            arm_angles = [-0.5, 0.5]
            motion_proxy.setAngles(arm_names, arm_angles, fractionMaxSpeed)
            time.sleep(0.75)

            arm_angles = [0.5, -0.5]
            motion_proxy.setAngles(arm_names, arm_angles, fractionMaxSpeed)
            time.sleep(0.75)

        arm_angles = [1.5, 1.5]
        motion_proxy.setAngles(arm_names, arm_angles, fractionMaxSpeed)
        time.sleep(1)

        posture_proxy.goToPosture("StandInit", 0.5)
    except Exception as e:
        print("Error in hips sway motion:", e)

# Positive move (dance for happy1 song)
def dance1():
    try:
        time.sleep(0.5)

        arm_names = ["LShoulderPitch", "RShoulderPitch"]
        arm_angles = [-0.5, -0.5]
        motion_proxy.setAngles(arm_names, arm_angles, 0.3)
        time.sleep(0.5)

        for _ in range(3):
            motion_proxy.setAngles("LShoulderPitch", -1.2, 0.4)
            motion_proxy.setAngles("RShoulderPitch", 0.5, 0.4)
            time.sleep(0.3)

            motion_proxy.setAngles("LShoulderPitch", 0.5, 0.4)
            motion_proxy.setAngles("RShoulderPitch", -1.2, 0.4)
            time.sleep(0.3)

        head_names = "HeadPitch"
        head_angles = [0.5, -0.3, 0.5]
        for angle in head_angles:
            motion_proxy.setAngles(head_names, angle, 0.5)
            time.sleep(0.5)

        clap_names = ["LShoulderRoll", "RShoulderRoll"]
        motion_proxy.setAngles(clap_names, [0.0, 0.0], 0.3)
        time.sleep(0.5)
        motion_proxy.setAngles(clap_names, [0.5, -0.5], 0.3)
        time.sleep(0.5)

        motion_proxy.setAngles("LShoulderPitch", -1.2, 0.4)
        motion_proxy.setAngles("RShoulderPitch", -1.2, 0.4)
        motion_proxy.setAngles("HeadPitch", -0.5, 0.5)
        time.sleep(1.0)

        posture_proxy.goToPosture("StandInit", 0.5)
    except Exception as e:
        print("Error in excited motion:", e)

# Negative move (move for sad0 song)
def suffer0():
    try:
        time.sleep(0.5)

        names = ["LShoulderPitch", "RShoulderPitch"]
        angles = [-1.0, -1.0]
        fractionMaxSpeed = 0.2
        motion_proxy.setAngles(names, angles, fractionMaxSpeed)

        shoulder_roll_names = ["LShoulderRoll", "RShoulderRoll"]
        roll_angles = [0.6, -0.6]
        motion_proxy.setAngles(shoulder_roll_names, roll_angles, fractionMaxSpeed)

        head_names = ["HeadPitch"]
        head_up_angle = -1.0
        motion_proxy.setAngles(head_names, [head_up_angle], fractionMaxSpeed)

        start_time = time.time()
        while time.time() - start_time < 13:
            motion_proxy.setAngles(names, angles, fractionMaxSpeed)
            motion_proxy.setAngles(shoulder_roll_names, roll_angles, fractionMaxSpeed)

        angles = [1.0, 1.0]
        motion_proxy.setAngles(names, angles, fractionMaxSpeed)
        motion_proxy.setAngles(shoulder_roll_names, [0.0, 0.0], fractionMaxSpeed)

        motion_proxy.setAngles(head_names, [0.0], fractionMaxSpeed)
        time.sleep(0.5)

        posture_proxy.goToPosture("StandInit", 0.5)

    except Exception as e:
        print("Error al ejecutar el movimiento de mirar hacia arriba:", e)

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

# Function to get recognized text from speech recognition service
def get_recognized_text():
    try:
        response = requests.get('http://localhost:5000/recognize')
        if response.status_code == 200:
            return response.json().get('recognized_text', '')
        else:
            return 'Error: ' + response.text
    except Exception as e:
        return 'Error: ' + str(e)

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
                        nao_suffer()
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
        motion_proxy.rest()
    except Exception as e:
        print("Error al poner de NAO al descansar:", e)

if __name__ == "__main__":
    main()