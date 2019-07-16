import numpy as np


class Field(object):
    def __init__(self, rang, i_st, j_st, i_fin, j_fin, direct, walls, cubes):
        self.rang = rang
        self.i_st = i_st
        self.j_st = j_st
        self.i_fin = i_fin
        self.j_fin = j_fin
        self.field = np.zeros((self.rang, self.rang), dtype=int)
        self.route = []
        self.ano = []
        for i in range(self.rang):
            for j in range(self.rang):
                self.field[i][j] = -2
        self.field[self.i_st, self.j_st] = 1
        self.field[self.i_fin, self.j_fin] = -1
        for i in walls:
            self.field[i[0]][i[1]] = 0
        for i in cubes:
            self.field[i[0]][i[1]] = -3
        self.direct = direct
        self.com = ''
        self.turns_after_calibration = 0
        self.min_turns_for_calibration = 3

    #  направления: 0 - вниз, 1 - вправо, 2 - вверх, 3 - влево

    def build_map(self):
        k = 1
        fl = 0
        for i in range(self.rang):
            for j in range(self.rang):
                if self.field[i][j] > 1:
                    self.field[i][j] = -2
        for i in range(self.rang):
            for j in range(self.rang):
            	if self.field[i][j] == -1:
            		fl = 1
        while fl:
            for i in range(self.rang):
                for j in range(self.rang):
                    if self.field[i, j] == k:
                        if i > 0:
                            if (self.field[i - 1, j] == -2) or (
                                    (self.field[i - 1, j] > 0) and (self.field[i - 1, j] > self.field[i, j])):
                                if [i - 1, j] in self.ano:
                                    self.field[i - 1, j] = self.field[i, j] + 3
                                else:
                                	self.field[i - 1, j] = self.field[i, j] + 1
                            if self.field[i - 1, j] == -1:
                                fl = 0
                        if i < self.rang - 1:
                            if (self.field[i + 1, j] == -2) or (
                                    (self.field[i + 1, j] > 0) and (self.field[i + 1, j] > self.field[i, j])):
                                if [i + 1, j] in self.ano:
                                    self.field[i + 1, j] = self.field[i, j] + 3
                                else:
                                	self.field[i + 1, j] = self.field[i, j] + 1
                            if self.field[i + 1, j] == -1:
                                fl = 0
                        if j > 0:
                            if (self.field[i, j - 1] == -2) or (
                                    (self.field[i, j - 1] > 0) and (self.field[i, j - 1] > self.field[i, j])):
                                if [i, j - 1] in self.ano:
                                    self.field[i, j - 1] = self.field[i, j] + 3
                                else:
                                	self.field[i, j - 1] = self.field[i, j] + 1
                            if self.field[i, j - 1] == -1:
                                fl = 0
                        if j < self.rang - 1:
                            if (self.field[i, j + 1] == -2) or (
                                    (self.field[i, j + 1] > 0) and (self.field[i, j + 1] > self.field[i, j])):
                                if [i, j + 1] in self.ano:
                                    self.field[i, j + 1] = self.field[i, j] + 3
                                else:
                                	self.field[i, j + 1] = self.field[i, j] + 1
                            if self.field[i, j + 1] == -1:
                                fl = 0
            k += 1

    def find_route(self):
        i_cur = self.i_fin
        j_cur = self.j_fin
        self.route = []
        direct = (self.direct + 2) % 4
        min = 1
        for i in range(self.rang):
            for j in range(self.rang):
            	if self.field[i][j] == -1:
            		min = 0
            		self.route.append([i_cur, j_cur])
        while min != 1:
            min = 0

            if direct == 0:
                if i_cur > 0:
                    if ((min == 0) or (self.field[i_cur - 1, j_cur] < min)) and (self.field[i_cur - 1, j_cur] > 0):
                        min = self.field[i_cur - 1, j_cur]
                        i_min = i_cur - 1
                        j_min = j_cur
                if j_cur > 0:
                    if ((min == 0) or (self.field[i_cur, j_cur - 1] < min)) and (self.field[i_cur, j_cur - 1] > 0):
                        min = self.field[i_cur, j_cur - 1]
                        i_min = i_cur
                        j_min = j_cur - 1
                if j_cur < self.rang - 1:
                    if ((min == 0) or (self.field[i_cur, j_cur + 1] < min)) and (self.field[i_cur, j_cur + 1] > 0):
                        min = self.field[i_cur, j_cur + 1]
                        i_min = i_cur
                        j_min = j_cur + 1
                if i_cur < self.rang - 1:
                    if ((min == 0) or (self.field[i_cur + 1, j_cur] < min)) and (self.field[i_cur + 1, j_cur] > 0):
                        min = self.field[i_cur + 1, j_cur]
                        i_min = i_cur + 1
                        j_min = j_cur

            elif direct == 1:
                if j_cur > 0:
                    if ((min == 0) or (self.field[i_cur, j_cur - 1] < min)) and (self.field[i_cur, j_cur - 1] > 0):
                        min = self.field[i_cur, j_cur - 1]
                        i_min = i_cur
                        j_min = j_cur - 1
                if i_cur > 0:
                    if ((min == 0) or (self.field[i_cur - 1, j_cur] < min)) and (self.field[i_cur - 1, j_cur] > 0):
                        min = self.field[i_cur - 1, j_cur]
                        i_min = i_cur - 1
                        j_min = j_cur
                if i_cur < self.rang - 1:
                    if ((min == 0) or (self.field[i_cur + 1, j_cur] < min)) and (self.field[i_cur + 1, j_cur] > 0):
                        min = self.field[i_cur + 1, j_cur]
                        i_min = i_cur + 1
                        j_min = j_cur
                if j_cur < self.rang - 1:
                    if ((min == 0) or (self.field[i_cur, j_cur + 1] < min)) and (self.field[i_cur, j_cur + 1] > 0):
                        min = self.field[i_cur, j_cur + 1]
                        i_min = i_cur
                        j_min = j_cur + 1

            elif direct == 2:
                if i_cur < self.rang - 1:
                    if ((min == 0) or (self.field[i_cur + 1, j_cur] < min)) and (self.field[i_cur + 1, j_cur] > 0):
                        min = self.field[i_cur + 1, j_cur]
                        i_min = i_cur + 1
                        j_min = j_cur
                if j_cur > 0:
                    if ((min == 0) or (self.field[i_cur, j_cur - 1] < min)) and (self.field[i_cur, j_cur - 1] > 0):
                        min = self.field[i_cur, j_cur - 1]
                        i_min = i_cur
                        j_min = j_cur - 1
                if j_cur < self.rang - 1:
                    if ((min == 0) or (self.field[i_cur, j_cur + 1] < min)) and (self.field[i_cur, j_cur + 1] > 0):
                        min = self.field[i_cur, j_cur + 1]
                        i_min = i_cur
                        j_min = j_cur + 1
                if i_cur > 0:
                    if ((min == 0) or (self.field[i_cur - 1, j_cur] < min)) and (self.field[i_cur - 1, j_cur] > 0):
                        min = self.field[i_cur - 1, j_cur]
                        i_min = i_cur - 1
                        j_min = j_cur

            elif direct == 3:
                if j_cur < self.rang - 1:
                    if ((min == 0) or (self.field[i_cur, j_cur + 1] < min)) and (self.field[i_cur, j_cur + 1] > 0):
                        min = self.field[i_cur, j_cur + 1]
                        i_min = i_cur
                        j_min = j_cur + 1
                if i_cur > 0:
                    if ((min == 0) or (self.field[i_cur - 1, j_cur] < min)) and (self.field[i_cur - 1, j_cur] > 0):
                        min = self.field[i_cur - 1, j_cur]
                        i_min = i_cur - 1
                        j_min = j_cur
                if i_cur < self.rang - 1:
                    if ((min == 0) or (self.field[i_cur + 1, j_cur] < min)) and (self.field[i_cur + 1, j_cur] > 0):
                        min = self.field[i_cur + 1, j_cur]
                        i_min = i_cur + 1
                        j_min = j_cur
                if j_cur > 0:
                    if ((min == 0) or (self.field[i_cur, j_cur - 1] < min)) and (self.field[i_cur, j_cur - 1] > 0):
                        min = self.field[i_cur, j_cur - 1]
                        i_min = i_cur
                        j_min = j_cur - 1

            i_cur = i_min
            j_cur = j_min

            self.route.append([i_cur, j_cur])

            delta_i = self.route[len(self.route)-2][0] - self.route[len(self.route)-1][0]
            delta_j = self.route[len(self.route)-2][1] - self.route[len(self.route)-1][1]

            if delta_i == -1:
                direct = 2
            elif delta_j == 1:
                direct = 1
            elif delta_j == -1:
                direct = 3
            elif delta_i == 1:
                direct = 0

        self.route.reverse()

    def build_route(self):
        self.com = ''
        
        for n in range(len(self.route) - 1):

            delta_i = self.route[n + 1][0] - self.route[n][0]
            delta_j = self.route[n + 1][1] - self.route[n][1]

            if delta_i == -1:
                rout_dir = 2
            elif delta_j == 1:
                rout_dir = 1
            elif delta_j == -1:
                rout_dir = 3
            elif delta_i == 1:
                rout_dir = 0

            if self.direct % 2 == 0:
                if (self.direct + rout_dir) % 4 == 1:
                    self.com += '0 -90,'
                if (self.direct + rout_dir) % 4 == 3:
                    self.com += '0 90,'

            if self.direct % 2 != 0:
                if (self.direct + rout_dir) % 4 == 1:
                    self.com += '0 90,'
                if (self.direct + rout_dir) % 4 == 3:
                    self.com += '0 -90,'

            if (rout_dir != self.direct) and ((self.direct + rout_dir) % 2 == 0):
                self.com += '0 -90,'
                self.com += '0 -90,'

            self.com += '1 20,'
            self.direct = rout_dir

    #  команды 1 (1 20) - вперёд 20 см, 2 (0 90) - по часовой, 3 (0 -90) - против часовой

            #  check for cubes
            flaag = False
            self.turns_after_calibration += 1
            if self.turns_after_calibration > self.min_turns_for_calibration:
                self.turns_after_calibration = 0
                if self.route[n + 1][0] > 0:
                    if self.field[self.route[n + 1][0] - 1, self.route[n + 1][1]] == -3:
                        self.turns_after_calibration = 0
                        i_cube = self.route[n + 1][0] - 1
                        j_cube = self.route[n + 1][1]
                        flaag = True
                if self.route[n + 1][1] > 0:
                    if self.field[self.route[n + 1][0], self.route[n + 1][1] - 1] == -3:
                        self.turns_after_calibration = 0
                        i_cube = self.route[n + 1][0]
                        j_cube = self.route[n + 1][1] - 1
                        flaag = True
                if self.route[n + 1][1] < self.rang - 1:
                    if self.field[self.route[n + 1][0], self.route[n + 1][1] + 1] == -3:
                        self.turns_after_calibration = 0
                        i_cube = self.route[n + 1][0]
                        j_cube = self.route[n + 1][1] + 1
                        flaag = True
                if self.route[n + 1][0] < self.rang - 1:
                    if self.field[self.route[n + 1][0] + 1, self.route[n + 1][1]] == -3:
                        self.turns_after_calibration = 0
                        i_cube = self.route[n + 1][0] + 1
                        j_cube = self.route[n + 1][1]
                        flaag = True

            if flaag:
                delta_i = self.route[n + 1][0] - i_cube
                delta_j = self.route[n + 1][1] - j_cube
                if delta_i == -1:
                    cal_dir = 2
                elif delta_j == 1:
                    cal_dir = 1
                elif delta_j == -1:
                    cal_dir = 3
                elif delta_i == 1:
                    cal_dir = 0

                if self.direct % 2 == 0:
                    if (self.direct + cal_dir) % 4 == 1:
                        self.com += '0 -90,'
                    if (self.direct + cal_dir) % 4 == 3:
                        self.com += '0 90,'

                if self.direct % 2 != 0:
                    if (self.direct + cal_dir) % 4 == 1:
                        self.com += '0 90,'
                    if (self.direct + cal_dir) % 4 == 3:
                        self.com += '0 -90,'

                if (cal_dir != self.direct) and ((self.direct + cal_dir) % 2 == 0):
                    self.com += '0 -90,'
                    self.com += '0 -90,'

                self.com += '5 1,'
                self.direct = cal_dir

    #  команды 1 (1 20) - вперёд 20 см, 2 (0 90) - по часовой, 3 (0 -90) - против часовой

    def add_wall(self, i_wal, j_wal, i_cur, j_cur, direct):
        self.field[i_wal, j_wal] = 0
        for i in range(self.rang):
            for j in range(self.rang):
                if self.field[i, j] == 1:
                    self.field[i, j] = -2
        self.field[i_cur, j_cur] = 1
        self.direct = direct
        self.build_map()
        self.find_route()
        self.build_route()

    ''' #  rubbish - can be thrown away
    def smooth_route(self):
        direct = self.direct
        if direct == 0:
            delta_i_0 = 1
            delta_j_0 = 0
        if direct == 1:
            delta_j_0 = 1
            delta_i_0 = 0
        if direct == 2:
            delta_i_0 = -1
            delta_j_0 = 0
        if direct == 3:
            delta_j_0 = -1
            delta_i_0 = 0
        if len(self.route) > 3:
            for n in range(len(self.route)-2):
                delta_i_1 = self.route[n+1][0] - self.route[n][0]
                delta_j_1 = self.route[n+1][1] - self.route[n][1]
                delta_i_2 = self.route[n+2][0] - self.route[n+1][0]
                delta_j_2 = self.route[n+2][1] - self.route[n+1][1]
                if (delta_i_0 == delta_i_2 == 1) and (delta_j_1 == 1):
                    if self.field[self.route[n+1][0], self.route[n+1][1]] == self.field[self.route[n+1][0]+1, self.route[n+1][1]-1]:
                        self.route[n+1][0] = self.route[n+1][0]+1
                        self.route[n+1][1] = self.route[n+1][1]-1
                if (delta_i_0 == delta_i_2 == 1) and (delta_j_1 == -1):
                    if self.field[self.route[n+1][0], self.route[n+1][1]] == self.field[self.route[n+1][0]+1, self.route[n+1][1]+1]:
                        self.route[n+1][0] = self.route[n+1][0]+1
                        self.route[n+1][1] = self.route[n+1][1]+1
                if (delta_i_0 == delta_i_2 == -1) and (delta_j_1 == 1):
                    if self.field[self.route[n+1][0], self.route[n+1][1]] == self.field[self.route[n+1][0]-1, self.route[n+1][1]-1]:
                        self.route[n+1][0] = self.route[n+1][0]-1
                        self.route[n+1][1] = self.route[n+1][1]-1
                if (delta_i_0 == delta_i_2 == -1) and (delta_j_1 == -1):
                    if self.field[self.route[n+1][0], self.route[n+1][1]] == self.field[self.route[n+1][0]-1, self.route[n+1][1]+1]:
                        self.route[n+1][0] = self.route[n+1][0]-1
                        self.route[n+1][1] = self.route[n+1][1]+1
                if (delta_j_0 == delta_j_2 == 1) and (delta_i_1 == 1):
                    if self.field[self.route[n+1][0], self.route[n+1][1]] == self.field[self.route[n+1][0]-1, self.route[n+1][1]+1]:
                        self.route[n+1][0] = self.route[n+1][0]-1
                        self.route[n+1][1] = self.route[n+1][1]+1
                if (delta_j_0 == delta_j_2 == 1) and (delta_i_1 == -1):
                    if self.field[self.route[n+1][0], self.route[n+1][1]] == self.field[self.route[n+1][0]+1, self.route[n+1][1]+1]:
                        self.route[n+1][0] = self.route[n+1][0]+1
                        self.route[n+1][1] = self.route[n+1][1]+1
                if (delta_j_0 == delta_j_2 == -1) and (delta_i_1 == 1):
                    if self.field[self.route[n+1][0], self.route[n+1][1]] == self.field[self.route[n+1][0]-1, self.route[n+1][1]-1]:
                        self.route[n+1][0] = self.route[n+1][0]-1
                        self.route[n+1][1] = self.route[n+1][1]-1
                if (delta_j_0 == delta_j_2 == -1) and (delta_i_1 == -1):
                    if self.field[self.route[n+1][0], self.route[n+1][1]] == self.field[self.route[n+1][0]+1, self.route[n+1][1]-1]:
                        self.route[n+1][0] = self.route[n+1][0]+1
                        self.route[n+1][1] = self.route[n+1][1]-1
                delta_i_0 = self.route[n+1][0] - self.route[n][0]
                delta_j_0 = self.route[n+1][1] - self.route[n][1]
    '''