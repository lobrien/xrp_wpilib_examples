import wpilib
import wpilib.drive
import xrp
import os
import ntcore

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

    def robotPeriodic(self):
        self.drivetrain.feed()

    def autonomousInit(self):
        print("autoInit")
        self.io.setLed(True)
        dl = self.leftEncoder.getDistance()
        dr = self.rightEncoder.getDistance()
        self.leftEncoder.reset()
        self.rightEncoder.reset()
        
        print(f"Encoder distance: {dl}, {dr}")
        self.drivetrain.tankDrive(1.0, 1.0)
        
    def autonomousPeriodic(self):
        dl = self.leftEncoder.getDistance()
        dr = self.rightEncoder.getDistance()
        if dl < 500:
            print(f"Encoder distance: {dl}, {dr}")
        else:
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
        
