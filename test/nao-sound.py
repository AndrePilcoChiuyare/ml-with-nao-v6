from naoqi import ALProxy
import os
import time

# Replace with the correct IP and port
robot_ip = "127.0.0.1"
robot_port = 9559

# Connect to the ALAudioPlayer proxy
audio_player = ALProxy("ALAudioPlayer", robot_ip, robot_port)

# Path to the audio file (ensure the file exists at the specified location)
script_dir = os.path.dirname(os.path.abspath(__file__))
audio_file_path = os.path.join(script_dir, "..", "audio", "sampleaudio.ogg")

# Play the audio file (soundId is returned)
sound_id = audio_player.playFile(audio_file_path)

# Sleep for the duration of the audio file
# You might want to set the sleep time according to the length of your audio file
time.sleep(5)  # Adjust time to the length of your audio file in seconds

# Stop the audio playback if still playing (try to handle it gracefully)
try:
    if audio_player.isPlaying(sound_id):  # Only stop if it's still playing
        audio_player.stop(sound_id)
except Exception as e:
    print("An error occurred while stopping the audio:", e)
