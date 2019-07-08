#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time

class Sensors(object):
	def __init__ (self, angle, distance):
		self.angle = angle
		self.distance = distance
		#self.angle_ac

	def read_angle(self, gy):
		angle = gy.value()
		return angle

	def read_distance(self, us):
		distance = us.value()
		return distance
'''
		#Should be called wth high frequency
	def read_accurate_angle(self, angle_ac)	#Gyro should transmit raw values or speed
		delta_millis = millis - int(round(time.time()*1000))
		#print(delta_millis)
		angle_ac = angle_ac + delta_millis * gy.value()
		millis = int(round(time.time()*1000))
'''

#def initialization(gy, us):
	#us = ev3.UltrasonicSensor('in4')
	#us.mode='US-DIST-CM'	#put the US in the dist in sm mode

	#gy = ev3.GyroSensor('in3')
	#gy.mode = 'GYRO-ANG' #put the gyro into angle mode

	#assert gy.connected
	#assert us.connected

def main():
	gy = ev3.GyroSensor(ev3.INPUT_3)
	gy.mode = 'GYRO-ANG'
	
	us = ev3.UltrasonicSensor()
	us.mode = 'US-DIST-CM'

	assert gy.connected
	assert us.connected

	#initialization(gy, us)
	Analsys = Sensors(0, 0)
	while (True):
		angle = Analsys.read_angle(gy)
		#Analsys  Sensors.read_accurate_angle()
		distance = Analsys.read_distance(us)
		print (str(distance), '/n')
		time.sleep(0.5)
		#print (str(angle), '/n')

main()
