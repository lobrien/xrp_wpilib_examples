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

        self.controller = wpilib.Joystick(0)

        nt = ntcore.NetworkTableInstance.getDefault()
        self.table = nt.getTable("XRPRobot")

        self.axisXPub = self.table.getDoubleTopic("X").publish()
        self.axisYPub = self.table.getDoubleTopic("Y").publish()
        self.driveRunningPub = self.table.getBooleanTopic("DriveRunning").publish()

    def autonomousPeriodic(self) -> None:
        pass
        
    def teleopPeriodic(self):
        self.axisXPub.set(self.controller.getX())
        self.axisYPub.set(self.controller.getY())

        if self.controller.getTriggerPressed() and self.driveRunning:
            self.motor0.stopMotor()
            self.motor1.stopMotor()
            self.driveRunning = False
        else:
            self.motor0.set(0.5)
            self.motor1.set(0.5)
            self.driveRunning = True
        self.driveRunningPub.set(self.driveRunning)
