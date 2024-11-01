# Getting started with `wpilib` on XRP

The [Experiential Robotics Platform](https://experientialrobotics.org/) is an open robotics platform that is perfect for introducing learners to the `wpilib` library that is used by [FIRST Robotics Competition](https://www.firstinspires.org/robotics/frc).

TODO: Need an image here

This repository is a series of "the simplest robot code that could possibly work" examples for XRP and `wpilib`. The programming language is Python and `wpilib` is accessed via `robotpy`. 

## Installation

Prerequisites: 

- Assembled [XRP](https://www.sparkfun.com/products/22230) 
- [Install Python 3.12 on your development computer(s)](https://www.python.org/downloads/)
- [Install FRC Game, `wpilib`, and RobotPy on your dev computer(s)](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/frc-game-tools.html)
- [Install `wpilib` on the XRP](https://docs.wpilib.org/en/stable/docs/xrp-robot/hardware-and-imaging.html) 
- Optional but highly recommended: [Install Poetry on your dev machines](https://python-poetry.org/docs/)
- Run `poetry init`. This uses the `pyproject.toml` project configuration file and the `poetry.lock` file to determine what packages will be downloaded (by `pip` behind the scenes). The `poetry.lock` file contains the pre-resolved versions needed, which is delightful in complex projects.

## Running XRP programs

Unlike with the RoboRio, wpilib programs run on the XRP execute on the developer's computer with the WPI Simulation GUI. When the XRP starts, it creates its own WiFi network. This network is named something like **tk** and has a default password of **xrp-wpilib**. ([You can configure this.](https://docs.wpilib.org/en/stable/docs/xrp-robot/web-ui.html))

On its network, the default IP address of the XRP robot is **192.168.42.1** and it listens on port **3540**. You can set the environment variables `HALSIMXRP_HOST` and `HALSIMXRP_PORT` to these values, but the programs in this repo use Python's `os.environ` to do this, so as to minimize the configuration burden on users. 

To run a RobotPy program:

- Open a terminal 
- Switch to the repo root
- Run `poetry shell` to activate the Poetry environment, **and then**
- Run `robotpy --main hello_robot.py sim --xrp`; **or just run** 
- Run `poetry run robotpy --main hello_robot.py sim --xrp` 

The WPI Simulation GUI will appear. Despite this being the "simulation" GUI, the XRP robot _is_ active. 

tk Need an image here

**Protip:** The Simulation GUI will appear whether you are connected to the XRP's WiFi network or not. If you forgot to do so, or if you automatically switch to another preferred network, you may spend some time wondering why your robot isn't running properly (ask me how I know).

## Repository structure

I have roughly sequenced the programs in this repo from less to more complex and each of the numbered source repos has a README.md where I suggest even more structure:

- [Getting Started](01_getting_started/README.md)
- [Controllers, Network Tables, and State Machines](02_controllers_network_tables_and_state_machines/README.md)
- [Organizing Code](03_organizing_code)

## The Simplest Robot That Could Possibly Work

The first program to run is **01_getting_started/hello_robot.py**. This is a `TimedRobot` that turns the XRP's onboard LED on when Autonomous mode starts and off when Teleoperated mode does:

```python
import wpilib  # (1)!
import xrp
import os 

# This is easier than environment variables on every dev machine
os.environ["HALSIMXRP_HOST"] = "192.168.42.1" 
os.environ["HALSIMXRP_PORT"] = "3540"

class MyRobot(wpilib.TimedRobot):  # (2)!
    def robotInit(self):
        self.io = xrp.XRPOnBoardIO()
        
        # Quirk: You must set the XRP LED to False to initialize it
        self.io.setLed(False)
        
    def autonomousInit(self): 
        print("autoInit")
        self.io.setLed(True)

    def teleopInit(self):
        print("teleopInit")
        self.io.setLed(False)
```

1.  Import necessary modules: `wpilib` for general robot functionality, `xrp` for XRP hardware, and the `os` module to set the necessary environment variables
2. This repository starts with an emphasis on `TimedRobot`s. `CommandRobot`s are introduced in **tk**. IMO `CommandRobot`s are likely a better architecture for an actual FRC robot, but for learning purposes, `TimedRobot`s are ideal for discussing the FRC-match state-machine and are a good scaffold for a robot based on a Finite State Machine. 

## Safety

An aspect of XRP that I love is that it is low-voltage, making it much safer in terms of electricity and mechanical power than a typical RoboRio-based FIRST robot. 

## Code Style

There are a number of Python language features that I have deliberately avoided in this repo. This code is deliberately targeted to communicate with newer developers. 

### Classes only

FRC programmers must be comfortable with Object-Oriented Programming. Although Python does perfectly well with just functions, this repo puts all code (with the notable exception of the `os.environ` assignments) inside classes. 

At this point, the repo doesn't even have any class variables or functions, although I think they're pretty reasonable to use with all but quite new developers. 

### No lambda functions

In my experience, anonymous functions are significantly more challenging to understand than references to named functions. Named functions are a little more wordy but are known entities. Heck, encouraging learners to write more functions and fewer enormous blocks is a worthy goal in itself.

### No recursion

When I was a magazine editor, I had a (half-serious) joke that if an author said "recursion is easy," nothing else they said could be trusted either. 

Recursion is good. Recursion is clear in retrospect. Recursion is generally more elegant than iteration. But unless their introductory programming book is [SICP](https://en.wikipedia.org/wiki/Structure_and_Interpretation_of_Computer_Programs), recursion is not the way new developers are taught to approach problems. (And if they're learning from SICP, you can certainly use lambdas, too.)

### No type hints, few comments

It stabs me to the heart to conclude that, unless `mypy` is integrated into your build process, type hints are more trouble than they're worth for new FRC developers. My issue is that FRC code is _particularly_ prone to being updated on the fly and everything that's optional becomes obsolete very quickly.

Out-of-date comments are worse than no comments and incorrect type hints are worse than out-of-date comments. But as far as I know, even if you install `mypy` support in Visual Studio Code mistakes appear as "Problems" warnings and not as errors. (Let me know if I'm wrong, because I would _love_ to be wrong!) 

Speaking of comments, this sample code intentionally has very few. In my opinion, the purpose of sample code is to understand **the code**, not the intention. The intention should be spelled out in an accompanying article, video, or live lecture. "If something in your code needs explaining, you need to explain it in your article," was one of my editorial rules. 

And let's be honest: cut-and-paste is common. Cut-and-pasted comments are highly likely to become out-of-date, since the very fact that the code was copied implies that the dev does not think of the code as their responsibility. 

To be clear: Production code _should_ have both inline and reference comments. The lack of commenting in this repo is an artifact of its unusual purpose as tutorial material.



