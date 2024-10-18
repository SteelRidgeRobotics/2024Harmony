#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import wpilib
import wpilib.drive
import phoenix5

import constants


class DriveSubsystem(commands2.Subsystem):
    def __init__(self) -> None:
        super().__init__()

        self.front_left = phoenix5.TalonFX(
            constants.kLeftMotor1Port
        )
        self.back_left = phoenix5.TalonFX(
            constants.kLeftMotor2Port
        )
        self.front_right = phoenix5.TalonFX(
            constants.kRightMotor1Port
        )
        self.back_right = phoenix5.TalonFX(
            constants.kRightMotor2Port
        )

        # Set current limits for the drivetrain motors
        # self.front_left.setSmartCurrentLimit(constants.kDTCurrentLimit)
        # self.back_left.setSmartCurrentLimit(constants.kDTCurrentLimit)
        # self.front_right.setSmartCurrentLimit(constants.kDTCurrentLimit)
        # self.back_right.setSmartCurrentLimit(constants.kDTCurrentLimit)

        self.back_left.follow(self.front_left, phoenix5.FollowerType.PercentOutput)
        self.back_right.follow(self.front_right, phoenix5.FollowerType.PercentOutput)

        self.front_left.setInverted(phoenix5.InvertType.InvertMotorOutput)
        self.back_left.setInverted(phoenix5.InvertType.FollowMaster)

        self.front_left.setNeutralMode(phoenix5.NeutralMode.Brake)
        self.front_right.setNeutralMode(phoenix5.NeutralMode.Brake)
        self.back_left.setNeutralMode(phoenix5.NeutralMode.Brake)
        self.back_right.setNeutralMode(phoenix5.NeutralMode.Brake)

    def arcadeDrive(self, fwd: float, rot: float, slow: bool) -> None:
        """
        Drives the robot using arcade controls.

        :param fwd: the commanded forward movement
        :param rot: the commanded rotation
        """
        
        left = fwd + rot if not slow else (fwd + rot) * 0.2
        right = fwd - rot if not slow else (fwd - rot) * 0.2

        self.front_left.set(phoenix5.ControlMode.PercentOutput, left)
        self.front_right.set(phoenix5.ControlMode.PercentOutput, right)
