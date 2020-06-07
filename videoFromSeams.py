import os
import cv2
import numpy as np
from sc_vid import seam_carve
from sc_vid import add_seam
from sc_vid import seams_insertion2
import re
import pickle


# Number of Width pixels / vertical seams to add 
dW = 20
# Number of Height pixels / horizontal seams to add 
dH = 0

# folder where frames are
frameFolder = 'testFrames'
# folder where seams are
siFolder = 'testSeamInfo'
# folder to save seam carved frames to
scFolder = 'testSeams'
# output video name
videoOut = 'testVideoOutSeamsPreCompute7777.mp4'

# starting directory
dirStart = os.getcwd()

# move into frame folder folder
os.chdir('.\\%s' % frameFolder)

# get images in folder
images = [img for img in os.listdir(os.getcwd()) if img.endswith(".jpg")]


seamInfoFile = images[0].split('.')[0] + 'Vert.pckl'
with open(dirStart + '\\' + siFolder  + '\\' + seamInfoFile, "rb") as f:
    vSeams = pickle.load(f)

if dW > len(vSeams):
    raise Exception('Not enough Vertical seams computed') 

seamInfoFile = images[0].split('.')[0] + 'Horz.pckl'
with open(dirStart + '\\' + siFolder  + '\\' + seamInfoFile, "rb") as f:
    hSeams = pickle.load(f)

if dH > len(hSeams):
    raise Exception('Not enough Horizontal seams computed') 


for image in images:
    #print(image)
    im = cv2.imread(image)

    # get stored seams
    seamInfoFile = image.split('.')[0] + 'Vert.pckl'
    with open(dirStart + '\\' + siFolder  + '\\' + seamInfoFile, "rb") as f:
        vSeams = pickle.load(f)

    seamInfoFile = image.split('.')[0] + 'Horz.pckl'
    with open(dirStart + '\\' + siFolder  + '\\' + seamInfoFile, "rb") as f:
        hSeams = pickle.load(f)

    # apply seams
    img = seams_insertion2(im, vSeams[:dH])
    img = seams_insertion2(img, hSeams[:dW])

    # store new image
    cv2.imwrite(dirStart + '\\' + scFolder + '\\' + image, img)


# back to starting folder
os.chdir(dirStart)

# get new images
images = [img for img in os.listdir(scFolder) if img.endswith(".jpg")]

# sort new images in number ending order
images.sort(key=lambda f: int(re.sub('\D', '', f)))

# stitch video together
frame = cv2.imread(os.path.join(scFolder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(videoOut, 0, 15, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(scFolder, image)))

cv2.destroyAllWindows()
video.release()

