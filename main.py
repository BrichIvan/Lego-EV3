from Array import Field

wols = []
wols.append([2, 1])
wols.append([3, 1])
wols.append([5, 3])
wols.append([3, 0])
wols.append([4, 3])
wols.append([2, 4])
wols.append([2, 5])
wols.append([2, 3])

map1 = Field(6, 2, 0, 5, 5, wols)
map1.build_map()
map1.find_route()
map1.build_route()

print(map1.route)
print(map1.field)
print(map1.com)
