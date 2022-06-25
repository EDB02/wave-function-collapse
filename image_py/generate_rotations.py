'''
    Take a list of images and create all rotations
'''
from PIL import Image

images = ["1.png", "2.png", "3.png", "4.png"]

c = 5
for image in images:
    img = Image.open(r"circuit/"+image)
    for i in range(3):
        img = img.rotate(90)
        img.save("circuit/"+str(c)+".png")
        c+=1