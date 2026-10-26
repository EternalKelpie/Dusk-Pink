import random

WALL = 1
ROOM = 0
LOOT = 2
ENC = 3 # encounter

def GenerateRooms(width = 40, height= 30, roomNumber=6, seed = None, isLoot = False, isEnc = False):
    map = [[WALL for i in range(40)] for j in range(30)]       # 1 is wall, 0 will be room and corridors
    roomsCenter = []
    random.seed(seed)
    readyRooms =0
    attempts = 0
    while(readyRooms< roomNumber and attempts < roomNumber + 5):
        roomPlacementX = random.randint(1, 23)
        roomPlacementY = random.randint(1, 23)
        roomDimension = random.randint(3, 5)
        attempts= attempts + 1
        if (map[roomPlacementY - 1][roomPlacementX - 1] != ROOM and map[roomPlacementY + roomDimension + 1][roomPlacementX - 1] != ROOM and map[roomPlacementY - 1][roomPlacementX + roomDimension + 1] != ROOM   and map[roomPlacementY + roomDimension + 1][roomPlacementX + roomDimension + 1] != ROOM and map[roomPlacementY + roomDimension//2][roomPlacementX + roomDimension//2] != ROOM):
            i =0
            while i<roomDimension:
                j =0
                while j<roomDimension:
                    map[roomPlacementY +i ][roomPlacementX +j] = 0
                    j= j+1
                i= i+1
            center = ( roomPlacementX + roomDimension // 2, roomPlacementY + roomDimension // 2)
            roomsCenter.append(center)
            readyRooms = readyRooms + 1

    i = 0
    while i < len(roomsCenter) - 1:
        firstCen = roomsCenter[i]
        secondCen = roomsCenter[i + 1]

        x1, y1 = firstCen
        x2, y2 = secondCen


        while x1 != x2:
            map[y1][x1] = 0

            if x1 < x2:
                x1 += 1
            else:
                x1 -= 1

        while y1 != y2:
            map[y1][x1] = 0

            if y1 < y2:
                y1 += 1
            else:
                y1 -= 1

        map[y2][x2] = 1

        i += 1
    if(isLoot== True):
        for x in range(len(roomsCenter)):
            chance= random.randint(1, 100)
            if(chance >65):
                paramX= random.randint(-2,2)
                paramY = random.randint(-2, 2)
                place = roomsCenter[x]
                if map[place[1] + paramX][place[0] + paramY] == 0:
                    map[place[1] + paramX] [place[0] + paramY] = 2
    if(isEnc==True):
        for x in range(len(roomsCenter)):
            chance= random.randint(1, 100)
            if(chance >55):
                paramX= random.randint(-2,2)
                paramY = random.randint(-2, 2)
                place = roomsCenter[x]
                if map[place[1] + paramY][place[0] + paramX] == 0:
                   map[place[1] + paramY] [place[0] + paramX] = 3 



    return map

#a = GenerateRooms(42)
#for row in a:
#    print("".join("#" if cell == WALL else "o" for cell in row))
#    print()
