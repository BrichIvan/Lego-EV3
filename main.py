from Array import route
from Array import field

#print(field)


#print(route[12][0])

number = len(route)
robo_dir = 0
                            #направления: 0 - вниз, 1 - вправо, 2 - вверх, 3 - вниз
for n in range(number-1):
    '''i_n = route[n][0]
    j_n = route[n][1]'''
    delta_i = route[n+1][0] - route[n][0]
    delta_j = route[n+1][1] - route[n][1]

    if delta_i == -1:
        rout_dir = 2
    if delta_j == 1:
        rout_dir = 1
    if delta_j == -1:
        rout_dir = 3
    if delta_i == 1:
        rout_dir = 0

    if robo_dir % 2 == 0:
        if (robo_dir + rout_dir) % 4 == 1:
            print('поворот против часовой стрелки')
        if (robo_dir + rout_dir) % 4 == 3:
            print('поворот по часовой')
    else:
        if (robo_dir + rout_dir) % 4 == 1:
            print('поворот по часовой')
        if (robo_dir + rout_dir) % 4 == 3:
            print('поворот против часовой стрелки')
    print('езда вперёд')
    robo_dir = rout_dir