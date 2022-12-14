import cv2
import os
from cvzone.HandTrackingModule import HandDetector

# for capturing the video
cap = cv2.VideoCapture(0)

#resolution set to base level, 640x480, 1280x720
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("Resources/Background.png")

# storing all the modes into a list
modes_path = "Resources/Modes"
image_mode_path = os.listdir(modes_path)
image_mode = []

for image in sorted(image_mode_path,key=lambda x:int(x.replace('.png', ''))):
    image_mode.append(cv2.imread(os.path.join(modes_path, image)))

# storing all the Icons into a list
icons_path = "Resources/Icons"
icon_path_list = os.listdir(icons_path)
image_icons = []

for icons in sorted(icon_path_list,key=lambda x:int(x.replace('.png', ''))):
    image_icons.append(cv2.imread(os.path.join(icons_path,icons )))

mode_type = 0  # for changing the mode

detector = HandDetector(detectionCon=0.8, maxHands=1)

selection = 0
counter = 0
selection_speed = 7
mode_positions = [(1136,196),(1000,384),(1136,581)] # 0,1,2

counter_pause = 0
order_complete = 0
flag = 0
store_selected_items = [0,0,0]

while flag == 0:
    success, img = cap.read()

    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw

    # overlaying the webcam feed to the background image
    # ration is frame width and height
    imgBackground[139:139+480, 50:50+640] = img
    imgBackground[0:720, 847:1280] = image_mode[mode_type]
    
    if hands and mode_type == 3:
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        if fingers1 == [1,0,0,0,0]:
            if order_complete > 0:
                order_complete += 1
                if order_complete >= 30:
                    flag = 1

    if hands and counter_pause == 0 and mode_type < 3:
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)

        #here the 1 represent index finger this condition will execute. when the user show index finger
        if fingers1 == [0,1,0,0,0]:
            if selection != 1:
                counter = 1
            selection = 1
        elif fingers1 == [0,1,1,0,0]:
            if selection != 2:
                counter = 1
            selection = 2
        elif fingers1 == [0,1,1,1,0]:
            if selection != 3:
                counter = 1
            selection = 3
        else:
            selection = 0
            counter = 0

        if counter > 0:
            counter += 1
            # print(counter)
            """
                here giving the image path -> imgBackground
                center to show mode_positions ((1136,196),(1000,384),(1136,581)) based on the image that i have, (0,1,2) indexes.
                axes : (103,103)
                angle : 0
                start angle : 0
                end angle : counter * seletionspeed
                color : green in rbg(0,255,0)
                thickness of the layer : 20
            """
            cv2.ellipse(imgBackground,mode_positions[selection-1],(103,103),0,0,counter*selection_speed,(0,255,0),10)

            if counter*selection_speed > 360:
                store_selected_items[mode_type] = selection
                mode_type += 1
                counter = 0
                selection = 0
                counter_pause = 1

            if mode_type == 3:
                order_complete = 1

    if counter_pause > 0:
        counter_pause += 1
        if counter_pause >= 60:
            counter_pause = 0

    if store_selected_items[0] != 0:
        imgBackground[636:636 + 65,133:133 + 65] = image_icons[store_selected_items[0]-1]
    if store_selected_items[1] != 0:
        imgBackground[636:636 + 65,340:340 + 65] = image_icons[5+store_selected_items[1]]
    if store_selected_items[2] != 0:
        imgBackground[636:636 + 65,542:542 + 65] = image_icons[2+store_selected_items[2]]


    # cv2.imshow("Image",img)
    cv2.imshow("HandTracker - Coffee Booking", imgBackground)
    cv2.waitKey(1)