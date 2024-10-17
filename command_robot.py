import wpilib
import wpilib.drive
import commands2

import xrp
import os
import ntcore

# This is easier than environment variables on every dev machine
os.environ["HALSIMXRP_HOST"] = "192.168.42.1"
os.environ["HALSIMXRP_PORT"] = "3540"

# Never changes
class CommandRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.container = MyContainer()
        self.autonomous_command = None

    # Every 20ms in all modes
    def robotPeriodic(self):
        commands2.CommandScheduler.getInstance().run()

    def autonomousInit(self):
        self.autonomous_command = self.container.getAutonomousCommand()
        if self.autonomous_command:
            self.autonomous_command.schedule()
        
    def teleopInit(self):
        if self.autonomous_command:
            self.autonomous_command.cancel()

    def testInit(self):
        commands2.CommandScheduler.getInstance().cancelAll()

# Never changes (?).
class MyContainer:
    def __init__(self):
        self.drive = DriveSubsystem()

    def getAutonomousCommand(self):
        return AutonomousCommand(self.drive)

# Definitely changes w hardware, but not so much as commands
class DriveSubsystem(commands2.SubsystemBase):
    def __init__(self):
        self.io = xrp.XRPOnBoardIO()
        # Quirk: You must set the XRP LED to False to initialize it
        self.io.setLed(False)

        self.leftMotor = xrp.XRPMotor(0)
        self.rightMotor = xrp.XRPMotor(1)
        self.rightMotor.setInverted(True)

        self.driver = wpilib.drive.DifferentialDrive(self.leftMotor, self.rightMotor)
        self.driver.feed()
        # TODO: Can't be right, but I get timeout exception after ending autonomous
        self.driver.setSafetyEnabled(False)

    def drive(self, speed: float, rotation: float):
        self.driver.arcadeDrive(speed, rotation)
        
def AutonomousCommand(drive: DriveSubsystem):
       return CircleCWForward(drive).andThen(CircleCWBack(drive))

class CircleCWForward(commands2.CommandBase):
    def __init__(self, drive: DriveSubsystem):
        self.drive_system = drive
        self.addRequirements(drive)

        # Maybe you don't need this: can't you schedule a command to run for n seconds?
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.start()
        self.drive_system.io.setLed(True)

    def execute(self):
        self.drive_system.drive(1.0, -0.5)

    def isFinished(self):
        return self.timer.get() > 2.0
    
    def end(self, interrupted : bool):
        self.drive_system.io.setLed(False)
        self.drive_system.drive(0, 0)
        

class CircleCWBack(commands2.CommandBase):
    def __init__(self, drive: DriveSubsystem):
        self.drive_system = drive
        self.addRequirements(drive)

        # Maybe you don't need this: can't you schedule a command to run for n seconds?
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.start()
        self.drive_system.io.setLed(True)

    def execute(self):
        self.drive_system.drive(-1.0, -0.5)

    def isFinished(self):
        return self.timer.get() > 2.0
    
    def end(self, interrupted : bool):
        self.drive_system.io.setLed(False)
        self.drive_system.drive(0, 0)
        