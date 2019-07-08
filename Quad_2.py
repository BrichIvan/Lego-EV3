#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time

class Robot(object):
	def __init__ (self, speed, speed_ang, sm, angle):
		self.speed = speed
		self.speed_ang = speed_ang
		self.sm = sm
		self.angle = angle

	def drive_sm (self, sm, left_motor, right_motor):
		distance_ang = self.sm * -20.5
		left_motor.position_sp = distance_ang
		right_motor.position_sp = distance_ang
		left_motor.speed_sp = self.speed
		right_motor.speed_sp = self.speed

		left_motor.run_to_rel_pos()
		right_motor.run_to_rel_pos()

	def rotate_angle (self, angle, left_motor, right_motor):
		left_motor.position_sp = self.angle * 2.2
		right_motor.position_sp = -1 * self.angle * 2.2
		left_motor.speed_sp = self.speed_ang
		right_motor.speed_sp = self.speed_ang
		
		left_motor.run_to_rel_pos()
		right_motor.run_to_rel_pos()

		left_motor.wait_while(ev3.Motor.STATE_RUNNING)
		right_motor.wait_while(ev3.Motor.STATE_RUNNING)

	def check_distance (self, left_motor, rigt_motor, Analsys, us):
		while (left_motor.is_running or right_motor.is_runnnig):
			distance = Analsys.read_distance(us)
			print (str(distance))
			time.sleep(0.1)

class Sensors(object):
        def __init__ (self, gy, us):
                self.gy = gy
                self.us = us
                #self.angle_ac

        def read_angle(self, gy):
                angle = gy.value()
                return angle

        def read_distance(self, us):
                distance = us.value()
                return distance
'''
                #Should be called wth high frequency
        def read_accurate_angle(self, angle_ac) #Gyro should transmit $
                delta_millis = millis - int(round(time.time()*1000))
                #print(delta_millis)
                angle_ac = angle_ac + delta_millis * gy.value()
                millis = int(round(time.time()*1000))
'''


def initialization():
	left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
	right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
	gy = ev3.GyroSensor(ev3.INPUT_3)
	us = ev3.UltrasonicSensor(ev3.INPUT_4)

	assert left_motor.connected
	assert right_motor.connected
	assert gy.connected
	assert us.connected

	left_motor.stop_action = ev3.Motor.STOP_ACTION_BRAKE
	right_motor.stop_action = ev3.Motor.STOP_ACTION_BRAKE     

	us.mode = 'US-DIST-CM'  #put the US in the dist in sm mode 
	gy.mode = 'GYRO-ANG' #put the gyro into angule


def main():
	initialization()
	left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
	right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
	gy = ev3.GyroSensor(ev3.INPUT_3)
	us = ev3.UltrasonicSensor(ev3.INPUT_4)

	Analsys = Sensors(gy, us)
	Machine = Robot(400, 200, 40, 90)
	for k in range (4):
		Machine.drive_sm(40, left_motor, right_motor)
		Machine.check_distance(left_motor, rught_motor, Analsys, us)
		time.sleep(0.01)
		Machine.rotate_angle(90, left_motor, right_motor, Analsys)
		time.sleep(0.01)

main()
