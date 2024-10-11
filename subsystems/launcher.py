#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import phoenix5

import constants


class LauncherSubsystem(commands2.Subsystem):
    def __init__(self) -> None:
        super().__init__()
        """The two motors of the launcher subsytem"""
        self.feedWheel = phoenix5.WPI_TalonSRX(
            constants.kFeederMotor
        )
        self.launchWheel = phoenix5.WPI_TalonSRX(
            constants.kLauncherMotor
        )
        # self.supply_limit_config = phoenix5.SupplyCurrentLimitConfiguration()
        # self.supply_limit_config.currentLimit = constants.kFeedCurrentLimit
        # self.feedWheel.configSupplyCurrentLimit(self.supply_limit_config)
        # self.launchWheel.setSmartCurrentLimit(constants.kLauncherCurrentLimit)

    def getIntakeCommand(self) -> commands2.Command:
        """The startEnd helper method takes a method to call when the command is initialized and one to
        call when it ends"""
        return commands2.cmd.startEnd(
            # When the command is initialized, set the wheels to the intake speed values
            lambda: self.setWheels(
                constants.kIntakeLauncherSpeed, constants.kIntakeFeederSpeed
            ),
            # When the command stops, stop the wheels
            lambda: self.stop(),
            self,
        )

    def setWheels(self, launch: float, feed: float) -> None:
        """A method to set both wheels so we have a single method to use as a lambda for our command factory"""
        self.setLaunchWheel(launch)
        self.setFeedWheel(feed)

    def setLaunchWheel(self, speed: float) -> None:
        """An accessor method to set the speed (technically the output percentage) of the launch wheel"""
        self.launchWheel.set(phoenix5.ControlMode.PercentOutput, speed)

    def setFeedWheel(self, speed: float) -> None:
        """An accessor method to set the speed (technically the output percentage) of the feed wheel"""
        self.feedWheel.set(phoenix5.ControlMode.PercentOutput, speed)

    def stop(self) -> None:
        """A helper method to stop both wheels. You could skip having a method like this and call the
        individual accessors with speed = 0 instead"""
        self.launchWheel.set(phoenix5.ControlMode.PercentOutput, 0)
        self.feedWheel.set(phoenix5.ControlMode.PercentOutput, 0)
