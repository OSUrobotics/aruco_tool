import os 
import cv2
import numpy as np
from pathlib import Path
from cv2 import aruco
import pdb

# for me:
""" 
mtx = np.array(((617.0026849655, -0.153855356, 315.5900337131),  # fx, s,cx
...                              (0, 614.4461785395, 243.0005874753),  # 0,fy,cy
...                              (0, 0, 1)))

dist = np.array((0.1611730644, -0.3392379107, 0.0010744837, 0.000905697))
"""



class PoseDetector:
    """
    Takes an ArucoCorner object and converts its corner locations to object pose, given provided configuration settings
    """
    def __init__(self, corner_obj, camera_calib, dists, side_dims, freq):
        self.id = corner_obj.id
        self.aruco_corner = corner_obj
        
        self.mtx = camera_calib
        self.dist = dists

        self.marker_side_dims = side_dims
        self.processing_freq = freq  # take data at every x values

    def calc_poses(self, rel_pos=True):
        """
        Returns calculated poses for given ArucoCorners as an ArucoLoc object 
        """
        
        # pre-allocate the numpy array space
        corners = self.aruco_corner.reshape_corners()
        data_len = corner.data_len

        pose_data = np.full((data_len, 4), np.nan)

        # get the initial pose (even if no relative pose, still need this for calculating the rotation magnitude) 
        #first_corners # TODO: need a function that grabs the first pose 
        init_pose = self._calc_single_pose()

        # go through corners, calculate poses
        for i, c in self.aruco_corner.yield_corners(use_reshape=False):
            try:
                # change the perspective of the coordinates

                pass
            except:

                pass 

            


    def _calc_single_pose(self, corner_set):
        """
        Estimates pose in a single image. 
        """
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers([corner_set], self.marker_side_dims,
                                                                  self.mtx, self.dist)

        pose = np.concatenate((rvec, tvec))
        
        return pose

