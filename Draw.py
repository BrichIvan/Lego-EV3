from tkinter import *
from Array import Field
import paho.mqtt.client as mqtt

def on_connect(myPC, userdata, flags, rc):
    print("Connected")

def on_message(myPC, userdata, msg):
    global i_cur_1, j_cur_1, i_cur_2, j_cur_2, i_obstacle, j_obstacle
    message = msg.payload.decode()
    message = list(map(int, message.split(" ")))
    print("Topic:", msg.topic)
    if msg.topic == "Position/1":
        i_cur_1 = message[0]
        j_cur_1 = message[1]
    if msg.topic == "Position/2":
        i_cur_2 = message[0]
        j_cur_2 = message[1]
    if msg.topic == "Walls/":
        i_obstacle = message[0]
        j_obstacle = message[1]
    map_obj = Mapping()
    map_obj.add_obstacle(i_obstacle, j_obstacle)
    map_obj.add_current1(i_cur_1, j_cur_1)
    map_obj.add_current2(i_cur_2, j_cur_2)

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

myPC = mqtt.Client()
myPC.on_connect = on_connect
myPC.on_message = on_message
myPC.on_publish = on_publish
myPC.on_subscribe = on_subscribe
myPC.on_disconnect = on_disconnect
myPC.on_unsubscribe = on_unsubscribe

#  connection
myPC.connect("192.168.43.152", 1883, 60)
myPC.loop_start()
myPC.subscribe("Position/1", 2)
myPC.subscribe("Position/2", 2)
myPC.subscribe("Walls/", 2)


root = Tk()
root2 = Tk()
root3 = Tk()
root.bind("<Escape>", exit)
root2.bind("<Escape>", exit)
root3.bind("<Escape>", exit)


def exit():
    root.destroy()

global map1, map2
vizited1 = []
vizited2 = []
cubes = []
wols = []
wols.append([2, 1])
wols.append([3, 1])
wols.append([5, 3])
wols.append([3, 0])
wols.append([4, 3])
wols.append([2, 4])
wols.append([2, 5])
wols.append([2, 3])
wols.append([1, 6])
wols.append([3, 7])

#map1 = Field()

class Mapping(object):
    def __init__(self):
        self.but_put = Button(text='Upload', width=10, height=3)
        self.but_put.bind('<Button-1>', self.upload)
        self.but_put.grid(row=1, column=2)

        self.but_build_map = Button(root, text='build_map', width=10, height=3, command=lambda: self.build_map())
        self.but_build_map.grid(row=2, column=2)

        self.lb1 = Label(text="Введите ранг: ")
        self.lb1.grid(row=1, column=0, sticky=W)
        self.en1 = Entry()
        self.en1.grid(row=1, column=1)

        self.k = 0
        self.st = 0
        self.fn = 0

    def add_start(self, i1, j1):
        print("okay")
        self.b1[i1][j1]['bg'] = "green"
        if self.st == 0:
            self.b1[i1][j1]['text'] = "1 start"
            self.i_st1 = i1
            self.j_st1 = j1
        else:
            self.b1[i1][j1]['text'] = "2 start"
            self.i_st2 = i1
            self.j_st2 = j1
        self.but_add_start.destroy()
        self.but_add_finish.destroy()

        self.st += 1

    def add_finish(self, i1, j1):
        self.b1[i1][j1]['bg'] = "orange"
        if self.fn == 0:
            self.b1[i1][j1]['text'] = "1 finish"
            self.i_fin1 = i1
            self.j_fin1 = j1
        else:
            self.b1[i1][j1]['text'] = "2 finish"
            self.i_fin2 = i1
            self.j_fin2 = j1
        self.but_add_start.destroy()
        self.but_add_finish.destroy()
        self.fn += 1

    def Choose(self, i1, j1):
        if self.st < 2:
            self.but_add_start = Button(root3, text='Отметить СТАРТ',
                                        command=lambda i1=i1, j1=j1: self.add_start(i1, j1))
            self.but_add_start.pack()

        if self.fn < 2:
            self.but_add_finish = Button(root3, text='Отметить ЦЕЛЬ',
                                         command=lambda i1=i1, j1=j1: self.add_finish(i1, j1))
            self.but_add_finish.pack()


    def add_obstacle(self, i_obstacle, j_obstacle):
        #self.b1[wols[n][0]][wols[n][1]]['bg'] = "red"
        wols.append([i_obstacle, j_obstacle])
        self.build_map

    def add_current1(self, i_cur_1, j_cur_1):
        tr = self.en1.get()
        r = int(tr)
        for i in range(r):
            for j in range(r):
                if self.map1.field[i][j] == 1:
                    self.map1.field[i][j] = -2
                    vizited1.append(i, j)
        self.map1.field[i_cur_1][j_cur_1] = 1
        self.b1[i_cur_1][j_cur_1] = Button(root2, bg='#F08080')
        self.build_map

    def add_current2(self, i_cur_2, j_cur_2):
        tr = self.en1.get()
        r = int(tr)
        for i in range(r):
            for j in range(r):
                if self.map2.field[i][j] == 1:
                    self.map2.field[i][j] = -2
                    vizited2.append(i, j)
        self.map2.field[i_cur_2][j_cur_2] = 1
        self.b1[i_cur_2][j_cur_2] = Button(root2, bg='#FF69B4')
        self.build_map


    def build_map(self):
        self.but_build_map['fg'] = "red"
        tr = self.en1.get()
        r = int(tr)
        map1 = Field(r, self.i_st1, self.j_st1, self.i_fin1, self.j_fin1, 0, wols, cubes)
        map2 = Field(r, self.i_st2, self.j_st2, self.i_fin2, self.j_fin2, 0, wols, cubes)
        a = str(r)+";"+str(self.i_st1)+";"+str(self.j_st1)+";"+str(self.i_fin1)+";"+str(self.j_fin1)+";"+str(0)+";" + str(self.i_st2) + ";" + str(self.j_st2) + ";" + str(self.i_fin2) + ";" + str(self.j_fin2) + ";" + str(0)+";"+str(wols)+";"+str(cubes)

        map1.build_map()
        map1.find_route()
        map1.build_route()

        print(map1.route)
        print(map1.field)
        print(map1.com)

        for n in range(1, len(map1.route) - 1):
            self.b1[map1.route[n][0]][map1.route[n][1]]['bg'] = "lime"

        map2.ano.extend(map1.route)
        map2.build_map()
        map2.find_route()
        map2.build_route()

        print(map2.ano)
        print(map2.route)
        print(map2.field)
        print(map2.com)

        for n in range(1, len(map2.route) - 1):
            self.b1[map2.route[n][0]][map2.route[n][1]]['bg'] = "olive"

        for n in range(len(wols)):
            self.b1[wols[n][0]][wols[n][1]]['bg'] = "red"

        for n in range(len(vizited1)):
            self.b1[vizited1[n][0]][vizited1[n][1]]['bg'] = '#CD853F'
        for n in range(len(vizited2)):
            self.b1[vizited2[n][0]][vizited2[n][1]]['bg'] = "grey"


    def upload(self, event):
        self.but_put['fg'] = "red"
        self.but_put['activeforeground'] = "blue"
        self.but_put['text'] = "Done"

        tr = self.en1.get()
        r = int(tr)
        self.b1 = [[0 for i in range(r)] for j in range(r)]
        for i in range(r):
            for j in range(r):
                self.b1[i][j] = Button(root2, bg="yellow", width=4, height=4, command=lambda i1=i, j1=j: self.Choose(i1, j1))
                self.b1[i][j].grid(column=j, row=i)

        for n in range(len(wols)):
            self.b1[wols[n][0]][wols[n][1]]['bg'] = "red"




mainmenu = Menu(root)
root.config(menu=mainmenu)

filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Открыть...")
filemenu.add_command(label="Новый")
filemenu.add_command(label="Сохранить...")
filemenu.add_command(label="Выход")

helpmenu = Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="О программе")

mainmenu.add_cascade(label="Файл", menu=filemenu)






Mapping()
root.mainloop()
root2.mainloop()

