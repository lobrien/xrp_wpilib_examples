import wpilib
import xrp
import os
import ntcore
import math

# This is easier than environment variables on every dev machine
os.environ["HALSIMXRP_HOST"] = "192.168.42.1"
os.environ["HALSIMXRP_PORT"] = "3540"

class MotorRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.io = xrp.XRPOnBoardIO()
      
        # Quirk: You must set the XRP LED to False to initialize it
        self.io.setLed(False)

        self.motor = xrp.XRPMotor(1)
        self.motor.setInverted(True)
        self.gyro = xrp.XRPGyro()
        self.gyro.reset()

        


    def autonomousInit(self):
        print("autoInit")
        self.io.setLed(True)
        self.motor.set(0.75)
        self.gyro.reset()

    def autonomousPeriodic(self):
        angle = self.gyro.getAngle()
        print(f"Angle: {angle}")
        if abs(angle) > 90:
            print("Stop!")
            self.motor.stopMotor()
            self.io.setLed(False)
            
    def teleopInit(self):
        print("teleopInit")
        self.io.setLed(False)
        self.motor.stopMotor()

