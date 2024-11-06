import wpilib
import xrp
import os
import ntcore

# This is easier than environment variables on every dev machine
os.environ["HALSIMXRP_HOST"] = "192.168.42.1"
os.environ["HALSIMXRP_PORT"] = "3540"

class StateRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.io = xrp.XRPOnBoardIO()
        self.motor0 = xrp.XRPMotor(0)
        
        # Odd: It seems you must set the LED to False to initialize it
        self.io.setLed(False)

        self.is_running = False
       
    def toggleRunning(self):
        new_running_state = not self.is_running # `not` is True if expression is False and vice-versa
        self.io.setLed(new_running_state)

        # Motor is more complicated than True/False
        if new_running_state: 
            self.motor0.set(0.5)
        else:
            self.motor0.stopMotor()
        # Store the new state
        self.is_running = new_running_state
        print(f"Robot is running: {self.is_running}")
        
    def autonomousInit(self):
        print("autoInit")
        self.toggleRunning()


    def teleopInit(self):
        print("teleopInit")
        self.toggleRunning()

