import cv2
import numpy as np
import serial
import time #no need to do it with pip
rot=0


ard=serial.Serial('COM15',9600)
time.sleep(2) #time in seconds
cap=cv2.VideoCapture('http://192.168.43.232:4747/video')
fourcc=cv2.VideoWriter_fourcc(*'XVID')
output=cv2.VideoWriter('output_test9.avi',fourcc,20.0,(640,480))
# to save the video
def maxarea_center(frame):#function defined to return  x-coordi. of centre, number of contours
    count=0
    areamax=0
    cx=0

    contours_red, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for c_red in contours_red:
        area=cv2.contourArea(c_red)
        if area>100:
            count+=1

        if area>areamax:
            areamax=area
            M=cv2.moments(c_red)#to find the centroid
            cx=int(M['m10']/M['m00'])
            cy=int(M['m01']/M['m00'])
    return cx,count


last_seen_red = 0


while True:

    ret,frame=cap.read()
    output.write(frame)
    rows=frame.shape[0]
    cols=frame.shape[1]
    M=cv2.getRotationMatrix2D((cols/2,rows/2),-90,1)#to invert the view taken by camera
    frame=cv2.warpAffine(frame,M,(cols,rows))
    # print(frame.shape)
    middle=320
    # print(frame.shape)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    l=np.array([0,100,100])
    u=np.array([10 ,255,255])
    red=cv2.inRange(hsv,l,u)
    mask=cv2.bitwise_and(frame,frame,mask=red)
    lr=np.array([171,142,90])
    ur=np.array([180,255,255])
    red2=cv2.inRange(hsv,lr,ur)
    maskr=cv2.bitwise_and(frame,frame,mask=red2)

    red1= red+red2
    red1 = cv2.morphologyEx(red1, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    # opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones(5, 5))
    red1 = cv2.morphologyEx(red1, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    lb = np.array([92, 68, 141])
    ub = np.array([112, 255, 255])
    blue = cv2.inRange(hsv, lb, ub)
    maskb1 = cv2.bitwise_and(frame, frame, mask=blue)
    Lg = np.array([31, 197, 30])
    Ug = np.array([99, 255, 243])
    green = cv2.inRange(hsv, Lg, Ug)
    maskg1 = cv2.bitwise_and(frame, frame, mask=green)
    count_red=0
    count_green=0
    count_blue=0

    contours_red, _ = cv2.findContours(red1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours_green, _ = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours_blue, _ = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cxr,count_red=maxarea_center(red1)
    cxg, count_green = maxarea_center(green)
    cxb, count_blue = maxarea_center(blue)
    print(cxr)



    print(count_red)
    if count_red>0:
        rot=0
        last_seen_red = cxr
        if count_blue>0 and cxb>middle+250 and cxb<middle-250:
            if cxb-cxr>0:
                ard.write(b'l')
            else:
                ard.write(b'r')
        else:
            if cxr < middle-100:
                ard.write(b'l')
                print('move left')
            elif cxr > middle+100:
                ard.write(b'r')
                print('move right')
            elif cxr > middle-100 and cxr < middle+100:
                ard.write(b'f')
                print('move forward')
    else:
        if rot <= 80:
            if last_seen_red<320:
                ard.write(b'l')
            else:
                ard.write(b'r')
            rot+=1
        else:
            if count_green>0:
                if count_blue > 0 and cxb > middle + 250 and cxb < middle - 250:
                    ard.write('t')
                else:
                    if cxg < middle - 100:
                        ard.write(b'l')
                        print('move left')
                    elif cxg > middle + 100:
                        ard.write(b'r')
                        print('move right')
                    elif cxg >middle-100 and cxg <middle+100:
                        ard.write(b'f')
            else:
                ard.write(b't')

    cv2.imshow('red',red1)
    cv2.imshow('l',frame)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break

cap.release()
output.release()
cv2.destroyAllWindows()