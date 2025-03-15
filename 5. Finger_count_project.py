import mediapipe as mp
import cv2

mehands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hand = mehands.Hands(max_num_hands = 1)  # bcz we are using only 1 hand

video = cv2.VideoCapture(0)
while True:
    suc,img = video.read()
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hand.process(img1)
    # print(result.multi_hand_landmarks) # we get x,y,z coordinates of landmarks

    tipid = [4,8,12,16,20]  # tip landmarks of each finger
    lmlist = []


    if result.multi_hand_landmarks:
        for handlms in result.multi_hand_landmarks:
            for id,lm in enumerate(handlms.landmark): # landmark is an object used to find the landmark
                # in id => 0 to 20 index
                # print(id,lm)
                cx = lm.x   # To collect x values only
                cy = lm.y   # To collect y values only

                # append to lmlist (finger,x,y)
                lmlist.append([id,cx,cy])
                # print(lmlist)


                if len(lmlist)!=0 and len(lmlist)==21: # We need to count and perform comparison only when the 21 landmarks are detected.
                    fingerlist = []  # to compare

                    # For thumb right hand
                    if lmlist[12][1] < lmlist[20][1]:  # 1 -> x coordinate, comparing middle and pinky finger to identify whether it is left hand or right hand
                        if lmlist[4][1] > lmlist[3][1]:
                            fingerlist.append(0) # closed
                        else:
                            fingerlist.append(1) # open

                    # for thumb left hand
                    else:
                        if lmlist[4][1] < lmlist[3][1]:
                            fingerlist.append(0) # closed
                        else:
                            fingerlist.append(1) # open


                    # all fingers except thumb
                    for i in range(1,5): 
                        if lmlist[tipid[i]][2] > lmlist[tipid[i]-2][2]: # 2 means 2nd index of lmlist ie [id,x,y] y is the 2nd index
                            fingerlist.append(0) # 0 means finger is closed
                        else:
                            fingerlist.append(1) # 1 means finger is open
                    # print(fingerlist)

                    # we need the count of fingers which are open 
                    if len(fingerlist)!=0: # this should not be an empty list
                        finger_count = fingerlist.count(1)
                    # print(finger_count)

                    # Here the o/p is displayed in the terminal. But we need to show that in the screen itself.
                    cv2.putText(img,"Count:"+str(finger_count),(35,425),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),3)

                    if finger_count == 5:
                        cv2.putText(img,"Hey",(35,250),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,0),3)
                    elif lmlist[8][2] < lmlist[6][2] and lmlist[12][2] < lmlist[10][2]: # index & middle finger
                        cv2.putText(img,"Peace",(35,250),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,0),3)
                    elif lmlist[8][2] < lmlist[6][2]: #index finger up
                        cv2.putText(img,"Mrng",(35,250),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,0),3)
                    
                    elif lmlist[4][1] > lmlist[3][1] and lmlist[20][2] < lmlist[18][2]: #thumb & pinky
                        cv2.putText(img,"Yo Yo",(35,250),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,0),3)
                    elif lmlist[4][2] > lmlist[20][2]: 
                        cv2.putText(img,"Thumbs down",(35,250),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,0),3)
                    elif lmlist[4][2] < lmlist[20][2]:
                        cv2.putText(img,"Thumbs up",(35,250),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,0),3)


            mp_drawing.draw_landmarks(img,handlms,mehands.HAND_CONNECTIONS)

    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()