from tkinter import *
from Array_draw import Field
import paho.mqtt.client as mqtt
import time

#changes = lambda butt, col: butt.config(bg=col)

def on_connect(myPC, userdata, flags, rc):
    print("Connected")

def on_message(myPC, userdata, msg):
    global i_cur_1, j_cur_1, i_cur_2, j_cur_2, i_obstacle, j_obstacle, dir_cur_1, dir_cur_2, robot_numb

    message = msg.payload.decode()
    message = list(map(int, message.split(" ")))
    print("Topic:", msg.topic)
    if msg.topic == "Position/1":
        i_cur_1 = message[0]
        j_cur_1 = message[1]
        map_obj.dir_cur_1 = message[2]
        map_obj.add_current1(i_cur_1, j_cur_1)
    if msg.topic == "Position/2":
        i_cur_2 = message[0]
        j_cur_2 = message[1]
        map_obj.dir_cur_2 = message[2]
        map_obj.add_current2(i_cur_2, j_cur_2)
    if msg.topic == "Walls/":
        i_obstacle = message[0]
        j_obstacle = message[1]
        map_obj.add_obstacle(i_obstacle, j_obstacle)


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
myPC.publish("ConnStat/", "Viz", 2)
myPC.subscribe("Position/1", 2)
myPC.subscribe("Position/2", 2)
myPC.subscribe("Walls/", 2)
myPC.loop_start()

root = Tk()
root2 = Tk()
root3 = Tk()
root.bind("<Escape>", exit)
root2.bind("<Escape>", exit)
root3.bind("<Escape>", exit)



def exit():
    root.destroy()

#vizited1 = []
#vizited2 = []
cubes = []
#wols = []

cubes.append([4, 4])

'''wols.append([3, 2])
wols.append([4, 2])
wols.append([6, 4])
wols.append([4, 1])
wols.append([5, 4])
wols.append([3, 5])
wols.append([3, 6])
wols.append([3, 4])
wols.append([2, 7])
wols.append([4, 8])'''

#map1 = Field()

class Mapping(object):
    def __init__(self):
        self.but_put = Button(text='Upload', width=10, height=3)
        self.but_put.bind('<Button-1>', self.upload)
        self.but_put.grid(row=1, column=2)
        self.tr = ''

        self.but_build_map = Button(root, text='build_map', width=10, height=3, command=lambda: self.build_map())
        self.but_build_map.grid(row=2, column=2)

        self.but_rebuild_map = Button(root, text="UPDATE", width=10, height=3, command=lambda: self.rebuild_map())
        self.but_rebuild_map.grid(row=3, column=2)

        self.lb1 = Label(text="Введите ранг: ")
        self.lb1.grid(row=1, column=0, sticky=W)
        self.en1 = Entry()
        self.en1.grid(row=1, column=1)

        self.k = 0
        self.st = 0
        self.fn = 0

        self.i_st1 = 0
        self.j_st1 = 0
        self.i_st2 = 0
        self.j_st2 = 0

        self.i_fin1 = 0
        self.j_fin1 = 0
        self.i_fin2 = 0
        self.j_fin2 = 0

        self.dir_cur_1 = 0
        self.dir_cur_2 = 0

        self.wols = []
        #self.cubes = []

        self.vizited1 = []
        self.vizited2 = []

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


    '''def add_obstacle(self, i_obstacle, j_obstacle):
        print("NEW OBSTACLE")
        self.wols.append([i_obstacle, j_obstacle])
        print(self.wols[len(self.wols)-1])
        self.b1[i_obstacle][j_obstacle]['bg'] = "red"
        self.build_map()'''
       # self.b1[i_obstacle][j_obstacle]['bg'] = "red"
    def add_obstacle(self, i_obstacle, j_obstacle):
        print("NEW OBSTACLE")



        map1.add_wall(i_obstacle, j_obstacle, i_cur_1, j_cur_1, self.dir_cur_1)
        map2.add_wall(i_obstacle, j_obstacle, i_cur_2, j_cur_2, self.dir_cur_2)



        self.wols.append([i_obstacle, j_obstacle])

        print(self.wols[len(self.wols)-1])
        #self.b1[i_obstacle][j_obstacle]['bg'] = "red"

        #map1.build_map()
        #map1.find_route()
        #map1.build_route()

        #map2.build_map()
        #map2.find_route()
        #map2.build_route()

        print("Map1")
        print(map1.route)
        print(map1.field)
        print(map1.com)

        print("Map2")
        print(map2.route)
        print(map2.field)
        print(map2.com)
        '''
        for n in range(1, len(map1.route) - 1):
            print("LULZ1")
            self.b1[map1.route[n][0]][map1.route[n][1]]['bg'] = "lime"
            print("LULZ3")

        for n in range(len(self.wols)):
            print("LULZ2")
            self.b1[self.wols[n][0]][self.wols[n][1]]['bg'] = "red"

        for n in range(len(cubes)):
            self.b1[cubes[n][0]][cubes[n][1]]['bg'] = "black"

        for n in range(len(vizited1)):
            self.b1[vizited1[n][0]][vizited1[n][1]]['bg'] = '#CD853F'
        for n in range(len(vizited2)):
            self.b1[vizited2[n][0]][vizited2[n][1]]['bg'] = "grey"

        
        '''
        self.rebuild_map()
        #self.but_build.invoke()
        #root2.after(0, lambda: self.build_map())

    def add_current1(self, i_cur_1, j_cur_1):
        print("12345")
        #print(str(self.tr))
        r = int(self.tr)
        print("add_current1 okay")
        for i in range(r):
            for j in range(r):
                if map1.field[i][j] == 1:
                    map1.field[i][j] = -2
                    self.vizited1.append(i, j)
        map1.field[i_cur_1][j_cur_1] = 1
        self.i_st1 = i_cur_1
        self.j_st1 = j_cur_1
        self.rebuild_map
        #self.b1[i_cur_1][j_cur_1] = Button(root2, bg='#F08080')


    def add_current2(self, i_cur_2, j_cur_2):
        r = int(self.tr)
        print("add_current2 okay")
        for i in range(r):
            for j in range(r):
                if map2.field[i][j] == 1:
                    map2.field[i][j] = -2
                    self.vizited2.append(i, j)
        map2.field[i_cur_2][j_cur_2] = 1
        self.i_st2 = i_cur_2
        self.j_st2 = j_cur_2
        self.rebuild_map
        #self.b1[i_cur_2][j_cur_2] = Button(root2, bg='#FF69B4')

    def clear_m(self):
        r = int(self.tr)
        for i in range(r):
            for j in range(r):
                self.b1[i][j].config(bg="yellow")
        '''self.b1 = [[0 for i in range(r)] for j in range(r)]
        for i in range(r):
            for j in range(r):
                self.b1[i][j] = Button(root2, bg="yellow", width=4, height=4,
                                       command=lambda i1=i, j1=j: self.Choose(i1, j1))
                self.b1[i][j].grid(column=j, row=i)'''

        for n in range(len(self.wols)):
            self.b1[self.wols[n][0]][self.wols[n][1]].config(bg="red")
            #changes(self.b1[self.wols[n][0]][self.wols[n][1]], "red")

        for n in range(len(cubes)):
            self.b1[cubes[n][0]][cubes[n][1]].config(bg="black")
            #changes(self.b1[self.cubes[n][0]][self.cubes[n][1]], "black")

    def rebuild_map(self):
        self.clear_m()
        r = int(self.tr)

        map1.i_st = self.i_st1
        map1.j_st = self.j_st1
        map1.i_fin = self.i_fin1
        map1.j_fin = self.j_fin1

        map2.i_st = self.i_st2
        map2.j_st = self.j_st2
        map2.i_fin = self.i_fin2
        map2.j_fin = self.j_fin2

        print('123'+str(map1.i_st)+str(map1.j_st)+str(self.i_st1)+str(self.j_st1))

        map1.setup()
        map2.setup()

        print('123' + str(map1.i_st) + str(map1.j_st) + str(self.i_st1) + str(self.j_st1))

        map1.build_map()
        map1.find_route()
        map1.build_route()

        print(map1.route)
        print(map1.field)
        print(map1.com)

        for n in range(1, len(map1.route) - 1):
            #print("before")
            self.b1[map1.route[n][0]][map1.route[n][1]].config(bg="lime")
            #changes(self.b1[map1.route[n][0]][map1.route[n][1]], "lime")
            #print("AFTER")

        map2.ano = map1.route
        map2.build_map()
        map2.find_route()
        map2.build_route()

        print(map2.ano)
        print(map2.route)
        print(map2.field)
        print(map2.com)

        for n in range(1, len(map2.route) - 1):
            self.b1[map2.route[n][0]][map2.route[n][1]].config(bg="olive")
            #changes(self.b1[map2.route[n][0]][map2.route[n][1]], "olive")

        print(map1.field)
        print(map2.field)

        for n in range(len(self.wols)):
            #print("LULZ")
            self.b1[self.wols[n][0]][self.wols[n][1]].config(bg="red")
            #changes(self.b1[self.wols[n][0]][self.wols[n][1]], "red")

        for n in range(len(cubes)):
            self.b1[cubes[n][0]][cubes[n][1]].config(bg="black")
            #changes(self.b1[self.cubes[n][0]][self.cubes[n][1]], "black")

        for n in range(len(self.vizited1)):
            self.b1[self.vizited1[n][0]][self.vizited1[n][1]].config(bg='#CD853F')
        for n in range(len(self.vizited2)):
            self.b1[self.vizited2[n][0]][self.vizited2[n][1]].config(bg="grey")

        self.b1[map1.i_st][map1.j_st]['bg'] = "green"
        self.b1[map1.i_fin][map1.j_fin]['bg'] = "orange"
        self.b1[map2.i_st][map2.j_st]['bg'] = "green"
        self.b1[map2.i_fin][map2.j_fin]['bg'] = "orange"

    def build_map(self):
        global cubes
        self.but_build_map['fg'] = "red"

        #if self.tr == '':

        r = int(self.tr)

        map1.i_st = self.i_st1
        map1.j_st = self.j_st1
        map1.i_fin = self.i_fin1
        map1.j_fin = self.j_fin1

        map2.i_st = self.i_st2
        map2.j_st = self.j_st2
        map2.i_fin = self.i_fin2
        map2.j_fin = self.j_fin2

        #print(str(self.i_st2) + ' ' + str(self.j_st2))
        #print(str(self.i_fin2) + ' ' + str(self.j_fin2))

        map1.setup()
        map2.setup()


        a = str(r)+";"+str(self.i_st1)+";"+str(self.j_st1)+";"+str(self.i_fin1)+";"+str(self.j_fin1)+";"+str(self.dir_cur_1)+";" + str(self.i_st2) + ";" + str(self.j_st2) + ";" + str(self.i_fin2) + ";" + str(self.j_fin2) + ";" + str(self.dir_cur_2)+";"+str(self.wols)+";"+str(cubes)
        print(a)
        myPC.publish("Map/", a, 2)
        map1.build_map()
        map1.find_route()
        map1.build_route()

        '''print(map1.route)
        print(map1.field)
        print(map1.com)'''

        for n in range(1, len(map1.route) - 1):
            self.b1[map1.route[n][0]][map1.route[n][1]].config(bg="lime")

        map2.ano = map1.route
        map2.build_map()
        map2.find_route()
        map2.build_route()

        '''print(map2.ano)
        print(map2.route)
        print(map2.field)
        print(map2.com)'''

        for n in range(1, len(map2.route) - 1):
            self.b1[map2.route[n][0]][map2.route[n][1]].config(bg="olive")


        print(map1.field)
        print(map2.field)
        for n in range(len(self.wols)):
            #print("LULZ")
            self.b1[self.wols[n][0]][self.wols[n][1]].config(bg='red')

        for n in range(len(cubes)):
            self.b1[cubes[n][0]][cubes[n][1]].config(bg='black')
        '''
        for n in range(len(vizited1)):
            self.b1[vizited1[n][0]][vizited1[n][1]].config(bg='#CD853F')
        for n in range(len(vizited2)):
            self.b1[vizited2[n][0]][vizited2[n][1]].config(bg="grey")
        '''
        #self.but_build_map.destroy()
        #self.but_put.destroy()





    def upload(self, event):
        global map1, map2
        self.but_put['fg'] = "red"
        self.but_put['activeforeground'] = "blue"
        self.but_put['text'] = "Done"
        self.tr = self.en1.get()
        r = int(self.tr)

        dir_cur_1 = 0
        dir_cur_2 = 0

        map1 = Field(r, self.i_st1, self.j_st1, self.i_fin1, self.j_fin1, dir_cur_1, self.wols, cubes)
        map2 = Field(r, self.i_st2, self.j_st2, self.i_fin2, self.j_fin2, dir_cur_2, self.wols, cubes)
        map1.setup()
        map2.setup()

        self.b1 = [[0 for i in range(r)] for j in range(r)]
        for i in range(r):
            for j in range(r):
                self.b1[i][j] = Button(root2, bg="yellow", width=4, height=4, command=lambda i1=i, j1=j: self.Choose(i1, j1))
                self.b1[i][j].grid(column=j, row=i)

        for n in range(len(self.wols)):
            self.b1[self.wols[n][0]][self.wols[n][1]].config(bg="red")

        for n in range(len(cubes)):
            self.b1[cubes[n][0]][cubes[n][1]].config(bg="black")




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




global map_obj
map_obj = Mapping()

#Mapping()
root.mainloop()
root2.mainloop()  # ???
root3.mainloop()

