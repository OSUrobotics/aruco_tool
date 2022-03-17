"""
Specifically testing package's ability to analyze image(s) for aruco code corners
"""

#import pytest
import numpy as np
from cv2 import aruco
from aruco_tool import CornerFinder, ArucoCorner


# single image analysis
def test_single_id_found():
    """
    Tests that it finds a single id in an image
    """
    ar_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
    ar_params = aruco.DetectorParameters_create()

    t1 = CornerFinder("")
    data = t1._analyze_single_image("img_single.jpg", ar_dict, ar_params) # contains 2
    
    assert 2 in data.keys()
    

def test_single_id_cant_find():
    """
    Tests that it handles ids that it can't find in an image correctly 
    """
    ar_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
    ar_params = aruco.DetectorParameters_create()

    t1 = CornerFinder("")
    data = t1._analyze_single_image("img_mult.jpg", ar_dict, ar_params, desired_ids=[0, 1, 5]) # contains 0, 1, 2, 3
    
    assert 5 in data.keys()
    assert np.isnan(data[5][0][0])


def test_single_id_not_desired():
    """
    Tests that it handles ids that we weren't looking for in an img correctly
    """
    ar_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
    ar_params = aruco.DetectorParameters_create()

    t1 = CornerFinder("")
    data = t1._analyze_single_image("img_mult.jpg", ar_dict, ar_params, desired_ids=[0, 1, 2, 5]) # contains 0, 1, 2, 3
    
    assert 3 not in data.keys()


# getting multiple file names
def test_stream_files():
    """
    Tests that it finds the correct number of files in a folder
    """

    t1 = CornerFinder("stream_simple")
    files = t1._get_image_files()

    assert len(files) == 5

    t2 = CornerFinder("stream_mult")
    files2 = t2._get_image_files()

    assert len(files2) == 6


# test corner finding across multiple files
def test_stream_found_id():
    """
    Tests that the desired id we found has the correct number of corner sets to image numbers 
    """
    t1 = CornerFinder("stream_simple")
    data = t1._find_corners(desired_ids=[2])

    assert 2 in data.keys()


def test_stream_id_appears():
    """
    Tests that an id that appears midway through a stream has nan values placed for previous frames it wasn't in, and values where it is 
    """
    t1 = CornerFinder("stream_appear")
    data = t1._find_corners()

    assert 0 in data.keys()
    assert np.isnan(data[0][0][0][0]) # check that nans exist at beginning
    assert np.isreal(data[0][2][0][0]) # third image is when we expect this id to show up


def test_stream_id_disappears():
    """
    Tests that an id that disappears midway through a stream has nan values placed for subsequent frames it wasn't in, and values where it is 
    """
    t1 = CornerFinder("stream_disappear")
    data = t1._find_corners()

    assert 0 in data.keys()
    assert np.isnan(data[0][4][0][0]) # expected id to disappear in fifth image
    assert np.isreal(data[0][0][0][0]) # id exists at beginning, checking to see if it works

# test ArucoCorner object creation

def test_correct_aruco_corner_id():
    """
    Tests that the ArucoCorner object made by the corner finder is well formed 
    """
    t1 = CornerFinder("stream_simple")
    ids_found = t1.corner_analysis()
    
    correct_id = False
    correct_file_loc = False
    correct_data_len = False

    for id in ids_found:
        if id.id == 1:
            correct_id = True
        
            if id.file_loc == "stream_simple":
                correct_file_loc = True

            if id.data_len == 5:
                correct_data_len = True

    assert correct_id
    assert correct_file_loc
    assert correct_data_len


def test_moving_average_preceeding_nans():
    """
    Tests that the moving average function correctly handles the moving average when there are trailing nans. The trailing nans should still exist, contrary to what pandas rolling average would do on its own
    """
    t1 = CornerFinder("stream_appear")
    ids_found = t1.corner_analysis()

    zero_index = 1 # grabbing the id 0 aruco code, used to be consistently index 1, but adding for loop just in case
    for i, a in enumerate(ids_found):
        if a.id == 0:
            zero_index = i
            break

    test_data = ids_found[zero_index]
    filt_data = test_data._moving_average()

    assert np.all(np.isnan(filt_data[0]) & np.all(np.isnan(filt_data[1])))


def test_moving_average_trailing_nans():
    """
    Tests that the moving average function correctly handles the moving average when there are trailing nans. The trailing nans should still exist, contrary to what pandas rolling average would do on its own
    """
    t1 = CornerFinder("stream_disappear")
    ids_found = t1.corner_analysis()

    zero_index = 1 # grabbing the id 0 aruco code, used to be consistently index 1, but adding for loop just in case
    for i, a in enumerate(ids_found):
        if a.id == 0:
            zero_index = i
            break

    test_data = ids_found[zero_index]
    filt_data = test_data._moving_average()

    assert np.all(np.isnan(filt_data[4]) & np.all(np.isnan(filt_data[5])))

# test 1) aruco corner getting of first row and 2) that it reshapes to the correct size