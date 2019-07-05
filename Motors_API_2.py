#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time

left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

assert left_motor.connected
assert right_motor.connected

left_motor.speed_sp = 500
left_motor.time_sp = 3000
left_motor.stop_action = ev3.Motor.STOP_ACTION_BRAKE

right_motor.speed_sp = 500
right_motor.time_sp = 3000
right_motor.stop_action = ev3.Motor.STOP_ACTION_BRAKE
right_motor.run_timed()
left_motor.run_timed()

