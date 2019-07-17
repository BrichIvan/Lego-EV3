import paho.mqtt.client as mqtt
import time

class Robot(object):
	def __init__ (self, speed, speed_ang, sm, angle):
		self.speed = speed
		self.speed_ang = speed_ang
		self.sm = sm
		self.angle = angle

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
def send(in_out_data, pub_topic, lego):
	dist = input("Print distance: ")
	angle = input("Print angle: ")
	in_out_data["distance"] = dist
	in_out_data["angle"] = angle
	data = in_out_data["distance"] + " " + in_out_data["angle"]
	lego.publish(pub_topic, data, 2)


def mqtt_init():
	global pub_topic, sub_topic, lego

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
	lego.publish("ConnStat/", str(lego_id), 2)
	del(connstat)
	lego.user_data_set(in_out_data)
	lego.subscribe(sub_topic, 2)
	lego.loop_start()

lego_id = 2
#server_ip = ("192.168.43.152")
server_ip = ("10.42.0.1")
in_out_data = {"command": "0", "arg": "0", "distance": " ", "angle": " "}

def main():
	# hardware and mqtt initialization
	mqtt_init()
	print('Ready')

	Machine = Robot(200, 100, 0, 0)
	while (1):
		# Listen to MQTT
		command = str(in_out_data["command"]) + " " + str(in_out_data["arg"])
		command = command.strip().split()
		command = list(map(int, command))

		if command[1] != 0:

			if command[0] == 0:
				x = command[1]
				print(x)
				send(in_out_data, pub_topic, lego)
				in_out_data["command"] = "0"
				in_out_data["arg"] = "0"
			else:
				y = command[1]
				print (y)
				send(in_out_data, pub_topic, lego)
				in_out_data["command"] = "0"
				in_out_data["arg"] = "0"

		time.sleep(2)

		#Transmit to MQTT

main()
