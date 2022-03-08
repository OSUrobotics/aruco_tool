"""
Specifically testing package's ability to analyze aruco codes in a single image 
"""

#import pytest
import pdb
import numpy as np
from cv2 import aruco
from aruco_tool import CornerFinder


# single image analysis
def test_single_id_found():
    """
    Tests that it finds a single id in an image
    """
    ar_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
    ar_params = aruco.DetectorParameters_create()

    t1 = CornerFinder("")
    data = t1._analyze_single_image("tests/img_single.jpg", ar_dict, ar_params) # contains 0, 1, 2, 3
    
    assert 2 in data.keys()
    

def test_single_id_cant_find():
    """
    Tests that it handles ids that it can't find in an image correctly 
    """
    ar_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
    ar_params = aruco.DetectorParameters_create()

    t1 = CornerFinder("")
    data = t1._analyze_single_image("tests/img_mult.jpg", ar_dict, ar_params, desired_ids=[0, 1, 5]) # contains 0, 1, 2, 3
    
    assert 5 in data.keys()
    assert np.isnan(data[5][0][0])


def test_single_id_not_desired():
    """
    Tests that it handles ids that we weren't looking for in an img correctly
    """
    ar_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
    ar_params = aruco.DetectorParameters_create()

    t1 = CornerFinder("")
    data = t1._analyze_single_image("tests/img_mult.jpg", ar_dict, ar_params, desired_ids=[0, 1, 2, 5]) # contains 0, 1, 2, 3
    
    assert 3 not in data.keys()


# getting multiple file names
def test_stream_files():
    """
    Tests that it finds the correct number of files in a folder
    """

    t1 = CornerFinder("tests/stream_simple")
    files = t1._get_image_files()

    assert len(files) == 5

    t2 = CornerFinder("tests/stream_mult")
    files2 = t2._get_image_files()

    assert len(files2) == 6


# test corner finding across multiple files
def test_stream_found_id():
    """
    Tests that the desired id we found has the correct number of corner sets to image numbers 
    """
    t1 = CornerFinder("tests/stream_simple")
    data = t1._find_corners(desired_ids=[2])

    assert 2 in data.keys()


def test_stream_id_appears():
    """
    Tests that an id that appears midway through a stream has nan values placed for previous frames it wasn't in, and values where it is 
    """
    t1 = CornerFinder("tests/stream_appear")
    data = t1._find_corners()

    assert 0 in data.keys()
    assert np.isnan(data[0][0][0][0]) # check that nans exist at beginning
    assert np.isreal(data[0][2][0][0]) # third image is when we expect this id to show up


def test_stream_id_disappears():
    """
    Tests that an id that disappears midway through a stream has nan values placed for subsequent frames it wasn't in, and values where it is 
    """
    t1 = CornerFinder("tests/stream_disappear")
    data = t1._find_corners()

    assert 0 in data.keys()
    assert np.isnan(data[0][4][0][0]) # expected id to disappear in fifth image
    assert np.isreal(data[0][0][0][0]) # id exists at beginning, checking to see if it works

