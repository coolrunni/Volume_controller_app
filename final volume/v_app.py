from tkinter import *
from tkinter import messagebox 
from PIL import Image,ImageTk
import cv2
import time
from matplotlib.ft2font import BOLD
from matplotlib.pyplot import draw
import numpy as np
import HandtrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
##################
wCam, hCam = 640, 480
##################


root=Tk()
root.title("")
root.geometry("430x300")
Label(root,text="VOLUME CONTROL USING CAMERA",font=("Calibri 13 bold")).grid(row=0,column=1)
desc_user=Label(root,text="""Control anything with the tip of your finger!



Developer - Sanju(tkinter) and Arijit(opencv)""", font=5)
desc_user.grid(row=1,column=1)
# pic_label=Label(image=PhotoImage(file="ngo.png")).grid(row=2,column=0)




def show():
    msg=messagebox.askyesno("Security Alert!","Are you sure to open your camera")
    if msg == True:
        cap = cv2.VideoCapture(1)
        cap.set(3, wCam)
        cap.set(4, hCam)
        ptime=0

        detector = htm.handDetector()



        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        #volume.GetMute()
        #volume.GetMasterVolumeLevel()
        volRange = volume.GetVolumeRange()
        volume.SetMasterVolumeLevel(0, None)
        minVol = volRange[0]
        maxVol = volRange[1]

        vol=0
        volBar=400
        volPer=0

        while True:
            success, img = cap.read()
            detector.findHands(img)
            lmList = detector.findPosition(img, draw=False)
            if len(lmList)!= 0:
                #print(lmList[4],lmList[8])

                x1, y1 =lmList[4][1], lmList[4][2]
                x2, y2 =lmList[8][1], lmList[8][2]
                cx, cy = (x1+x2)//2, (y1+y2)//2

                cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
                cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
                cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)
                cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)

                length = math.hypot(x2-x1, y2-y1)
                #print(length)

                #Hand range 50 - 300
                #Volume Range 65 - 0 


                vol = np.interp(length, [50, 300], [minVol, maxVol])
                volBar = np.interp(length, [50, 300], [400, 150])
                volPer = np.interp(length, [50, 300], [0, 100])
                #print(int(length), vol)
                volume.SetMasterVolumeLevel(vol, None)



                if length<50:
                    cv2.circle(img, (cx,cy), 15, (0, 255, 0), cv2.FILLED)

            cv2.rectangle(img, (50,150), (85,400), (0, 255, 0), 2)
            cv2.rectangle(img, (50, int(volBar)), (85,400), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{str(int(volPer))} %',(40,450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 3)


            ctime = time.time()
            fps = 1/(ctime-ptime)
            ptime = ctime

            cv2.putText(img, f'FPS: {str(int(fps))}',(40,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)


            cv2.imshow("Img", img)
            cv2.waitKey(1)

Button(root,text="Next>",command=show).grid(row=2,column=1,padx=10,pady=150)
Button(root,text="Exit",command=root.destroy).grid(row=2,column=0,padx=20,pady=150)

root.mainloop()