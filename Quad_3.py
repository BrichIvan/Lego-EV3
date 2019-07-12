#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import paho.mqtt.client as mqtt
import time

class Robot(object):
	def __init__ (self, speed, speed_ang, sm, angle):
		self.speed = speed
		self.speed_ang = speed_ang
		self.sm = sm
		self.angle = angle

	def drive_sm (self, sm, left_motor, right_motor, gy, us, a):
		distance_ang = sm * -20.5
		left_motor.position_sp = distance_ang
		right_motor.position_sp = distance_ang
		left_motor.speed_sp = self.speed
		right_motor.speed_sp = self.speed

		left_motor.run_to_rel_pos()
		right_motor.run_to_rel_pos()

		while (left_motor.is_running or right_motor.is_running):
			pass

	def rotate_angle (self, angle, left_motor, right_motor, gy, us, a):
		k = 0.035
		angle = angle + self.angle
		if (self.angle > angle):
			left_motor.speed_sp = self.speed_ang
			right_motor.speed_sp = -1 * self.speed_ang
			left_motor.run_forever()
			right_motor.run_forever()

			while (gy.value() >= (angle + k*self.speed_ang)):
				pass
		else:
			left_motor.speed_sp = -1 * self.speed_ang
			right_motor.speed_sp = self.speed_ang

			left_motor.run_forever()
			right_motor.run_forever()

			while (gy.value() <= (angle - k*self.speed_ang)):
				pass

		left_motor.stop()
		right_motor.stop()


# MQTT def

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
	gy.mode = 'GYRO-RATE'
	gy.mode = 'GYRO-ANG' #put the gyro into angule
	
	while (not(gy.value() == 0)) :
		pass

	gy.mode = 'GYRO-ANG'

lego_id = 1
a = dict.fromkeys(['topic', 'data'])
a["topic"] = "Sensors/" + str(lego_id)
def main():
	initialization()
	left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
	right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
	gy = ev3.GyroSensor(ev3.INPUT_3)
	us = ev3.UltrasonicSensor(ev3.INPUT_4)
	print('Ready')

	Machine = Robot(200, 100, 0, 0)
	#Machine.rotate_angle(-10, left_motor, right_motor, gy, us, a)
	while (1):
		# Listen to mqtt
		command = input()
		command = command.strip().split()
		command = list(map(int, command))

		if command[0] == 0:
			x = command[1]
			#print(x)
			Machine.rotate_angle(x, left_motor, right_motor, gy, us, a)
		else:
			y = command[1]
			#print (y)
			Machine.drive_sm(y, left_motor, right_motor, gy, us, a)

		distance = us.value()
		self.angle = gy.value()
		a["data"] = [str(distance), str(self.angle)]
		print (a["data"][0] + ' ' + a["data"][1])

		time.sleep(0.2)


main()
