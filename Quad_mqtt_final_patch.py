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

	def drive_sm (self, sm, left_motor, right_motor, gy, us):
		distance_ang = sm * -20.5
		left_motor.position_sp = distance_ang
		right_motor.position_sp = distance_ang
		left_motor.speed_sp = self.speed
		right_motor.speed_sp = self.speed

		left_motor.run_to_rel_pos()
		right_motor.run_to_rel_pos()

		while (left_motor.is_running or right_motor.is_running):
			distance = us.value()
			self.angle = gy.value()
			# a["data"] = [str(distance), str(self.angle)]
			# print (a["data"][0] + ' ' + a["data"][1])
			pass

	def rotate_angle (self, angle, left_motor, right_motor, gy, us):
		k = 0.035
		angle = angle + self.angle
		if (self.angle > angle):
			left_motor.speed_sp = self.speed_ang
			right_motor.speed_sp = -1 * self.speed_ang
			left_motor.run_forever()
			right_motor.run_forever()

			while (gy.value() >= (angle + k*self.speed_ang)):
				distance = us.value()
				self.angle = gy.value()
				# a["data"] = [str(distance), str(self.angle)]
				# print (a["data"][0] + ' ' + a["data"][1])
				pass
		else:
			left_motor.speed_sp = -1 * self.speed_ang
			right_motor.speed_sp = self.speed_ang

			left_motor.run_forever()
			right_motor.run_forever()

			while (gy.value() <= (angle - k*self.speed_ang)):
				distance = us.value()
				self.angle = gy.value()
				# a["data"] = [str(distance), str(self.angle)]
				# print (a["data"][0] + ' ' + a["data"][1])
				pass

		left_motor.stop()
		right_motor.stop()

# MQTT functions and callbacks
def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected")
		userdata = str(lego_id)
	else:
		print("Connection status:", rc)

def on_message(client, userdata, msg):
	message = msg.payload.decode()
	message = list(map(int, message.split(" ")))
	userdata["command"] = str(message[0])
	userdata["arg"] = str(message[1])

def on_publish(client, userdata, mid):
    print("Published ID:", mid)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed ID:", mid)

def on_unsubscribe(client, userata, mid):
    print("Unsubscribed ID:", mid)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection:", rc)
    else:
        print("Disconnected")
# ---------------------------------------
def send(in_out_data, us, gy, pub_topic, lego):
	in_out_data["distance"] = str(us.value())
	in_out_data["angle"] = str(gy.value())
	data = in_out_data["distance"] + " " + in_out_data["angle"]
	lego.publish(pub_topic, data, 0)

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
server_ip = ("192.168.43.152")
in_out_data = {"command": "0", "arg": "0", "distance": " ", "angle": " "}

def main():
	# hardware initialization
	initialization()
	left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
	right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
	gy = ev3.GyroSensor(ev3.INPUT_3)
	us = ev3.UltrasonicSensor(ev3.INPUT_4)

	# MQTT initialization
	connstat = "0"
	pub_topic = "Sensors/" + str(lego_id)
	sub_topic = "Command/" + str(lego_id)
	lego = mqtt.Client()
	lego.user_data_set(connstat)
	lego.on_connect = on_connect
	lego.on_message = on_message
	lego.on_publish = on_publish
	lego.on_subscribe = on_subscribe
	lego.on_disconnect = on_disconnect
	lego.on_unsubscribe = on_unsubscribe
	lego.connect(server_ip, 1883, 60)
	while connstat == 0:
		pass
	lego.publish("ConnStat/", str(lego_id), 0)
	del(connstat)
	lego.user_data_set(in_out_data)
	lego.subscribe(sub_topic, 0)
	lego.loop_start()

	print('Ready')
	Machine = Robot(200, 100, 0, 0)
	#Machine.rotate_angle(-10, left_motor, right_motor, gy, us, a)
	while (1):
		# Listen to MQTT
		command = str(in_out_data["command"]) + " " + str(in_out_data["arg"])
		command = command.strip().split()
		command = list(map(int, command))

		if command[1] != 0:

			if command[0] == 0:
				x = command[1]
				#print(x)
				Machine.rotate_angle(x, left_motor, right_motor, gy, us)
				send(in_out_data, us, gy, pub_topic, lego)
				in_out_data["command"] = "0"
				in_out_data["arg"] = "0"
			else:
				y = command[1]
				#print (y)
				Machine.drive_sm(y, left_motor, right_motor, gy, us)
				send(in_out_data, us, gy, pub_topic, lego)
				in_out_data["command"] = "0"
				in_out_data["arg"] = "0"
		#Transmit to MQTT
		#send(in_out_data, us, gy, pub_topic, lego)

		time.sleep(0.2)

main()
