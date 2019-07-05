#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time

class Robot(object):
	def __init__ (self, speed, speed_ang, sm):
		self.speed = speed
		self.speed_ang = speed_ang
		self.sm = sm
		#self.angle

	def drive_sm (self, left_motor, right_motor):
		distance_ang = self.sm * -20.5
		left_motor.position_sp = distance_ang
		right_motor.position_sp = distance_ang
		left_motor.speed_sp = self.speed
		right_motor.speed_sp = self.speed

		left_motor.run_to_rel_pos()
		right_motor.run_to_rel_pos()
		
		left_motor.wait_while(ev3.Motor.STATE_RUNNING)
		right_motor.wait_while(ev3.Motor.STATE_RUNNING)

	def rotate_angle (self, left_motor, right_motor):
		left_motor.position_sp = 200
		right_motor.position_sp = -200
		left_motor.speed_sp = self.speed_ang
		right_motor.speed_sp = self.speed_ang
		
		left_motor.run_to_rel_pos()
		right_motor.run_to_rel_pos()

		left_motor.wait_while(ev3.Motor.STATE_RUNNING)
		right_motor.wait_while(ev3.Motor.STATE_RUNNING)

def initialization():
	left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
	right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

	assert left_motor.connected
	assert right_motor.connected

	left_motor.stop_action = ev3.Motor.STOP_ACTION_BRAKE
	right_motor.stop_action = ev3.Motor.STOP_ACTION_BRAKE

def main():
	initialization()
	Machine = Robot(400, 200, 40)
	for k in range (4):
		Machine.drive_sm(left_motor, right_motor)
		time.sleep(0.01)
		Machine.rotate_angle(left_motor, right_motor)
		time.sleep(0.01)

main()
