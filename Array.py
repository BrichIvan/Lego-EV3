import numpy as np


class Field(object):
    def __init__(self, rang, i_st, j_st, i_fin, j_fin, walls):
        self.rang = rang
        self.i_st = i_st
        self.j_st = j_st
        self.i_fin = i_fin
        self.j_fin = j_fin
        self.field = np.zeros((self.rang, self.rang), dtype=int)
        self.route = []
        for i in range(self.rang):
            for j in range(self.rang):
                self.field[i][j] = -2
        self.field[self.i_st, self.j_st] = 1
        self.field[self.i_fin, self.j_fin] = -1
        for p in walls:
            self.field[p[0]][p[1]] = 0
        self.direct = 0
        self.com = ''
#                               направления: 0 - вниз, 1 - вправо, 2 - вверх, 3 - влево

    def build_map(self):
        k = 1
        fl = 1
        while fl:
            for i in range(self.rang):
                for j in range(self.rang):
                    if self.field[i, j] == k:
                        if i > 0:
                            if (self.field[i - 1, j] == -2) or ((self.field[i - 1, j] > 0) and (self.field[i - 1, j] > self.field[i, j])):
                                self.field[i - 1, j] = self.field[i, j] + 1
                            if self.field[i - 1, j] == -1:
                                fl = 0
                        if i < self.rang - 1:
                            if (self.field[i + 1, j] == -2) or ((self.field[i + 1, j] > 0) and (self.field[i + 1, j] > self.field[i, j])):
                                self.field[i + 1, j] = self.field[i, j] + 1
                            if self.field[i + 1, j] == -1:
                                fl = 0
                        if j > 0:
                            if (self.field[i, j - 1] == -2) or ((self.field[i, j - 1] > 0) and (self.field[i, j - 1] > self.field[i, j])):
                                self.field[i, j - 1] = self.field[i, j] + 1
                            if self.field[i, j - 1] == -1:
                                fl = 0
                        if j < self.rang - 1:
                            if (self.field[i, j + 1] == -2) or ((self.field[i, j + 1] > 0) and (self.field[i, j + 1] > self.field[i, j])):
                                self.field[i, j + 1] = self.field[i, j] + 1
                            if self.field[i, j + 1] == -1:
                                fl = 0
            k += 1

    def find_route(self):
        i_cur = self.i_fin
        j_cur = self.j_fin
        self.route.append([i_cur, j_cur])
        min = 0
        while min != 1:
            min = 0
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
            if j_cur < self.rang - 1:
                if ((min == 0) or (self.field[i_cur, j_cur + 1] < min)) and (self.field[i_cur, j_cur + 1] > 0):
                    min = self.field[i_cur, j_cur + 1]
                    i_min = i_cur
                    j_min = j_cur + 1
            i_cur = i_min
            j_cur = j_min

            self.route.append([i_cur, j_cur])
        self.route.reverse()

    def add_wall(self, i_wal, j_wal):
        self.field[i_wal, j_wal] = 0
        self.build_map()
        self.find_route()

    def build_route(self):
        self.com = ''

        for n in range(len(self.route) - 1):

            delta_i = self.route[n + 1][0] - self.route[n][0]
            delta_j = self.route[n + 1][1] - self.route[n][1]

            if delta_i == -1:
                rout_dir = 2
            if delta_j == 1:
                rout_dir = 1
            if delta_j == -1:
                rout_dir = 3
            if delta_i == 1:
                rout_dir = 0

            if self.direct % 2 == 0:
                if (self.direct + rout_dir) % 4 == 1:
                    self.com += '3 '
                if (self.direct + rout_dir) % 4 == 3:
                    self.com += '2 '

            if self.direct % 2 != 0:
                if (self.direct + rout_dir) % 4 == 1:
                    self.com += '2 '
                if (self.direct + rout_dir) % 4 == 3:
                    self.com += '3 '

            if (rout_dir != self.direct) and ((self.direct + rout_dir) % 2 == 0):
                self.com += '3 '
                self.com += '3 '

            self.com += '1 '
            self.direct = rout_dir
# команды 1 - вперёд, 2 - по часовой, 3 - против часовой
