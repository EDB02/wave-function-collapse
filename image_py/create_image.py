'''
    take as input an integer N and a matrix NxN with '|' as separator.
    create an image from that matrix
'''
from PIL import Image

def openImage(name):
    img = Image.open("circuit/"+str(name)+".png")
    return img

size = int(input())

imgS = 11
images = 14

ris = Image.new("RGB", (size*imgS, size*imgS))

imgs = []

for i in range(1,images+1):
    imgs.append(openImage(i))

for i in range(size):
    line = input().split("|")
    for j in range(size):
        ris.paste(imgs[int(line[j])-1], (j*imgS, i*imgS-1))

ris.show()
