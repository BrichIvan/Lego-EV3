#! /usr/bin/env python3
import ev3dev.ev3 as ev3
import time 

class Robot(object):
	def __init__ (self, speed, speed_ang, sm):
		self.speed = speed
		self.speed_ang = speed_ang
		self.sm = sm

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

	def rotate_angle_anticlockwise (self, left_motor, right_motor):
		left_motor.position_sp = 200
		right_motor.position_sp = -200
		left_motor.speed_sp = self.speed_ang
		right_motor.speed_sp = self.speed_ang
		
		left_motor.run_to_rel_pos()
		right_motor.run_to_rel_pos()

		left_motor.wait_while(ev3.Motor.STATE_RUNNING)
		right_motor.wait_while(ev3.Motor.STATE_RUNNING)
	
	def rotate_angle_clockwise (self, left_motor, right_motor):
		left_motor.position_sp = -200
		right_motor.position_sp = 200
		left_motor.speed_sp = self.speed_ang
		right_motor.speed_sp = self.speed_ang
		
		left_motor.run_to_rel_pos()
		right_motor.run_to_rel_pos()

		left_motor.wait_while(ev3.Motor.STATE_RUNNING)
		right_motor.wait_while(ev3.Motor.STATE_RUNNING)
	


	
class Sensors(object):
	def __init__ (self, distance):		
		self.distance = distance

	def read_distance(self, us):
		distance = us.value()
		return distance





def initialization():
	left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
	right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
	us = ev3.UltrasonicSensor() 

	assert left_motor.connected
	assert right_motor.connected
	assert us.connected

	left_motor.stop_action = ev3.Motor.STOP_ACTION_BRAKE
	right_motor.stop_action = ev3.Motor.STOP_ACTION_BRAKE
	
	us.mode = 'US-DIST-CM'



def main():
	initialization()
	left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
	right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
	
	
	us = ev3.UltrasonicSensor()
	us.mode = 'US-DIST-CM'

	assert us.connected

	Analsys = Sensors(us)


	Machine = Robot(400, 200, 30)


	while (True):
		distance = Analsys.read_distance(us)
		print (str(distance))
		time.sleep(0.5)
		if distance < 200:
			Machine.rotate_angle_anticlockwise(left_motor, right_motor)
			time.sleep(0.01)
			Machine.drive_sm(left_motor, right_motor)
			time.sleep(0.01)
			Machine.rotate_angle_clockwise(left_motor, right_motor)
		else:
			left_motor.run_forever(speed_sp = -400)	
			right_motor.run_forever(speed_sp = -400)	


main()




	
	
