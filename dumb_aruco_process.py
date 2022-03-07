from cv2 import aruco
import cv2
import numpy as np 

def read_single_image(file_name, ar_dict, ar_params, desired_ids=None):
    img = cv2.imread(file_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    bboxs, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters = aruco_params)

    id_data = dict()
    for id, box in zip(ids, bboxs):
        if desired_ids is not None and id in desired_ids:
            id_data[id[0]] = box[0]
    
    # double check that all desired ids are accounted for
    for idd in desired_ids:
        if idd not in id_data.keys():
            id_data[idd] = np.array([[np.nan, np.nan], [np.nan, np.nan], [np.nan, np.nan], [np.nan, np.nan]])

    # if it doesn't find any desired ids, return None
    if not id_data:
        id_data = None

    return id_data

desired_ids =[0, 3, 4]

# # read a single image
# img = cv2.imread("tests/left0000.jpg")
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# set up aruco dict and parameters
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
aruco_params = aruco.DetectorParameters_create()

# bboxs, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters = aruco_params)

# id_data = dict()

# for id, box in zip(ids, bboxs):
    
#     if id in desired_ids:
#         id_data[id[0]] = box[0]
file = "tests/left0000.jpg"
file2 = "tests/img_mult.jpg"
data = read_single_image(file2, aruco_dict, aruco_params, desired_ids=desired_ids)
print(data)

#if draw: 
#aruco.drawDetectedMarkers(img, bboxs) 
