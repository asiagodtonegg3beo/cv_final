# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
import numpy as np
from sys import platform
import argparse
import math 

try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/../../build/python/openpose/Release');
            os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../build/x64/Release;' +  dir_path + '/../../build/bin;'
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('../../python');
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", default="C:\\Users\\dvlab\\openpose-1.7.0\\examples\\media\\test.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../../models/"
    params["net_resolution"] = "560x560"
    params["hand"] = True
    
    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item

    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Process Image
    datum = op.Datum()
    imageToProcess = cv2.imread(args[0].image_path)
    imageToProcess = cv2.resize(imageToProcess, (640, 480), interpolation=cv2.INTER_AREA)
    datum.cvInputData = imageToProcess
    opWrapper.emplaceAndPop(op.VectorDatum([datum]))

    # Display Image
    print("Body keypoints: \n" + str(datum.poseKeypoints))
    print(datum.handKeypoints)
    people = datum.poseKeypoints[0]
    monkey = datum.poseKeypoints[1]
    img = datum.cvOutputData
    #cv2.circle(image, (int(coor[0]),int(coor[1])), point_size, point_color, thickness
    human_left_hands = (int(people[7][0]),int(people[7][1]))
    #cv2.circle(img, human_left_hands, 5, (255,0,255), 10)
    #cv2.putText(img, 'human_hands', (human_left_hands[0]-30, human_left_hands[1]+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,255), 2)

    human_bbox = ( 92, 23, 503, 628)
    #cv2.rectangle(img, (human_bbox[0],human_bbox[1]), (human_bbox[0]+human_bbox[2],human_bbox[1]+human_bbox[3]), (0,255,0), 4) #(x,y),(x+w,x+h)
    #cv2.putText(img, 'person', (human_bbox[0], human_bbox[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    monkey_bbox = ( 536, 350, 276, 222)
    #cv2.rectangle(img, (monkey_bbox[0],monkey_bbox[1]), (monkey_bbox[0]+monkey_bbox[2],monkey_bbox[1]+monkey_bbox[3]), (0,0,255), 4) #(x,y),(x+w,x+h)
    #cv2.putText(img, 'monkey', (monkey_bbox[0], monkey_bbox[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)
#-------------------------------------people------------------------------------------------------------------------------------
    people_neck = (int(people[1][0]),int(people[1][1]))
#-------------------------------------people------------------------------------------------------------------------------------
#-------------------------------------monkey------------------------------------------------------------------------------------
    monkey_left_eyes = [int(monkey[16][0]),int(monkey[16][1])] #monkey[16]
    monkey_right_eyes = [int(monkey[15][0]),int(monkey[15][1])] #monkey[15]
    monkey_mid = (int((monkey_left_eyes[0] + monkey_right_eyes[0])/2),int((monkey_left_eyes[1] + monkey_right_eyes[1])/2))
    monkey_nose = (655,403) #monkey[0]
    monkey_left_ear = (int(monkey[18][0]),int(monkey[18][1]))
    monkey_right_ear = (int(monkey[17][0]),int(monkey[17][1]))
    monkey_center = (int((monkey_left_ear[0]+monkey_left_eyes[0])/2),int((monkey_left_ear[1]+monkey_left_eyes[1])/2-15))
    monkey_neck = [int(monkey[1][0]),int(monkey[1][1])]
#-------------------------------------monkey------------------------------------------------------------------------------------

    #image = cv2.arrowedLine(img, monkey_center, monkey_left_eyes, (0,255,0), 2)
    image = cv2.line(img, monkey_neck,people_neck , (0,255,255), 2)
    distance_position = (abs(monkey_neck[0]-people_neck[0]),abs(monkey_neck[1]-people_neck[1]))
    distance = int(math.sqrt(distance_position[0]*distance_position[0]+distance_position[1]+distance_position[1]))
    cv2.putText(img, 'd(people_neck): '+str(distance+1)+' pixel',(monkey_neck[0]-150,monkey_neck[1]-135), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
    #image = cv2.arrowedLine(img, monkey_center, (monkey_left_eyes[0]-3*(monkey_center[0]-monkey_left_eyes[0]),monkey_left_eyes[1]-3*(monkey_center[1]-monkey_left_eyes[1])), (0,0,255),thickness=3)

    #image = cv2.arrowedLine(img, monkey_mid, human_left_hands, (0,0,255), 2)
    cv2.putText(img,'Risk: '+'High',(440,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.putText(img,'Probility:'+'70%',(440,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", img)
    cv2.imwrite('out.jpg',img)
    cv2.waitKey(0)
except Exception as e:
    print(e)
    sys.exit(-1)
