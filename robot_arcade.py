import os
import wpilib
import wpilib.drive
import xrp

# If your XRP isn't at the default address, set that here
os.environ["HALSIMXRP_HOST"] = "192.168.42.1"
os.environ["HALSIMXRP_PORT"] = "3540"

class ArcadeRobot(wpilib.TimedRobot):
    def robotInit(self) -> None:
        leftMotor = xrp.XRPMotor(0)
        rightMotor = xrp.XRPMotor(1)
        rightMotor.setInverted(True)
        self.leftMotorEncoder = wpilib.Encoder(4,5)
        self.rightMotorEncoder = wpilib.Encoder(6,7)

        self.drive = wpilib.drive.DifferentialDrive(leftMotor, rightMotor)
        self.stick = wpilib.Joystick(0)

    def teleopPeriodic(self) -> None:
        self.drive.arcadeDrive(xSpeed=self.stick.getX(), zRotation=self.stick.getY())