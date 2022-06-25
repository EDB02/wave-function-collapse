'''
    A very slow wave function collapse algorithm
'''
import json
import random
from time import sleep
from PIL import Image

rn = 0
size = 4
imgS = 11
dic = json.load(open("connections.json", "r"))
images = 14
matrix = []
done = []
sksk = {}

def openImage(name):
    img = Image.open("circuit/"+str(name)+".png")
    return img

def Init():
    global done
    global matrix
    done = []
    matrix = []
    done = [[False for _ in range(size)] for _ in range(size)]
    for i in range(size):
        matrix.append([])
        for j in range(size):
            matrix[i].append([])
            for k in range(1,images+1):
                matrix[i][j].append(k)

def getMin():
    mins = []
    mino = 2e9
    for i in range(size):
        for j in range(size):
            if len(matrix[i][j]) == mino:
                mins.append((i,j))
            elif not done[i][j] and len(matrix[i][j]) < mino:
                mino = len(matrix[i][j])
                mins = [(i,j)]
    return (random.choice(mins), mino)

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def update(x, y):
    l0 = []
    l1 = []
    l2 = []
    l3 = []
    for i in matrix[x][y]:
        l0 = list(set(dic[str(i)]["l0"]) | set(l0))
        l1 = list(set(dic[str(i)]["l1"]) | set(l1))
        l2 = list(set(dic[str(i)]["l2"]) | set(l2))
        l3 = list(set(dic[str(i)]["l3"]) | set(l3))
    dfs(x-1, y, list(set(l3)))
    dfs(x, y+1, list(set(l2)))
    dfs(x+1, y, list(set(l1)))
    dfs(x, y-1, list(set(l0)))


def dfs(x, y, vals):
    if x < 0 or x >= size or y < 0 or y >= size:# or sksk.get((x,y), False):
        return
    #sksk[x,y] = True
    ck = False
    for i in matrix[x][y]:
        if not (i in vals):
            ck = True
            matrix[x][y].remove(i)
    if ck:
        #matrix[x][y] = list(intersection(matrix[x][y], vals))
        if len(matrix[x][y]) < 1:
            global repeat
            repeat = True
        else:
            update(x, y)

def check():
    for i in range(size):
        for j in range(size):
            if len(matrix[i][j]) > 1:
                return True
    return False

def run():
    global sksk
    Init()
    while check():
        a,m = getMin()
        x,y = a
        #print(str(x)+" "+str(y)+" "+str(m))
        #print(matrix)
        #sleep(1)
        matrix[x][y] = [random.choice(matrix[x][y])]
        done[x][y] = True
        sksk = {}
        update(x,y)
        if repeat:
            return
    print("\n\n\n")
    print(matrix)
    print("\n\n\n")
    createImage()

def createImage():
    global repeat
    if repeat:
        return
    ris = Image.new("RGB", (size*imgS, size*imgS))

    imgs = []

    for i in range(1,images+1):
        imgs.append(openImage(i))

    for i in range(size):
        for j in range(size):
            ris.paste(imgs[matrix[j][i][0]-1], (i*imgS, j*imgS-1))
    global rn
    #ris.save("result/r+"+str(rn)+".png")
    ris.show()
    rn += 1
    #run()

repeat = True

speed = 0

while repeat:
    repeat = False
    speed += 1
    run()

print("speed: "+ str(speed))
#matrix[0][0] = [3]