"""my_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
# motor = robot.getDevice('motorname')
# ds = robot.getDevice('dsname')
# ds.enable(timestep)
wheel_motors = []
motors_names = ["left_motor","right_motor"]
robot.keyboard.enable(timestep)
robot.keyboard = robot.getKeyboard()

for i in range(2):
    wheel_motors.append(robot.getDevice(motors_names[i]))
    wheel_motors[i].setPosition(float('inf'))
    wheel_motors[i].setVelocity(0.0)
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    
    key = robot.keyboard.getKey()
    print (key)
    if key == 87:
        for i in range(2):
            wheel_motors[i].setVelocity(1.0)
    elif key == 65:
        wheel_motors[0].setVelocity(-0.5)
        wheel_motors[1].setVelocity(0.5)
    elif key == 68:
        wheel_motors[0].setVelocity(0.5)
        wheel_motors[1].setVelocity(-0.5)
    elif key == 83:
        for i in range(2):
            wheel_motors[i].setVelocity(-1.0)
    else:
         pass
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)

# Enter here exit cleanup code.
