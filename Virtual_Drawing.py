#Importing cv2 and numpy library
import cv2
import numpy as np

#Accessing webcam and assigning into the variable name called "cap"
cap = cv2.VideoCapture(0)

#Creating a window for the workspace
cv2.namedWindow("Result", cv2.WINDOW_FREERATIO)

#Setting up colour's lower and upper limit of HSV
myColours = [[26, 137, 255, 46, 224, 255],    #Orange
            # [135, 110, 145, 179, 255, 255 ],    #red
            # [30, 62, 255, 36, 232, 255 ], #yellow
            # [0, 0, 255, 0, 0, 255], #white
            # [ 110, 153, 157, 117, 213, 230],    #Blue
            [52, 80, 96, 90, 123, 180]]     #Green

#Setting up BGR values of specified colour
ColourVal = [[0, 225, 255],         #Orange
                # [0,28,255],           #Red
                # [0,185,255],          #Yellow
                # [255, 255, 255],        #white
                # [154,189,31],         #Blue
                [0, 255, 0]]          #Green


#Creating an empty array to store coordinates of x,y, and BGR colourID's
myPoints =  []                          #[x , y , colourID ]

#Finding the colour of the object
def findColor(frame,myColours,ColourVal):
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    count = 0                                       
    newPoints=[]                                    
    for colour in myColours:
        lower = np.array(colour[0:3])
        upper = np.array(colour[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        ret1, thresh = cv2.threshold(mask,1,255,cv2.THRESH_BINARY)
        #cv2.imshow("thresh",thresh)
        x,y=Contours(thresh)
        cv2.circle(frame,(x,y),8,ColourVal[count],cv2.FILLED)
       
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count +=1
    return newPoints
    

#Contour 
def Contours(frame):
    contours,hierarchy = cv2.findContours(frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    x,y,w,h = 0,0,0,0
       

    for cnt in contours:
        if cv2.contourArea(cnt)>1:   
            
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx) 
    return x+w//2,y   #Returning the coordinate of the top tip of the contour


#Drawing 
def draw(myPoints,ColorVal):
    for point in myPoints:
        cv2.circle(frame,(point[0],point[1]),8,ColourVal[point[2]],cv2.FILLED)



'''def draw(myPoints,ColorVal):
    if len(myPoints)>2:
         for i in range(1,len(myPoints)):
           
            cv2.line(frame,(myPoints[i-1][0],myPoints[i-1][1]),(myPoints[i][0],myPoints[i][1]),ColourVal[myPoints[i][2]],5)
'''

while True:
    ret, frame = cap.read()
    
    newPoints = findColor(frame, myColours,ColourVal)

    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints)!=0:
        draw(myPoints,ColourVal)    
        
    flip = cv2.flip(frame,1)      
    cv2.imshow("Result", flip)   
    if cv2.waitKey(10) == ord(' '):
        break

cv2.destroyAllWindows()
cap.release() 