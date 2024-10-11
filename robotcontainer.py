#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
from wpilib.interfaces import GenericHID

import commands2
import commands2.button

import constants

from commands.autos import Autos
from commands.launchnote import LaunchNote
from commands.preparelaunch import PrepareLaunch

from subsystems.drivetrain import DriveSubsystem
from subsystems.launcher import LauncherSubsystem

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
        self.driverController = commands2.button.CommandXboxController(
            constants.kDriverControllerPort
        )
        self.operatorController = commands2.button.CommandXboxController(
            constants.kOperatorControllerPort
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
                    -self.driverController.getLeftY(),
                    -self.driverController.getRightX(),
                ),
                self.drive,
            )
        )

    def configureButtonBindings(self):
        self.operatorController.a().whileTrue(
            PrepareLaunch(self.launcher)
            .withTimeout(constants.kLauncherDelay)
            .andThen(LaunchNote(self.launcher))
            .handleInterrupt(lambda: self.launcher.stop())
        )

        self.operatorController.leftBumper().whileTrue(self.launcher.getIntakeCommand())

    def getAutonomousCommand(self) -> commands2.Command:
        return Autos.exampleAuto(self.drive)
