from naoqi import ALProxy
import time

# Replace with the correct IP and port
robot_ip = "127.0.0.1"
robot_port = 9559

# Connect to the ALMotion proxy to control the robot
motion_proxy = ALProxy("ALMotion", robot_ip, robot_port)

# Wake up the robot to enable movements
motion_proxy.wakeUp()

# Define joint names for the lower body (legs) to set the crouching position
names = ["HeadPitch",
         "LHipYawPitch", "RHipYawPitch",
         "LHipRoll", "RHipRoll",
         "LHipPitch", "RHipPitch",
         "LKneePitch", "RKneePitch",
         "LAnklePitch", "RAnklePitch",
         "LAnkleRoll", "RAnkleRoll"]

# Define angles in radians for the crouching position (angles need to be carefully chosen)
angles = [0.0,            # HeadPitch (keep head neutral)
          -0.5, -0.5,     # Hips yaw-pitch
          0.0, 0.0,       # Hip roll
          -1.0, -1.0,     # Hip pitch (leaning hips back)
          2.0, 2.0,       # Knee pitch (bending the knees)
          -1.0, -1.0,     # Ankle pitch (leaning ankles forward)
          0.0, 0.0]       # Ankle roll

# Time for the movement to complete (in seconds)
times = 2.0

# Make the robot crouch with a smooth motion
motion_proxy.angleInterpolation(names, angles, times, True)

# Optional: let the robot stay crouched for 3 seconds
time.sleep(3)

# You can have it stand back up if desired by calling motion_proxy.wakeUp() again or setting new angles.