import os
import wpilib
import wpilib.drive
import xrp

# If your XRP isn't at the default address, set that here
os.environ["HALSIMXRP_HOST"] = "192.168.42.1"
os.environ["HALSIMXRP_PORT"] = "3540"

class Drive:
    def __init__(self):
        leftMotor = xrp.XRPMotor(0)
        rightMotor = xrp.XRPMotor(1)
        rightMotor.setInverted(True)
        self.leftMotorEncoder = wpilib.Encoder(4,5)
        self.rightMotorEncoder = wpilib.Encoder(6,7)

        self.differential_drive = wpilib.drive.DifferentialDrive(leftMotor, rightMotor)

    def tankDrive(self, xspeed : float, zrotation : float):
        self.differential_drive.tankDrive(xspeed, zrotation)

class DriverStation:
    def __init__(self):
        self.controller = wpilib.XboxController(0)
        

    def getLeftXY(self) -> tuple[float, float]:
        # Note that controller axes are different than wpilib axes
        # See: https://docs.wpilib.org/en/stable/docs/software/basic-programming/coordinate-system.html
        return -self.controller.getLeftX(), -self.controller.getLeftY()
    
    

class ArcadeRobot(wpilib.TimedRobot):
    def robotInit(self) -> None:
        self.drive = Drive()
        self.driver_station = DriverStation()

    def teleopPeriodic(self) -> None:
       x, y = self.driver_station.getLeftXY()
       self.drive.tankDrive(xspeed=x, zrotation=y)
        