import wpilib
from wpimath.units import seconds
import xrp
import os
import ntcore

# If your XRP isn't at the default address, set that here
os.environ["HALSIMXRP_HOST"] = "192.168.42.1"
os.environ["HALSIMXRP_PORT"] = "3540"

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.gyro = xrp.XRPGyro()
        self.motor0 = xrp.XRPMotor(0)
        self.motor1 = xrp.XRPMotor(1)
        self.io = xrp.XRPOnBoardIO()
        self.motor1.setInverted(True)
        self.controller = wpilib.Joystick(0)

        nt = ntcore.NetworkTableInstance.getDefault()
        self.table = nt.getTable("datatable")

        self.axisXPub = self.table.getDoubleTopic("X").publish()
        self.axisYPub = self.table.getDoubleTopic("Y").publish()

        print(f"self.motor0 {self.motor0.isAlive()}")

    ledTurnedOn = False


    def autonomousPeriodic(self) -> None:
        pass
        
    def teleopPeriodic(self):
        self.axisXPub.set(self.controller.getX())
        self.axisYPub.set(self.controller.getY())

        if self.controller.getTriggerPressed() and not self.ledTurnedOn:
            self.io.setLed(True)
            self.motor0.set(0.5)
            self.motor1.set(0.5)
            self.ledTurnedOn = True

