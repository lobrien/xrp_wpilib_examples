import wpilib
import xrp
import os
import ntcore

# This is easier than environment variables on every dev machine
os.environ["HALSIMXRP_HOST"] = "192.168.42.1"
os.environ["HALSIMXRP_PORT"] = "3540"

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        MOTOR_CHANNEL_LEFT = 0
        MOTOR_CHANNEL_RIGHT = 1

        self.gyro = xrp.XRPGyro()
        self.motor0 = xrp.XRPMotor(MOTOR_CHANNEL_LEFT)
        self.motor1 = xrp.XRPMotor(MOTOR_CHANNEL_RIGHT)
        self.io = xrp.XRPOnBoardIO()
        self.motor1.setInverted(True)
        self.driveRunning : bool = False


        self.controller = wpilib.XboxController(0)

        nt = ntcore.NetworkTableInstance.getDefault()
        self.table = nt.getTable("XRPRobot")

        self.axisXPub = self.table.getDoubleTopic("X").publish()
        self.axisYPub = self.table.getDoubleTopic("Y").publish()
        
        # Must setDefault* to make entry visible on Shuffleboard
        self.table.getEntry("SetLed").setDefaultBoolean(False)
        self.ledControlSub = self.table.getBooleanTopic("SetLed").subscribe(defaultValue=False)

        self.lastLedControl = True
        self.io.setLed(True)

    def ledToggle(self):
        self.io.setLed(not self.lastLedControl)
        self.lastLedControl = not self.lastLedControl
        return self.lastLedControl
    
    def ledOn(self):
        print("on")
        self.io.setLed(True)
        self.lastLedControl = True

    def ledOff(self):
        print("off")
        self.io.setLed(False)
        self.lastLedControl = False
        
    def teleopPeriodic(self):
        self.axisXPub.set(self.controller.getLeftX())
        self.axisYPub.set(self.controller.getLeftY())
        
        if self.ledControlSub.get() :
            self.ledOn()
        else :
            self.ledOff()
