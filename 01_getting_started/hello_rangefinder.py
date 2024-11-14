import wpilib
import wpilib.drive
import wpimath.units as units 
import xrp
import os
import math
from dataclasses import dataclass

# This is easier than environment variables on every dev machine
os.environ["HALSIMXRP_HOST"] = "192.168.42.1"
os.environ["HALSIMXRP_PORT"] = "3540"

@dataclass(frozen=True)
class DigitalChannelConstants:
    LEFT_MOTOR_CHANNEL = 0
    RIGHT_MOTOR_CHANNEL = 1

@dataclass
class ControlConstants:
    LEFT_MOTOR_SPEED= 1.0 # 100%
    RIGHT_MOTOR_SPEED= 1.0 

    WALL_STOP_DISTANCE = 12.0 # inches

class MotorRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.io = xrp.XRPOnBoardIO()
      
        # Quirk: You must set the XRP LED to False to initialize it
        self.io.setLed(False)

        self.drivetrain = self.initDrivetrain(DigitalChannelConstants.LEFT_MOTOR_CHANNEL, DigitalChannelConstants.RIGHT_MOTOR_CHANNEL)

        self.rangeFinder = xrp.XRPRangefinder()
        #self.lf = xrp.XRPReflectanceSensor()

        # State variable to keep track of whether we've finished the autonomous behavior
        self.ran = False

    def initDrivetrain(self, leftMotorChannel, rightMotorChannel):
        leftmotor = xrp.XRPMotor(leftMotorChannel)
        rightmotor = xrp.XRPMotor(rightMotorChannel)
        rightmotor.setInverted(True)

        drivetrain = wpilib.drive.DifferentialDrive(
            leftmotor,
            rightmotor
            )
        return drivetrain
            
    def robotPeriodic(self):
        self.drivetrain.feed()

    def autonomousInit(self):
        print("autoInit")
        self.io.setLed(True)
        
        self.drivetrain.tankDrive(ControlConstants.LEFT_MOTOR_SPEED, ControlConstants.RIGHT_MOTOR_SPEED)    
        self.ran = False
        
    def autonomousPeriodic(self):
        if self.ran == True:
            return
        
        # Our robots work in inches, but function returns meters
        range_to_wall = units.metersToInches(self.rangeFinder.getDistance())

        print(f"Range to wall: {range_to_wall:.1f} inches")

        if range_to_wall <= ControlConstants.WALL_STOP_DISTANCE: 
             self.drivetrain.stopMotor()
             self.io.setLed(False)
             self.ran = True
             print("Stopped")
    
    def autonomousEnd(self):
        self.drivetrain.stopMotor()
        
    def teleopInit(self):
        print("teleopInit")
        self.io.setLed(False)
        
    def disabledInit(self):
        pass
        
