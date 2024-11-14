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

        initialLedState = False
        self.setLedOn(initialLedState)

        # LED blinking timer
        self.timer = wpilib.Timer()

        # Default time in seconds
        self.timer_on_duration = 1.0
        self.timer_off_duration = 1.0
        
        self.table, self.onDurationSub, self.offDurationSub = self.initTweakableLedTimer(initialLedState)

    def initTweakableLedTimer(self, initialLedState) -> \
        tuple[ntcore.NetworkTableInstance, ntcore.DoubleSubscriber, ntcore.DoubleSubscriber]:
        
        nt = ntcore.NetworkTableInstance.getDefault()
        table = nt.getTable("XRPRobot")
        
        # This sets the initial value (note, synchronized with LED's initial state)
        table.getEntry("SetLed").setDefaultBoolean(initialLedState)

        ## Create the topics for controlling duration
        table.getEntry("OnDuration").setDefaultValue(self.timer_on_duration)
        table.getEntry("OffDuration").setDefaultValue(self.timer_off_duration)

        # Create the subscriptions to listen to tweaks
        onDurationSub = table.getDoubleTopic("OnDuration").subscribe(self.timer_on_duration)
        offDurationSub = table.getDoubleTopic("OffDuration").subscribe(self.timer_off_duration)
        return table, onDurationSub, offDurationSub

    # State transition to set the LED on or off
    # As always: change the hardware state, synchronize the program state    
    def setLedOn(self, b : bool):
        self.io.setLed(b)
        self.lastLedControl = b

    # Helper function that reads the network table values from the appropriate subscription
    # and modifies programmatic state-change thresholds
    def updateDurations(self):
        runtimeOnDuration = self.onDurationSub.get()
        runtimeOffDuration = self.offDurationSub.get()

        self.timer_on_duration = runtimeOnDuration
        self.timer_off_duration = runtimeOffDuration


    # Despite the robot being disabled, the robot can still read and synchronize to 
    # the network table values. This is useful for updating the robot's configuration
    def disabledPeriodic(self) -> None:
        # Updates while disabled (On machine status LEDs / Display) (Step 2)
        self.updateDurations()

    # Start the timer, which is used to control the duration of LED on/off states
    # and update the duration thresholds
    def autonomousInit(self) -> None:
        self.timer.start()
        # Reads final pre-auto values (Step 1)
        self.updateDurations()
        
    def autonomousPeriodic(self) -> None:
        # Works on XRP, but this feels like cheating? (Step 3)
        self.updateDurations()
        
        # How much time has passed?
        time = self.timer.get()

        # Logical test for state (lastLedControl) and duration exceeding threshold
        if self.lastLedControl and time > self.timer_on_duration:
            self.setLedOn(False)
            self.timer.reset()
        elif not self.lastLedControl and time > self.timer_off_duration:
            self.setLedOn(True)
            self.timer.reset()
        else: 
            # Do nothing
            pass
