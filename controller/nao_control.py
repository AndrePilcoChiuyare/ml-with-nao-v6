import requests
from naoqi import ALProxy
import time
import os
import random as rd
import threading

# NAO Robot Configuration
NAO_IP = "127.0.0.1"  # Replace with your NAO's IP address
NAO_PORT = 9559

# Initialize NAO proxies
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

# Make NAO dance
def nao_dance():
    try:
        rd.seed(time.time())
        # Path to the audio file (ensure the file exists at the specified location)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        music_number = rd.choice([0, 1])
        dances = [dance0, dance1]
        music_file = "happy" + str(music_number) + ".ogg"
        audio_file_path = os.path.join(script_dir, "..", "audio", music_file)

        dance_thread = threading.Thread(target=dances[music_number])
        dance_thread.start()

        # Play the audio file (soundId is returned)
        sound_id = audio_proxy.playFile(audio_file_path)
    except Exception as e:
        print("Error de NAO al bailar:", e)

def nao_suffer():
    try:
        rd.seed(time.time())
        # Path to the audio file (ensure the file exists at the specified location)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        music_number = rd.choice([0, 1])
        suffers = [suffer0, 1]
        if music_number == 1:
            posture_proxy.goToPosture("SitRelax", 1.0)
            music_file = "sad" + str(music_number) + ".ogg"
            audio_file_path = os.path.join(script_dir, "..", "audio", music_file)
            sound_id = audio_proxy.playFile(audio_file_path)
            posture_proxy.goToPosture("StandInit", 0.5)
        else:
            music_file = "sad" + str(music_number) + ".ogg"
            audio_file_path = os.path.join(script_dir, "..", "audio", music_file)
            suffer_thread = threading.Thread(target=suffers[music_number])
            suffer_thread.start()
            sound_id = audio_proxy.playFile(audio_file_path)
            
    except Exception as e:
        print("Error de NAO al sufrir:", e)

# Define the dance moves, including arm and head movements, lasting 8 seconds
# Excited animation function
def dance1():
    try:
        time.sleep(0.5)

        # Lift both arms quickly (as if celebrating)
        arm_names = ["LShoulderPitch", "RShoulderPitch"]
        arm_angles = [-0.5, -0.5]  # Arms halfway up
        motion_proxy.setAngles(arm_names, arm_angles, 0.3)  # Fast speed for excitement
        time.sleep(0.5)

        # Wave arms alternately (simulate waving in excitement)
        for _ in range(3):  # Wave 3 times
            motion_proxy.setAngles("LShoulderPitch", -1.2, 0.4)  # Lift left arm higher
            motion_proxy.setAngles("RShoulderPitch", 0.5, 0.4)   # Lower right arm
            time.sleep(0.3)

            motion_proxy.setAngles("LShoulderPitch", 0.5, 0.4)   # Lower left arm
            motion_proxy.setAngles("RShoulderPitch", -1.2, 0.4)  # Lift right arm higher
            time.sleep(0.3)

        # Quick nodding head (simulate excitement)
        head_names = "HeadPitch"
        head_angles = [0.5, -0.3, 0.5]  # Head up, down, up
        for angle in head_angles:
            motion_proxy.setAngles(head_names, angle, 0.5)
            time.sleep(0.5)

        # Clap hands together (simulate excitement)
        clap_names = ["LShoulderRoll", "RShoulderRoll"]
        motion_proxy.setAngles(clap_names, [0.0, 0.0], 0.3)  # Bring shoulders together
        time.sleep(0.5)
        motion_proxy.setAngles(clap_names, [0.5, -0.5], 0.3)  # Return arms to normal
        time.sleep(0.5)

        # End with a cheering posture (arms up, head back)
        motion_proxy.setAngles("LShoulderPitch", -1.2, 0.4)  # Left arm up
        motion_proxy.setAngles("RShoulderPitch", -1.2, 0.4)  # Right arm up
        motion_proxy.setAngles("HeadPitch", -0.5, 0.5)  # Head looking up
        time.sleep(1.0)

        # Reset to a neutral posture
        posture_proxy.goToPosture("StandInit", 0.5)

    except Exception as e:
        print("Error in excited motion:", e)

# Hips sway animation function
def dance0():
    try:
        time.sleep(0.5)

        # Estirar ambos brazos hacia adelante
        arm_names = ["LShoulderPitch", "RShoulderPitch"]  # Hombros para mover brazos hacia adelante
        arm_angles = [0.0, 0.0]  # angulos en radianes (0 = brazos estirados hacia adelante)
        fractionMaxSpeed = 0.3
        motion_proxy.setAngles(arm_names, arm_angles, fractionMaxSpeed)

        # Movimiento de arriba a abajo por 9 segundos
        for _ in range(6):  # Repetir el movimiento varias veces
            # Mover los brazos hacia arriba
            arm_angles = [-0.5, -0.5]  # Mover los brazos hacia arriba (angulo negativo)
            motion_proxy.setAngles(arm_names, arm_angles, fractionMaxSpeed)
            time.sleep(0.75)

            # Mover los brazos hacia abajo
            arm_angles = [0.5, 0.5]  # Mover los brazos hacia abajo (angulo positivo)
            motion_proxy.setAngles(arm_names, arm_angles, fractionMaxSpeed)
            time.sleep(0.75)

        # Regresar los brazos a la posicion inicial
        arm_angles = [1.5, 1.5]  # Posicion de reposo de los brazos
        motion_proxy.setAngles(arm_names, arm_angles, fractionMaxSpeed)
        time.sleep(1)

        # Volver a postura neutra
        posture_proxy.goToPosture("StandInit", 0.5)

    except Exception as e:
        print("Error in hips sway motion:", e)

def suffer0():
    try:
        time.sleep(0.5)

        # Levantar los brazos
        names = ["LShoulderPitch", "RShoulderPitch"]  # Mover ambos hombros
        angles = [-1.0, -1.0]  # angulos en radianes para levantar los brazos hacia arriba
        fractionMaxSpeed = 0.2  # Velocidad lenta
        motion_proxy.setAngles(names, angles, fractionMaxSpeed)

        shoulder_roll_names = ["LShoulderRoll", "RShoulderRoll"]  # Mover ambos hombros
        roll_angles = [0.6, -0.6]
        motion_proxy.setAngles(shoulder_roll_names, roll_angles, fractionMaxSpeed)

        # Mover la cabeza hacia arriba
        head_names = ["HeadPitch"]
        head_up_angle = -1.0  # Mirando hacia arriba
        motion_proxy.setAngles(head_names, [head_up_angle], fractionMaxSpeed)

        # Mantener la posicion por 14 segundos
        start_time = time.time()
        while time.time() - start_time < 13:
            motion_proxy.setAngles(names, angles, fractionMaxSpeed)
            motion_proxy.setAngles(shoulder_roll_names, roll_angles, fractionMaxSpeed)

        # Bajar los brazos y centrar la cabeza
        angles = [1.0, 1.0]  # Mover los brazos hacia abajo
        motion_proxy.setAngles(names, angles, fractionMaxSpeed)
        motion_proxy.setAngles(shoulder_roll_names, [0.0, 0.0], fractionMaxSpeed)


        # Centrar la cabeza
        motion_proxy.setAngles(head_names, [0.0], fractionMaxSpeed)  # Centrar la cabeza
        time.sleep(0.5)

        # Regresar a la postura inicial
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