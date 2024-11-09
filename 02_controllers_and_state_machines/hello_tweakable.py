import wpilib
import xrp
import os
import ntcore

# This is easier than environment variables on every dev machine
os.environ["HALSIMXRP_HOST"] = "192.168.42.1"
os.environ["HALSIMXRP_PORT"] = "3540"

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.gyro = xrp.XRPGyro()
        self.motor0 = xrp.XRPMotor(0)
        self.motor1 = xrp.XRPMotor(1)
        self.io = xrp.XRPOnBoardIO()
        self.motor1.setInverted(True)
        self.driveRunning = False

        self.controller = wpilib.XboxController(0)

        nt = ntcore.NetworkTableInstance.getDefault()
        self.table = nt.getTable("XRPRobot")

        self.axisXPub = self.table.getDoubleTopic("X").publish()
        self.axisYPub = self.table.getDoubleTopic("Y").publish()

        # Weird how getEntry() instead of `getBooleanTopic` and that `subscribe` call passes `defaultValue`
        # It makes me think this line isn't necessary and getEntry is superior to get{TYPE}Topic
        self.table.getEntry("SetLed").setDefaultBoolean(False)

        self.ledControlSub = self.table.getBooleanTopic("SetLed").subscribe(defaultValue=False)

        self.lastLedControl = False
        self.io.setLed(False)

    def autonomousPeriodic(self) -> None:
        pass

    def ledToggle(self):
        self.io.setLed(not self.lastLedControl)
        self.lastLedControl = not self.lastLedControl
        return self.lastLedControl
        
    def teleopPeriodic(self):
        self.axisXPub.set(self.controller.getLeftX())
        self.axisYPub.set(self.controller.getLeftY())

        if self.ledControlSub.get() and not self.lastLedControl:
            self.ledToggle()
        if not self.ledControlSub.get() and self.lastLedControl:
            self.ledToggle()

        if self.controller.getAButtonPressed():
            self.ledToggle()
            print("A button pressed. LED on.")
        if self.controller.getBButtonPressed():
            self.ledToggle()
            print("B button pressed. LED off.")

     