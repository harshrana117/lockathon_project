import cv2
import numpy as np
import win10toast

import plyer.platforms.win.notification
from plyer import notification

import math
import time

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)
#toaster = win10toast.ToastNotifier()

##Initialization
def intialDisplayMessage():
    print('Detecting Face ...')
    time.sleep(2)


##Function to notify user
def notify(distance):
    ##return toaster.show_toast('Eye Care', 'Please maintain a safe distance from laptop screen', duration=2)
    return notification.notify('Eye Care', 'Please maintain a safe distance from laptop screen', app_icon='python.ico', timeout=10, ticker='Maintain distance')

intialDisplayMessage()

#Infinite Loop Runs the application till user ends
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)


    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        face_center_x_cor = x + w/2
        face_center_y_cor = y + h/2

        print('corodinates of face center: ', '(', face_center_x_cor, ', ', face_center_y_cor, ')')

        face_area = h*w

        print('detected face height = ', h)
        print('detected face width = ', w)
        #print('area=', face_area)

        a = math.pow(face_area, -0.61)

        ##Function
        distance = 53588*a

        ##Correction factor (calculated after analysing a lot of data )
        correction_factor = (distance)/4

        user_distance = distance - correction_factor

        print('Approx distance from screen(cm) = ', user_distance)

## Condition Check
        if user_distance < 40:
            notify(user_distance)
            time.sleep(1)
            break

        #print('press Q/q to exit')

## To display the input feed
    cv2.imshow('image', img)

## press q to exit
    k = cv2.waitKey(1)
    if k== ord('q'):
        break


cap.release()
cv2.destroyAllWindows()