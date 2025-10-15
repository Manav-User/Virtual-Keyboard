import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8)
keys = [["Q","W","E","R","T","Y","U","I","O","P","<--"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]]
finalText = ""

def drawALL(img,buttonList):
    for button in buttonList:
        x,y = button.pos
        w,h = button.size
        cvzone.cornerRect(img,(button.pos[0],button.pos[1],button.size[0],button.size[1]),20,rt=0)
        cv2.rectangle(img,button.pos,(x+w,y+h),(0,0,0),cv2.FILLED)
        cv2.putText(img,button.text,(x+25,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
    return img

## For Blurr keys and able to see background
# def drawALL(img,buttonList):
#     imgNew = np.zeros_like(img,np.uint8)
#     for button in buttonList:
#         x,y = button.pos
#         w, h = button.size
#         cvzone.cornerRect(imgNew,(x, y, w, h),20,rt=0)
#         cv2.rectangle(imgNew,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
#         cv2.putText(imgNew,button.text,(x+25,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
#     out = img.copy()
#     alpha = 0.5
#     mask = cv2.cvtColor(imgNew, cv2.COLOR_BGR2GRAY)
#     mask = mask > 0
#     out[mask] = cv2.addWeighted(img,alpha,imgNew,1-alpha,0)[mask]
#     return out

class Button:
    def __init__(self,pos,text,size=[85,85]):
        self.pos = pos
        self.size = size
        self.text = text
       
buttonList = []
for i in range(len(keys)):
    for j,key in enumerate(keys[i]):
        if key == "<--":
            buttonList.append(Button([100*j+50,100*i+50],key,[180,85]))
        else:
            buttonList.append(Button([100*j+50,100*i+50],key))
   
while True:
    success,img = cap.read()
    hands,img = detector.findHands(img)
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]

    img = drawALL(img,buttonList)
    
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        
        for button in buttonList:
            x,y = button.pos
            w,h = button.size
            if x<lmList[8][0]<x+w and y<lmList[8][1]<y+h:
                cv2.rectangle(img,(x-5,y-5),(x+w+5,y+h+5),(96, 96, 96),cv2.FILLED)
                cv2.putText(img,button.text,(x+25,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                p1 = lmList[8][:2]
                p2 = lmList[12][:2]
                l, _, _ = detector.findDistance(p1,p2,img)

                if l<30:
                    cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED)
                    cv2.putText(img,button.text,(x+25,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                    if button.text == "<--":
                        finalText = finalText[:-1] 
                    else:
                        finalText += button.text
                    sleep(0.2)
    
    cv2.rectangle(img,(50,570),(800,670),(0,255,255),cv2.FILLED)
    cv2.putText(img,finalText,(60,650),cv2.FONT_HERSHEY_PLAIN,5,(128,0,128),5) 
    cv2.putText(img,"Text Bar:",(50, 540),cv2.FONT_HERSHEY_TRIPLEX,2,(0,0,0),3)       
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break