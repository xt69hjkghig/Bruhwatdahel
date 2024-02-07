import cv2
from PIL import Image as Img
import numpy as np 
from time import time as tm


start = tm()
def racist(image1, image2):         #Detect and replace pixel value function
    real_output_image = Img.new('L', (1440, 1080))
    image = real_output_image.load()
    for i in range(0, 1440):
        for j in range(0, 1080):
            if image1[i, j] == image2[i, j]:
                image[i, j] = 130
            elif image1[i, j] != image2[i, j] and image1[i, j] <=128:
                image[i, j] = 255
            elif image1[i, j] != image2[i, j] and image1[i, j] >128:
                image[i, j] = 0
    return real_output_image


frame_number = 0
out = cv2.VideoWriter('project.avi', cv2.VideoWriter.fourcc(*'DIVX'), 60, (1440, 1080)) # simple cv2 init
cap = cv2.VideoCapture('badapple60fps.mp4')
cap2 = cv2.VideoCapture('badapple60fps.mp4')
TOTAL_FRAME = cap.get(cv2.CAP_PROP_FRAME_COUNT)


while(frame_number < (TOTAL_FRAME - 1)):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)  
    ret, frame = cap.read()     
    cap2.set(cv2.CAP_PROP_POS_FRAMES, frame_number+1)
    ret2, frame2 = cap2.read()


    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)     
    frame_pil = Img.fromarray(frame)
    pixels = frame_pil.load()
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    frame_pil2 = Img.fromarray(frame2)
    pixels2 = frame_pil2.load()


    output = racist(pixels, pixels2)        #Run the function through PIL.Image
    real_output_image = cv2.cvtColor(np.array(output), cv2.COLOR_RGB2BGR)    #Load the frame back to cv2 (yea i don't like opencv that much)
    out.write(real_output_image)
    print(frame_number)
    frame_number += 1
print('Time Taken: ' + str(int(tm() - start)) + ' seconds.')


