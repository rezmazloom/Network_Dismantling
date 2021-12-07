#!/env/python3

import cv2
import os
import numpy as np

IMAGEFOLDER = "figures1CCM_RA_S1_edited"
VIDEONAME = "CM_RA_S1.avi"

images = np.sort([img for img in os.listdir(IMAGEFOLDER) if img.endswith(".png")]).tolist()
frame = cv2.imread(os.path.join(IMAGEFOLDER, images[0]))
height, width, layers = frame.shape

# parameters
# filename, fourcc(int), FPS, dimentions(tuple(w,h)) 
video = cv2.VideoWriter(VIDEONAME, 0, 1,(width,height))

for image in images:
  video.write(cv2.imread(os.path.join(IMAGEFOLDER, image)))

cv2.destroyAllWindows()
video.release()

#def save():
#  os.system("ffmpeg -r 1 -i img%01d,png -vcodec mpeg4 -y movie.mp4")

#import ffmpeg #ffmpeg-python
#(
#  ffmpeg
#  .input("/figures1CCM_RA/*.png",
#  pattern_type="glob", framerate=1)
#  .output("movie.mp4")
#  .run()
#)
