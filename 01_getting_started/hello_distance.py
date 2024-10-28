import wpilib
import wpilib.drive
import xrp
import os
import ntcore
import math

# This is easier than environment variables on every dev machine
os.environ["HALSIMXRP_HOST"] = "192.168.42.1"
os.environ["HALSIMXRP_PORT"] = "3540"

# servo initial value is 90.0, 0.5
# seems to ignore values under 
class MotorRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.io = xrp.XRPOnBoardIO()
      
        # Quirk: You must set the XRP LED to False to initialize it
        self.io.setLed(False)

        leftmotor = xrp.XRPMotor(0)
        rightmotor = xrp.XRPMotor(1)
        rightmotor.setInverted(True)
        self.drivetrain = wpilib.drive.DifferentialDrive(
            leftmotor,
            rightmotor
            )

        self.leftEncoder = wpilib.Encoder(4,5)
        self.rightEncoder = wpilib.Encoder(6,7)
        self.leftEncoder.reset()
        self.rightEncoder.reset()

        # The circumference of the wheel is it's diameter times pi
        # We will use inches as our measurement unit
        wheel_diameter = 2.3622 # inches. (This is 60mm, from datasheet)
        wheel_circumference = wheel_diameter * math.pi
        
        # The encoder has this many ticks per revolution *of the motor shaft* 
        # (*not* the wheel itself)
        encoder_resolution = 12 # From datasheet

        # The gear ratio is how many times the motor shaft has to spin 
        # for the *wheels* to make one full rotation.
        gear_ratio = 48.75 # From datasheet

        # So the encoder has this many ticks per revolution of the *wheel*
        # Calculate the total counts per wheel revolution
        counts_per_wheel_revolution = encoder_resolution * gear_ratio

        # And since we know the circumference of the wheel, we can calculate:
        distance_per_pulse = wheel_circumference / counts_per_wheel_revolution

        # We can tell the encoder to use distance per pulse 
        # This changes the values returned by getDistance() to be in inches
        self.leftEncoder.setDistancePerPulse(distance_per_pulse)
        self.rightEncoder.setDistancePerPulse(distance_per_pulse)

        self.ran = False
       

    def robotPeriodic(self):
        self.drivetrain.feed()

    def autonomousInit(self):
        print("autoInit")
        self.io.setLed(True)
        
        self.leftEncoder.reset()
        self.rightEncoder.reset()

        dl = self.leftEncoder.getDistance()
        dr = self.rightEncoder.getDistance()
        print(f"Encoder distance: {dl}, {dr}")
        self.drivetrain.tankDrive(1.0, 1.0)
        self.ran = False
        
    def autonomousPeriodic(self):
        if self.ran == True:
            return
        dl = self.leftEncoder.getDistance()
        dr = self.rightEncoder.getDistance()
        print(f"Encoder distance: {dl}, {dr}")
        if dl > 66.5: # inches
            self.drivetrain.stopMotor()
            self.ran = True
            print("Stopped")
    
    def autonomousEnd(self):
        self.drivetrain.stopMotor()
        
    def teleopInit(self):
        print("teleopInit")
        self.io.setLed(False)
        
    def disabledInit(self):
        pass
        
