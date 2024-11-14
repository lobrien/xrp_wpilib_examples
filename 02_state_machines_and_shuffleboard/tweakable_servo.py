import wpilib
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

        self.controller = wpilib.XboxController(0)

        nt = ntcore.NetworkTableInstance.getDefault()
        self.table = nt.getTable("XRPRobot")

        self.axisXPub = self.table.getDoubleTopic("X").publish()
        self.axisYPub = self.table.getDoubleTopic("Y").publish()
        self.table.getEntry("Servo").setDouble(0) 

        self.servoControlSub = self.table.getDoubleTopic("Servo").subscribe(defaultValue=0.0)


        self.arm = xrp.XRPServo(4)
        self.arm.setAngle(0)
        

    def autonomousInit(self):
        print("autoInit")
        self.io.setLed(True)
        self.arm.setAngle(80.0)
        print(f"Angle arm {self.arm.getAngle()}, {self.arm.getPosition()}")

    def teleopPeriodic(self):
        if self.controller.getAButtonPressed():
            new_angle = self.arm.getAngle() + 10
            self.arm.setAngle(new_angle)
            print(f"Angle arm {self.arm.getAngle()}, {self.arm.getPosition()}")
        if self.controller.getBButtonPressed():
            new_angle = self.arm.getAngle() - 10
            self.arm.setAngle(new_angle)
            print(f"Angle arm {self.arm.getAngle()}, {self.arm.getPosition()}")
        

    def teleopInit(self):
        print("teleopInit")
        self.io.setLed(False)
        # 0.0 is fully away from body
        #self.arm.setPosition(0.05)
        print(f"Angle arm {self.arm.getAngle()}, {self.arm.getPosition()}")
       

    def disabledInit(self):
        self.arm.setPosition(0.95)
        print(f"Angle arm {self.arm.getAngle()}, {self.arm.getPosition()}")
       
        
