import cv2
import numpy as np 
from PIL import Image as Img
from PIL import ImageOps as IOs
from time import time as tm

start = tm()       
out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 60, (1440, 1080))        #Output
video = cv2.VideoCapture('badapple60fps.mp4')       #Get Video    
frame_number = 0            #Init position
TOTAL_FRAME = video.get(cv2.CAP_PROP_FRAME_COUNT) #Get limit

while(frame_number < TOTAL_FRAME):
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)    #Read current frame
    ret, frame = video.read()       

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_pil = Img.fromarray(frame)        #Use PIL instead

    resized_frame = frame_pil.resize((20, 15))
    invert_resized_frame = IOs.invert(resized_frame)        #Invert frame's color

    reading_frame = frame_pil.resize((72, 72))      #Get lightness data
    lightness = reading_frame.getdata()

    real_output_image = Img.new('L', (1440, 1080))      #Create output frame

    for i in range(0, 72):          
        for j in range(0, 72):
            current_width = i * 20          
            current_height = j * 15         
            current_iteration = i  + j * 72
            if (lightness[current_iteration] // 150) < 1:                   
                real_output_image.paste(resized_frame, (current_width, current_height))
            else:
                real_output_image.paste(invert_resized_frame, (current_width, current_height))
    real_output_image = cv2.cvtColor(np.array(real_output_image), cv2.COLOR_RGB2BGR)    #Load the frame back to cv2 (yea i don't like opencv that much)
    out.write(real_output_image)        
    print(frame_number)         #Current iteration
    frame_number += 1

duration = tm() - start     #Get total time taken
print('Time taken: ' + str(int(duration)) + ' seconds')
