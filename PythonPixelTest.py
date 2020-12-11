
import sys
import numpy as np
import cv2


def makeHologram(original, finalsize, innersquare, distance=0):
    side = min(finalsize)
    if (innersquare >= side):
        hologram = None
        return hologram
#    print(side)
    #scale = ()
    scale = 1
    scaleR = 4
    print(original.shape[0])
    print(original.shape[1])

    #width = int((scale*original.shape[1]))
    width = int(side / (1.0 + 2.0 * (float)(original.shape[0]) / original.shape[1]))
    #height = int((scale*original.shape[0]))
    height = int(side / (2.0 + (float)(original.shape[1]) / original.shape[0]))
#    print(height)
#    print(width)
    offset = 0
    if (2 * height + innersquare >= side):
        print("square")
        offset = int((width - (side - innersquare) / 2 * (original.shape[1] / original.shape[0])) / 2 - (side - innersquare) / 2 + height)
        height = int((side - innersquare) / 2)
        width = int((side - innersquare) / 2 * (original.shape[1] / original.shape[0]))
#        print(height)
#        print(width)
#        print(offset)
    

    image = cv2.resize(original, (width, height), interpolation = cv2.INTER_CUBIC)
    
    up = image.copy()
    down = rotate_bound(image.copy(),180)
    right = rotate_bound(image.copy(), 90)
    left = rotate_bound(image.copy(), 270)
    
    hologram = np.zeros([side, side, 3], image.dtype)

    #center_x = (int)(hologram.shape[0])/2
    #center_y = (int)(hologram.shape[1])/2

    #vert_y = (int)(up.shape[0])/2
    #vert_x = (int)(up.shape[1])/2
    #hologram[0:(int)(up.shape[0]), (int)(center_x-vert_x+distance):(int)(center_x+vert_x+distance)] = up
    #hologram[(int)(hologram.shape[0]-down.shape[0]):(int)(hologram.shape[0]) , (int)(center_x-vert_x+distance):(int)(center_x+vert_x+distance)] = down
    
    hologram[0:height, height + offset:width+height + offset] = up
    hologram[side - height:side, side - height - width - offset:side - height - offset] = down
    
    #hori_y = (int)(right.shape[0])/2
    #hori_x = (int)(right.shape[1])/2
    #hologram[ (int)(center_x-hori_x) : (int)(center_x-hori_x+right.shape[0]) , (int)(hologram.shape[1]-right.shape[1]+distance) : (int)(hologram.shape[1]+distance)] = right
    #hologram[ (int)(center_x-hori_x) : (int)(center_x-hori_x+left.shape[0]) , (int)(0+distance) : (int)(left.shape[1]+distance) ] = left
    
    hologram[height + offset:height + width + offset, side - height:side] = right
    hologram[side - height - width - offset:side - height - offset, 0:height] = left


    #cv2.imshow("up",up)
    #cv2.imshow("down",down)
    #cv2.imshow("left",left)
    #cv2.imshow("right",right)
    #cv2.imshow("hologram",hologram)
    return hologram

def process_video(video):
    cap = cv2.VideoCapture(video)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    holo = None
    ret = False
    while(not ret):
        ret, frame = cap.read()
        if ret:
            #frame = cv2.resize(frame, (640, 640), interpolation = cv2.INTER_CUBIC)
            holo = makeHologram(frame, (640, 640), 0)
    out = cv2.VideoWriter('hologram.avi',fourcc, 30.0, (holo.shape[0],holo.shape[1]))
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    count = 0
    print ("Processing %d frames"%(total_frames))
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            #frame = cv2.resize(frame, (640, 640), interpolation = cv2.INTER_CUBIC)
            holo = makeHologram(frame, (640, 640), 0)
            out.write(holo)
            count += 1
            print ("Total:%d of %d"%(count,total_frames))
        if(count>=total_frames-1):
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    return

def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))
    
if __name__ == '__main__' :
    if (len(sys.argv) == 2) :
        #try :
        orig = cv2.imread(sys.argv[1])
        holo = makeHologram(orig, (1920, 720), 400)
        process_video("C:/Users/arthu/Pictures/clip_snowball.mp4")
            #cv2.imwrite("hologram.png",holo)
#        except ValueError:
#            exit(84)
        exit(0)
    exit(84)