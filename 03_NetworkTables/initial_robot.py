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

        # Weird how getEntry() instead of `getBooleanTopic` and that `subscribe` call passes `defaultValue`
        # It makes me think this line isn't necessary and getEntry is superior to get{TYPE}Topic
        self.table.getEntry("SetLed").setDefaultBoolean(False)
        self.setLedOn(False)

        # LED blinking timer
        self.timer = wpilib.Timer()

        # Time in secs on
        self.timer_on_duration = 1.0
        self.timer_off_duration = 1.0
    
    def setLedOn(self, b : bool):
        self.io.setLed(b)
        self.lastLedControl = b

    def autonomousInit(self) -> None:
        self.timer.start()

    def autonomousPeriodic(self) -> None:
        time = self.timer.get()
        if self.lastLedControl and time > self.timer_on_duration:
            self.setLedOn(False)
            self.timer.reset()
        elif not self.lastLedControl and time > self.timer_off_duration:
            self.setLedOn(True)
            self.timer.reset()
        else: 
            # Do nothing
            pass