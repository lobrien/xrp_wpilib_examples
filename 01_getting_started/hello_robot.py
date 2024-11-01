import wpilib
import xrp
import os

# This is easier than environment variables on every dev machine
os.environ["HALSIMXRP_HOST"] = "192.168.42.1"
os.environ["HALSIMXRP_PORT"] = "3540"

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.io = xrp.XRPOnBoardIO()
        
        # Quirk: You must set the XRP LED to False to initialize it
        self.io.setLed(False)
        
    def autonomousInit(self):
        print("autoInit")
        self.io.setLed(True)

    def autonomousExit(self):
        print("autoExit")
        self.io.setLed(False)
