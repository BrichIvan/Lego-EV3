#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time

class Sensors(object):
	def __init__ (self, angle, distance, angle_ac):
		self.angle = angle
		self.dictance = distance
		self.angle_ac

	def read_angle(self, angle):
		angle = gy.value()

	def read_distance(self, distance):
		distance = us.value()
'''
		#Should be called wth high frequency
	def read_accurate_angle(self, angle_ac)	#Gyro should transmit raw values or speed
		delta_millis = millis - int(round(time.time()*1000))
		#print(delta_millis)
		angle_ac = angle_ac + delta_millis * gy.value()
		millis = int(round(time.time()*1000))
'''

def initialization():
	us = UltrasonicSensor()	
	us.mode = 'US_DIST_CM'	#put the US in the dist in sm mode

	gy = GyroSensor()
	gy.mode = 'GYRO-ANG' #put the gyro into angle mode

	assert gy.connected
	assert us.connected

def main():
	initialization()
	while (true):
		Analsys = Sensors(angle, distance, 0)	#Analsys = Sensors(0, 0, 0)
		Analsys = Sensors.read_angle()
		#Analsys = Sensors.read_accurate_angle()
		Analsys = Sensors.read_distance()
		print (str(Sensors.distance), '/n')
		time.sleep(0,5)
		#print (str(angle), '/n')

main()




current_millis = int(round(time.time()*1000))
time.sleep(5)
delta_millis = current_millis - int(round(time.time()*1000))
print(delta_millis)

