import cv2
import os
from sc_vid import seam_carve
import numpy as np
import pickle
import re

# Video to frames

# video file to change
videoFile = '144p.mp4'
# output video name
videoOut = 'testVideoOut.mp4'

# folder to save frames to
frameFolder = 'testFrames'
# folder to save seam carved frames to
scFolder = 'testSeams'
#folder to save seam information to
siFolder = 'testSeamInfo'

# output video height in pixels
newHeight = 144

# output video width in pixels
newWidth = 256

# starting directory
dirStart = os.getcwd()

# if folder does not exist, make it
if not os.path.isdir(frameFolder):
    os.mkdir(frameFolder)
    print('made directory: ' + frameFolder)

if not os.path.isdir(scFolder):
    os.mkdir(scFolder)
    print('made directory: ' + scFolder)

if not os.path.isdir(siFolder):
    os.mkdir(siFolder)
    print('made directory: ' + siFolder)




# capture frames sequentially 
vidcap = cv2.VideoCapture(videoFile)
success,image = vidcap.read()
count = 0

# move into frame folder folder
os.chdir('.\\%s' % frameFolder)

while success:
    cv2.imwrite('frame%d.jpg' % count, image)     # save frame as JPEG file
    success,image = vidcap.read()

    #frame counter
    print('frame %d' % count)
    count += 1
  
# Technical help provided by stackoverflow
# https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames


# Do seam carving here
images = [img for img in os.listdir(os.getcwd()) if img.endswith(".jpg")]

#sort files numerically not alphabetically
images.sort(key=lambda f: int(re.sub('\D', '', f))) 

# Technical help provided by stackoverflow
# https://stackoverflow.com/questions/33159106/sort-filenames-in-directory-in-ascending-order/33159707

# find number of vertical frames to add to make 16:9
height, width = np.shape(cv2.imread(images[0]))[:2]
#dW = int(np.ceil(height*16/9)) - width
dW = newWidth - width

# number of horizontal frames to add
dH = newHeight - height

count = 0
for img in images:
    im = cv2.imread(img)

    # perform seam carving
    #newIm, seamInfo = seam_carve(im, 0, dW)
    newIm, verSeam, horSeam = seam_carve(im, dH, dW)

    # save images to folder
    cv2.imwrite(dirStart + '\\' + scFolder + '\\' + img, newIm)

    # save seam information VERTICAL
    seamInfoFile = img.split('.')[0] + 'Vert.pckl'
    f = open(dirStart + '\\' + siFolder + '\\' + seamInfoFile, 'wb')
    pickle.dump(verSeam, f)
    f.close()

    # save seam information HORIZONTAL
    seamInfoFile = img.split('.')[0] + 'Horz.pckl'
    f = open(dirStart + '\\' + siFolder + '\\' + seamInfoFile, 'wb')
    pickle.dump(horSeam, f)
    f.close()

    print('seam carved frame %d' % count )
    count += 1



# back to starting folder
os.chdir(dirStart)

images = [img for img in os.listdir(scFolder) if img.endswith(".jpg")]

images.sort(key=lambda f: int(re.sub('\D', '', f)))

frame = cv2.imread(os.path.join(scFolder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(videoOut, 0, 15, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(scFolder, image)))

cv2.destroyAllWindows()
video.release()

# Technical help provided by stackoverflow
# https://stackoverflow.com/questions/44947505/how-to-make-a-movie-out-of-images-in-python


