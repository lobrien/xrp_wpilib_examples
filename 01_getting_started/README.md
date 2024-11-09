# Getting started programs

This subdirectory has self-contained programs that use the XRP's most important on-board features: the LED, the motors and encoders, the servo, the gyro, and the ultrasonic range finder (TODO).

I didn't write sample code for the line sensor because I couldn't relate it to any FRC game I'm familiar with. (I imagine it's just as simple to use as the other hardware!)

All of the robots in this directory are `TimedRobot`s because such robots are simpler than command-based robots. Behavior is mostly started in `autonomousInit`, and stopped in either `autonomousExit` or due to simple logic in `autonomousPeriodic`. 

The programs are:

## **hello_robot.py**

This program turns on the LED when the autonomous mode begins and off when it ends. 

## **hello_motor.py**

This extends the code in **hello_robot.py** to start a single one of the motors on the XRP. 

Running the motor at less than 100% effort is a good opportunity to show that mechanical behavior is more variable than software behavior. I happened to first run this in front of the team as my rechargeable batteries were too weak to turn the wheel even in air (ah, the Demo Gods!). You might be able to find a power level that's sufficient to turn the wheel in the air but not on a surface. 

## **hello_encoders.py**

This is longer code that introduces both the encoder hardware and the `DifferentialDrive`. 

I think it's worthwhile to spend some time going over `robotInit` for this. It's got concepts like Digital IO channels, inverting a motor, and the use of higher-abstraction `wpilib` classes.

One thing I _don't_ do is turn off motor safety with `setSafetyEnabled(False)`. Instead, I call `feed()` in `robotPeriodic` with no guarding logic. I didn't want to suggest turning off motor safety (harmless with the XRP, I would think, not so with a competition robot). But is it wiser to call `feed()` with no logic, in a separate area of the code where it's purpose may be obscure? I dunno'.

You may be horrified that this code uses raw ticks for distance. I wanted to introduce the physical structure of encoders at this point, thinking that unlike LEDs and motors, this might be their first time encountering the concept. 

This is the first use of `autonomousPeriodic`. You may or may not want to point out that this `if-then` logic is evaluated every 20ms. I didn't want to complicate things with a discussion of state-machines, even though:

This code also uses `robotPeriodic`. And you've probably already introduced how the modes all follow the same pattern of `{mode}Init`, `{mode}Periodic`, `{mode}Exit`. Still,  I delayed using a sentinel variable until: 

## **hello_distance.py**

New team members may not have fully internalized applying their academic math knowledge to real-world problems. I think the first year I mentored FRC I didn't even pause after saying "2πr, right?". So I like to go slow with this one, especially because it also demonstrates using a datasheet to get precise numbers rather than measuring or using a binary search of constants to fine-tune constants.

(Tangent (heh heh): First and even second year HS students probably have familiarity with the use of π, but in our local curriculum Trigonometry is a sophomore subject. They likely haven't yet heard of SOHCAHTOA and can't be expected to answer "So if we know this angle and that length, how do we tell...?")

Inches. Yeah, I know. I weakly hold the position that inches, degrees, and pounds are the appropriate units of measure in FRC. The hardware is almost certainly going to be in Imperial units. I think it's more important that team members communicate well with each other than lecturing them on SI units. 

I don't use the `wpilib` units of measure yet. I think that can wait, even though I feel pretty strongly that they should be used during the season. 

The other new technique here is the use of `self.ran` to short-circuit `autonomousPeriodic`. I think it's important to point out that member variables should be declared and, if at all possible, assigned in `robotInit()` (I think `__init__(self)` can wait). 

## **hello_servo.py**

I think this makes sense here. Code-wise, I don't think it adds anything.

## **hello_gyro.py** 

As I write this, this robot is confusing me! It seems to me that `Gyro.getAngle()` will return negative values for a while and then it will switch to positive (i.e., -88, -89, 270)! 

This is an opportunity to introduce the concept of normalization, but I'm honestly taken aback by this behavior! 

## **hello_distance.py**

tk

## **hello_everything_together**

tk 