import paho.mqtt.client as mqtt
import time

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
def send(lego):
    rang = 8
    i_st1 = "1"
    j_st1 = "1"
    i_fin1 = "4"
    j_fin1 = "4"
    dir_1 = "1"

    i_st2 = "6"
    j_st2 = "1"
    i_fin2 = "6"
    j_fin2 = "2"
    dir_2 = "1"

    walls = [[2, 1], [2, 2], [5, 3], [4, 6]]
    for i in range(rang):
        walls.append([i, 0])
        walls.append([i, rang-1])
    for j in range(rang):
        walls.append([0, j])
        walls.append([rang-1, j])
    cubes = [[1, 5], [2, 3], [5, 2], [5, 4]]
    a = str(rang)+";"+i_st1+";"+j_st1+";"+i_fin1+";"+j_fin1+";"+dir_1+";"+i_st2+";"+j_st2+";"+i_fin2+";"+j_fin2+";"+dir_2+";"+str(walls)+";"+str(cubes)
    lego.publish("Map/", a, 2)

def mqtt_init():
    global pub_topic, sub_topic, lego

    connstat = "0"
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
    lego.publish("ConnStat/", "Viz", 2)
    del(connstat)

lego_id = 0
#server_ip = ("192.168.43.152")
server_ip = ("10.42.0.1")

def main():
    # hardware and mqtt initialization
    mqtt_init()
    time.sleep(1)
    print('Ready')
    send(lego)
    lego.loop_start()
    while 1:
        k = input("Which map to show? ")
        lego.publish("Show/", k, 2)
    #Transmit to MQTT

main()
