'''
    Compare the edges of the images and create the connections
'''
from PIL import Image
import json 
 
images = 14
limit = 9
coord1 = [[(0,0),(0,limit)],[(0,limit),(limit,limit)],[(limit,limit),(limit,0)],[(limit,0),(0,0)]]
coord2 = [[(limit,0),(limit,limit)],[(0,0),(limit,0)],[(0,limit),(0,0)],[(limit,limit),(0,limit)]]

subfolder = "images"

dic = {}

for i in range(len(coord1)):
    ck1 = ck2 = False
    toadd = 9
    if coord1[i][0][0] == coord1[i][1][0]:
        ck1 = True
    if coord2[i][0][0] == coord2[i][1][0]:
        ck2 = True
    for j in range(1, toadd+1):
        if ck1:
            coord1[i].append((coord1[i][0][0], j))
        else:
            coord1[i].append((j, coord1[i][0][1]))
        if ck2:
            coord2[i].append((coord2[i][0][0], j))
        else:
            coord2[i].append((j, coord2[i][0][1]))
    

# creating a image object
for image1 in range(1,images+1):
    dic[image1] = {"l0":[],"l1":[],"l2":[],"l3":[]}
    img1 = Image.open(subfolder+"/"+str(image1)+".png")
    px1 = img1.load()
    for image2 in range(1,images+1):
        #if image1 == image2:
        #    continue
        img2 = Image.open(subfolder+"/"+str(image2)+".png")
        px2 = img2.load()
        for a in range(len(coord1)):
            ck = 0
            for b in range(len(coord1[a])):
                #print(str(px1[coord1[a][b]] )+ " : " + str(px2[coord2[a][b]]) )
                if px1[coord1[a][b]] == px2[coord2[a][b]]:
                    ck += 1
            if ck == len(coord1[a]) or ck == len(coord1[a])-1:
                dic[image1]["l"+str(a)].append(image2)

print(dic)
out = open("connections.json", "w")
json.dump(dic, out, indent=4)
