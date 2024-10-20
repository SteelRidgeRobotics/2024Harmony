#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import constants
from subsystems.launcher import LauncherSubsystem


class LaunchNote(commands2.Command):
    def __init__(self, launcher: LauncherSubsystem) -> None:
        super().__init__()
        self.launcher = launcher
        self.addRequirements(launcher)

    def initialize(self) -> None:
        self.launcher.setLaunchWheel(constants.kLauncherSpeed)
        self.launcher.setFeedWheel(constants.kLaunchFeederSpeed)

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool) -> None:
        self.launcher.stop()
