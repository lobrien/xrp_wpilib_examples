import wpilib
import xrp
import os
import ntcore

# This is easier than environment variables on every dev machine
os.environ["HALSIMXRP_HOST"] = "192.168.42.1"
os.environ["HALSIMXRP_PORT"] = "3540"

class MotorRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.io = xrp.XRPOnBoardIO()
      
        # Quirk: You must set the XRP LED to False to initialize it
        self.io.setLed(False)

        self.motor = xrp.XRPMotor(0)

    def autonomousInit(self):
        print("autoInit")
        self.io.setLed(True)
        self.motor.set(0.5)
      
    def autonomousExit(self):
        print("autoExit")
        self.io.setLed(False)
        self.motor.stopMotor()

