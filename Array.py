import numpy as np

rang = 6
#rang = int(input())
field = np.zeros((rang, rang), dtype=int)
for i in range(rang):
    for j in range(rang):
        field[i][j] += -2

route = []
i_st = 0
j_st = 0
i_fin = 5
j_fin = 5


field[i_st, j_st] = 1             #начало
field[i_fin, j_fin] = -1            #конец

field[2, 1] = 0
field[3, 1] = 0
field[2, 2] = 0
field[5, 3] = 0
field[4, 3] = 0
field[2, 4] = 0
field[2, 5] = 0
field[2, 3] = 0             #стенки


k = 1
fl = 1
while (fl):
    for i in range(rang):
        for j in range(rang):
            if field[i, j] == k:
                if i > 0:
                    if (field[i - 1, j] == -2) or ((field[i - 1, j] > 0) and (field[i - 1, j] > field[i, j])):
                        field[i - 1, j] = field[i, j] + 1
                    if field[i - 1, j] == -1:
                        fl = 0
                if i < rang - 1:
                    if (field[i + 1, j] == -2) or ((field[i + 1, j] > 0) and (field[i + 1, j] > field[i, j])):
                        field[i + 1, j] = field[i, j] + 1
                    if field[i + 1, j] == -1:
                        fl = 0
                if j > 0:
                    if (field[i, j - 1] == -2) or ((field[i, j - 1] > 0) and (field[i, j - 1] > field[i, j])):
                        field[i, j - 1] = field[i, j] + 1
                    if field[i, j - 1] == -1:
                        fl = 0
                if j < rang - 1:
                    if (field[i, j + 1] == -2) or ((field[i, j + 1] > 0) and (field[i, j + 1] > field[i, j])):
                        field[i, j + 1] = field[i, j] + 1
                    if field[i, j + 1] == -1:
                        fl = 0
    k += 1


#print(field)

'''field[1, 4] = -1'''

fl = 1
i_cur = i_fin
j_cur = j_fin
route.append([i_cur, j_cur])
while k > 1:
    min = 0
    if i_cur > 0:
        if ((min == 0) or (field[i_cur - 1, j_cur] < min)) and (field[i_cur - 1, j_cur] > 0):
            min = field[i_cur - 1, j_cur]
            i_min = i_cur - 1
            j_min = j_cur
    if i_cur < rang - 1:
        if ((min == 0)  or (field[i_cur + 1, j_cur] < min)) and (field[i_cur + 1, j_cur] > 0):
            min = field[i_cur + 1, j_cur]
            i_min = i_cur + 1
            j_min = j_cur
    if j_cur > 0:
        if ((min == 0) or (field[i_cur, j_cur - 1] < min)) and (field[i_cur, j_cur - 1] > 0):
            min = field[i_cur, j_cur - 1]
            i_min = i_cur
            j_min = j_cur - 1
    if j_cur < rang - 1:
        if ((min == 0) or (field[i_cur, j_cur + 1] < min)) and (field[i_cur, j_cur + 1] > 0):
            min = field[i_cur, j_cur + 1]
            i_min = i_cur
            j_min = j_cur + 1
    i_cur = i_min
    j_cur = j_min
    k -= 1
    route.append([i_cur, j_cur])
route.reverse()
print(field)
print(route)
