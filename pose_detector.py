import os 
import cv2
import numpy as np
from pathlib import Path
from cv2 import aruco
import pdb


class PoseDetector:
    """
    Takes an ArucoCorner object and converts its corner locations to object pose, given provided configuration settings
    """
    def __init__(self, corner_obj, camera_calib, dists, side_dims, freq):
        self.id = corner_obj.id
        
        
        self.mtx = camera_calib
        self.dist = dists

        self.code_side_dims = side_dims
        self.processing_freq = freq  # take data at every x values

    def calc_poses():
        """
        Returns calculated poses for given ArucoCorners as an ArucoLoc object 
        """
        
        pass

    def _calc_single_pose():
        """
        Estimates pose in a single image. 
        """
        
        pass
