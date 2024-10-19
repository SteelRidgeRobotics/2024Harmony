#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import constants

# from subsystems.can_drivesubsystem import DriveSubsystem
from subsystems.drivetrain import DriveSubsystem
from subsystems.launcher import LauncherSubsystem

class Autos(commands2.Command):
    def __init__(self, drive: DriveSubsystem, launcher: LauncherSubsystem) -> None:
        super().__init__()
        self.drive = drive
        self.launcher = launcher
        self.addRequirements(drive)

    def doNothing(self) -> commands2.Command:

        return (commands2.cmd.run(lambda: self.drive.arcadeDrive(0, 0, False), self.drive))

    def exampleAuto(self) -> commands2.Command:
        return (
            commands2.cmd.run(lambda: self.drive.arcadeDrive(-0.5, 0, False), self.drive)
            .withTimeout(1.0)
            .andThen(
                commands2.cmd.run(lambda: self.drive.arcadeDrive(0, 0, False), self.drive)
            )
        )
    
    def speaker_center(self) -> commands2.Command:
        return (
            commands2.cmd.run(lambda: self.launcher.setLaunchWheel(constants.kLauncherSpeed))
            .withTimeout(constants.kLauncherDelay)
            .andThen(
                lambda: self.launcher.setFeedWheel(constants.kLaunchFeederSpeed)
            )
            .withTimeout(1)
            .andThen(
                lambda: self.launcher.stop()
            )
            .andThen(
                lambda: self.drive.arcadeDrive(constants.kAutoSpeed,0, False)
            )
            .withTimeout(1)
        )
    def amp_side_speaker(self, team = 1) -> commands2.Command:
        return (
            commands2.cmd.run(lambda: self.launcher.setLaunchWheel(constants.kLauncherSpeed))
            .withTimeout(constants.kLauncherDelay)
            .andThen(
                lambda: self.launcher.setFeedWheel(constants.kLaunchFeederSpeed)
            )
            .withTimeout(1)
            .andThen(
                lambda: self.launcher.stop()
            )
            .andThen(
                lambda: self.drive.arcadeDrive(constants.kAutoSpeed, team * constants.kAutoTurnAmp, False)
            )
            .withTimeout(1)
        )
    
    def feed_side_speaker(self, team = 1) -> commands2.Command:
        
        return (
            commands2.cmd.run(lambda: self.launcher.setLaunchWheel(constants.kLauncherSpeed))
            .withTimeout(constants.kLauncherDelay)
            .andThen(
                lambda: self.launcher.setFeedWheel(constants.kLaunchFeederSpeed)
            )
            .withTimeout(1)
            .andThen(
                lambda: self.launcher.stop()
            )
            .andThen(
                lambda: self.drive.arcadeDrive(constants.kAutoSpeed, 0, False)
            )
            .withTimeout(1)
            .andThen(
                lambda: self.drive.arcadeDrive(0, team * constants.kAutoTurnFeed, False)
            )
            .withTimeout(.5)
            .andThen(
                lambda: self.drive.arcadeDrive(constants.kAutoSpeed, 0, False)
            )
            .withTimeout(1)
        )