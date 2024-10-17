#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib

import constants

from commands.autos import Autos
from commands.launchnote import LaunchNote
from commands.preparelaunch import PrepareLaunch

import commands2

from subsystems.drivetrain import DriveSubsystem
from subsystems.launcher import LauncherSubsystem

from wpilib import SendableChooser

# from subsystems.pwm_drivesubsystem import DriveSubsystem
# from subsystems.pwm_launchersubsystem import LauncherSubsystem


class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:
        # The driver's controller
        self.driverController = wpilib.XboxController(
            constants.kDriverControllerPort
        )

        # The robot's subsystems
        self.drive = DriveSubsystem()
        self.launcher = LauncherSubsystem()

        self.configureButtonBindings()

        self.drive.setDefaultCommand(
            # A split-stick arcade command, with forward/backward controlled by the left
            # hand, and turning controlled by the right.
            commands2.cmd.run(
                lambda: self.drive.arcadeDrive(
                    self.driverController.getLeftY(),
                    -self.driverController.getRightX(),
                ),
                self.drive,
            )
        )

        self.chooser = SendableChooser()
        
        self.chooser.setDefaultOption("None", 0)
        self.chooser.addOption("Leave", 1)
        self.chooser.addOption("Front Speaker", 2)
        self.chooser.addOption("Blue Amp Side Speaker", 3)
        self.chooser.addOption("Blue Feed Side Speaker", 4)
        self.chooser.addOption("Red Amp Side Speaker", 5)
        self.chooser.addOption("Red Feed Side Speaker", 6)

        wpilib.SmartDashboard.putData("Auto Select", self.chooser)


    def configureButtonBindings(self):

        commands2.button.JoystickButton(self.driverController, wpilib.XboxController.Button.kRightBumper).whileTrue(PrepareLaunch(self.launcher)
            .withTimeout(constants.kLauncherDelay)
            .andThen(LaunchNote(self.launcher))
            .handleInterrupt(lambda: self.launcher.stop()))

        commands2.button.JoystickButton(self.driverController, wpilib.XboxController.Button.kLeftBumper).whileTrue(self.launcher.getIntakeCommand())

    def getAutonomousCommand(self) -> commands2.Command:
        if self.chooser.getSelected() == 0:
            pass
        elif self.chooser.getSelected() == 1:
            Autos.exampleAuto(self.drive, self.launcher)
        elif self.chooser.getSelected() == 2:
            Autos.speaker_center(self.drive, self.launcher)
        elif self.chooser.getSelected() == 3:
            Autos.amp_side_speaker(self.drive, self.launcher, 1)
        elif self.chooser.getSelected() == 4:
            Autos.feed_side_speaker(self.drive, self.launcher, 1)
        elif self.chooser.getSelected() == 5:
            Autos.amp_side_speaker(self.drive, self.launcher, -1)
        elif self.chooser.getSelected() == 6:
            Autos.feed_side_speaker(self.drive, self.launcher, -1)