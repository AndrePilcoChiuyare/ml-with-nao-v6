from naoqi import ALProxy

# Replace with the correct IP and port
robot_ip = "127.0.0.1"
robot_port = 9559

# Connect to the ALTextToSpeech proxy
tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)

# Make the robot say something
tts.say("Hello, I am a NAO robot!")