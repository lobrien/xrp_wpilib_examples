## Network Tables and State Machines

Controllers are pretty basic and I could see putting **hello_controller.py** in the first folder. Yeah, maybe I should do that. 

**hello_shuffleboard.py**

I'm a *big* fan of using Network Tables for debugging robot behavior and tweaking configurable values. 

I guess I could call this **hello_pubsub.py**, but I think Shuffleboard is the most approachable of the GUIs. 

I don't know if the WPILib installer puts the FRC Tools in your path, but you can find Shuffleboard at:

- Windows: tk
- Mac: ~/wpilib/2024/tools Run: `{path_to}/Shuffleboard.py` 

This code demonstrates 2 behaviors in Teleop mode: the value of the left joystick is shown in Shuffleboard, and reads the Boolean variable `XRPRobot/SetLed` from Network Tables. To demonstrate this, drag a Toggle Button or a Toggle Switch from the Widgets pane of the left-hand window (possibly collapsed at first). 

Right-click on the toggle widget, choose "Properties..." and set the title to `XRPRobot/SetLed`.

Frustratingly, you cannot set an initial value within Shuffleboard! (At least, not on the Mac). Instead, you MUST set its initial value in your robot code. Only then will the widget activate. You can then subscribe to the `XRPRobot/SetLed` topic and manipulate robot state based on Shuffleboard state. 



