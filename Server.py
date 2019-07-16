from Array import Field
import paho.mqtt.client as mqtt
import time

#  MQTT functions
def on_connect(myPC, userdata, flags, rc):
    print("Connected")


def on_message(myPC, userdata, msg):
    global ready_for_action, map1, map2, position_1, position_2, wall_send, walls
    message = msg.payload.decode()
    print("Topic:", msg.topic)
    message = list(map(int, message.split()))
    if msg.topic == "Sensors/1":
        ready_for_action["Robot1"] = 1
        userdata["dist/1"] = a[0]
        userdata["angle/1"] = a[1]
        if message[0] < 225:
            if position_1["direct"] == 0:
                i_obstacle = position_1["i"] + 1
                j_obstacle = position_1["j"]
                map1.add_wall(position_1["i"] + 1, position_1["j"], position_1["i"], position_1["j"], position_1["direct"])
                map2.add_wall(position_1["i"] + 1, position_1["j"], position_2["i"], position_2["j"], position_2["direct"])
            if position_1["direct"] == 2:
                i_obstacle = position_1["i"] - 1
                j_obstacle = position_1["j"]
                map1.add_wall(position_1["i"] - 1, position_1["j"], position_1["i"], position_1["j"], position_1["direct"])
                map2.add_wall(position_1["i"] - 1, position_1["j"], position_2["i"], position_2["j"], position_2["direct"])
            if position_1["direct"] == 1:
                i_obstacle = position_1["i"]
                j_obstacle = position_1["j"] + 1
                map1.add_wall(position_1["i"], position_1["j"] + 1, position_1["i"], position_1["j"], position_1["direct"])
                map2.add_wall(position_1["i"], position_1["j"] + 1, position_2["i"], position_2["j"], position_2["direct"])
            if position_1["direct"] == 3:
                i_obstacle = position_1["i"]
                j_obstacle = position_1["j"] - 1
                map1.add_wall(position_1["i"], position_1["j"] - 1, position_1["i"], position_1["j"], position_1["direct"])
                map2.add_wall(position_1["i"], position_1["j"] - 1, position_2["i"], position_2["j"], position_2["direct"])
            walls.append([i_obstacle, j_obstacle])
            wall_send = 1
            struct_route(map1, map2)
    if msg.topic == "Sensors/2":
        ready_for_action["Robot2"] = 1
        userdata["dist/2"] = a[0]
        userdata["angle/2"] = a[1]
        if message[0] < 225:
            if position_2["direct"] == 0:
                i_obstacle = position_2["i"] + 1
                j_obstacle = position_2["j"]
                map2.add_wall(position_2["i"] + 1, position_2["j"], position_2["i"], position_2["j"], position_2["direct"])
                map1.add_wall(position_2["i"] + 1, position_2["j"], position_1["i"], position_1["j"], position_1["direct"])
            if position_2["direct"] == 2:
                i_obstacle = position_2["i"] - 1
                j_obstacle = position_2["j"]
                map2.add_wall(position_2["i"] - 1, position_2["j"], position_2["i"], position_2["j"], position_2["direct"])
                map1.add_wall(position_2["i"] - 1, position_2["j"], position_1["i"], position_1["j"], position_1["direct"])
            if position_2["direct"] == 1:
                i_obstacle = position_2["i"]
                j_obstacle = position_2["j"] + 1
                map2.add_wall(position_2["i"], position_2["j"] + 1, position_2["i"], position_2["j"], position_2["direct"])
                map1.add_wall(position_2["i"], position_2["j"] + 1, position_1["i"], position_1["j"], position_1["direct"])
            if position_2["direct"] == 3:
                i_obstacle = position_2["i"]
                j_obstacle = position_2["j"] - 1
                map2.add_wall(position_2["i"], position_2["j"] - 1, position_2["i"], position_2["j"], position_2["direct"])
                map1.add_wall(position_2["i"], position_2["j"] - 1, position_1["i"], position_1["j"], position_1["direct"])
            walls.append([i_obstacle, j_obstacle])
            wall_send = 1
            struct_route(map1, map2)
    print(userdata)


def on_publish(myPC, userdata, mid):
    print("Publish mid: " + str(mid))


def on_subscribe(myPC, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid))


def on_disconnect(myPC, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
    else:
        print("Disconnected")


def on_unsubscribe(myPC, userata, mid):
    print("Unsubscribed: " + str(mid))


def conn_call(myPC, userdata, msg):
    global conn
    message = msg.payload.decode()
    if message == "0":
        print("F")
    if message == "1":
        conn["Robot1"] = 1
        print("Robot 1 connected")
    if message == "2":
        conn["Robot2"] = 2
        print("Robot 2 connected")
    if message == "Viz":
        conn["Viz"] = 100
        print("Vizualization connected")


def map_call(myPC, userdata, msg):
    global rang, position_1, position_2, position_end_1, position_end_2, walls, cubes, init_set
    message = msg.payload.decode()
    message = list(map(int, message.split(";")))
    rang = message[0]
    position_1["i"] = int(message[1])
    position_1["j"] = int(message[2])
    position_end_1["i"] = int(message[3])
    position_end_1["j"] = int(message[4])
    position_1["direct"] = int(message[5])
    walls1 = message[6]
    cubes1 = message[7]

    walls1 = walls1[1:len(walls1)-1]
    walls = []
    while len(walls1) > 0:
        walls1 = walls1[1:len(walls1)]
        posit = walls1.find(", ")
        int_1 = int(walls1[0:posit])
        walls1 = walls1[posit + 2:len(walls1)]
        posit = walls1.find("]")
        int_2 = int(walls1[0:posit])
        walls1 = walls1[posit + 1:len(walls1)]
        walls.append([int_1, int_2])
        posit = walls1.find(", ")
        if posit == 0:
            walls1 = walls1[posit + 2:len(walls1)]
    
    cubes1 = cubes1[1:len(cubes1)-1]
    cubes = []
    while len(cubes1) > 0:
        cubes1 = cubes1[1:len(cubes1)]
        posit = cubes1.find(", ")
        int_1 = int(cubes1[0:posit])
        cubes1 = cubes1[posit + 2:len(cubes1)]
        posit = cubes1.find("]")
        int_2 = int(cubes1[0:posit])
        cubes1 = cubes1[posit + 1:len(cubes1)]
        cubes.append([int_1, int_2])
        posit = cubes1.find(", ")
        if posit == 0:
            cubes1 = cubes1[posit + 2:len(cubes1)]
        
    init_set = 1
#  ------------------------------

def struct_route(map1, map2):
    global queue1, queue2
    queue1 = map1.com
    queue1 = list(map(str, queue1.split(",")))
    queue1.pop()
    queue1.reverse()
    queue2 = map2.com
    queue2 = list(map(str, queue2.split(",")))
    queue2.pop()
    queue2.reverse()


#  mqtt initialization
m = {}

ready_for_action = {"Robot1": 0, "Robot2": 0}
conn = {"Robot1": 0, "Robot2": 0, "Viz": 0}

#  callbacks initialization
myPC = mqtt.Client()
myPC.user_data_set(m)
myPC.on_connect = on_connect
myPC.on_message = on_message
myPC.on_publish = on_publish
myPC.on_subscribe = on_subscribe
myPC.on_disconnect = on_disconnect
myPC.on_unsubscribe = on_unsubscribe

#  connection
myPC.connect("10.42.0.1", 1883, 60)
myPC.subscribe("ConnStat/", 2)
myPC.subscribe("Map/", 2)
myPC.message_callback_add("ConnStat/", conn_call)
myPC.message_callback_add("Map/", map_call)
myPC.loop_start()

print("Waiting until connection...")
while conn["Robot1"] == 0 or conn["Robot2"] == 0 or conn["Viz"] == 0:
   pass

myPC.message_callback_remove("ConnStat/")
print("All robots connected!")

myPC.subscribe("Sensors/1", 2)
myPC.subscribe("Sensors/2", 2)

#  set matrix size. one cell is 20x20 cm
init_set = 0
rang = 4  # 200x200 cm
#  set starting point and direction
position_1 = {"i": 0, "j": 0, "direct": 0}
position_2 = {"i": 0, "j": 0, "direct": 0}
#  set end points
position_end_1 = {"i": 2, "j": 2}
position_end_2 = {"i": 0, "j": 1}
#  set known walls and cubes
walls = []
cubes = []
wall_send = 0

while init_set == 0:
   pass

print("Vizualization imported")
ready_for_action["Robot1"] = 1
ready_for_action["Robot2"] = 1

#  initial route sending
map1 = Field(rang, position_1["i"], position_1["j"], position_end_1["i"], position_end_1["j"], position_1["direct"], walls, cubes)
map1.build_map()
map1.find_route()
map1.build_route()
map2 = Field(rang, position_2["i"], position_2["j"], position_end_2["i"], position_end_2["j"], position_2["direct"], walls, cubes)
map2.build_map()
map2.find_route()
map2.build_route()
struct_route(map1, map2)

print(map1.field)
print()
print(map1.route)
print()
print(queue1)
print()

#  main cycle
while True:

    if ready_for_action["Robot1"] == 1:
        if len(queue1) > 0:
            ready_for_action["Robot1"] = 0
            k = queue1.pop()
            if k == "1 20" and position_1["direct"] == 0:
                position_1["i"] += 1
            elif k == "1 20" and position_1["direct"] == 2:
                position_1["i"] += -1
            elif k == "1 20" and position_1["direct"] == 1:
                position_1["j"] += 1
            elif k == "1 20" and position_1["direct"] == 3:
                position_1["i"] += -1
            elif k == "0 90":
                if position_1["direct"] == 0:
                    position_1["direct"] = 3
                else:
                    position_1["direct"] += -1
            elif k == "0 -90":
                if position_1["direct"] == 3:
                    position_1["direct"] = 0
                else:
                    position_1["direct"] += 1
            myPC.publish("Command/1", k, 2)
            myPC.publish("Position/1", str(position_1["i"]) + " " + str(position_1["j"]), 2)

    if ready_for_action["Robot2"] == 1:
        if len(queue2) > 0:
            ready_for_action["Robot2"] = 0
            k = queue2.pop()
            if k == "1 20" and position_2["direct"] == 0:
                position_2["i"] += 1
            elif k == "1 20" and position_2["direct"] == 2:
                position_2["i"] += -1
            elif k == "1 20" and position_2["direct"] == 1:
                position_2["j"] += 1
            elif k == "1 20" and position_2["direct"] == 3:
                position_2["i"] += -1
            elif k == "0 90":
                if position_2["direct"] == 0:
                    position_2["direct"] = 3
                else:
                    position_2["direct"] += -1
            elif k == "0 -90":
                if position_2["direct"] == 3:
                    position_2["direct"] = 0
                else:
                    position_2["direct"] += 1
            myPC.publish("Command/2", k, 2)
            myPC.publish("Position/2", str(position_2["i"]) + " " + str(position_2["j"]), 2)

    if wall_send == 1:
        wall_send = 0
        k = str(walls[len(walls)-1][0]) + " " + str(walls[len(walls)-1][1])
        myPC.publish("Walls/", k, 2)
