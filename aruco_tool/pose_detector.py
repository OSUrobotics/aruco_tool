import os 
import cv2
import numpy as np
from pathlib import Path
from cv2 import aruco
import pdb
from aruco_loc import ArucoLoc

# for me:
""" 
mtx = np.array(((617.0026849655, -0.153855356, 315.5900337131),  # fx, s,cx
                            (0, 614.4461785395, 243.0005874753),  # 0,fy,cy
                            (0, 0, 1)))

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


    def find_marker_locations(self):
        """
        Calculates poses and outputs that data as ArucoLoc objects 
        """
        poses = self.calc_poses()

        return ArucoLoc(self.id, poses, file_folder=self.aruco_corner.file_loc)


    def calc_poses(self, rel_pos=True):
        """
        Returns calculates poses for the given ArucoCorner object
        """
        
        # pre-allocate the numpy array space
        data_len = self.aruco_corner.data_len

        pose_data = np.full((data_len, 8), np.nan)

        # get the initial pose (even if no relative pose, still need this for calculating the rotation magnitude) 
        #first_corners
        _, init_corners = self.aruco_corner.get_init_corner()
        [init_rvec, init_tvec] = self._calc_single_pose(init_corners) # TODO: should we make it stricter, so that its guaranteed there are no np.nan?

        # go through corners, calculate poses
        for i, next_corners in self.aruco_corner.yield_corners(use_reshaped=False):
            try:
                # if its all nans, just skip calculation
                if np.all(np.isnan(next_corners)):
                    raise Exception("Row of nans, skipping calculation")

                [next_rvec, next_tvec] = self._calc_single_pose(next_corners)

                rel_angle = self._angle_between(init_corners[0] - init_corners[2], next_corners[0] - next_corners[2])
                rel_rvec, rel_tvec = self._relative_position(init_rvec, init_tvec, next_rvec, next_tvec)

                translation_val = np.round(np.linalg.norm(rel_tvec), 4)
                rotation_val = rel_angle * 180 / np.pi

                # found the stack overflow for it?
                # https://stackoverflow.com/questions/51270649/aruco-marker-world-coordinates
                rotM = np.zeros(shape=(3, 3))
                cv2.Rodrigues(rel_rvec, rotM, jacobian=0)
                ypr = cv2.RQDecomp3x3(rotM)  # TODO: not sure what we did with this earlier... need to check

                row_data = [rel_tvec[0][0], rel_tvec[1][0], rel_tvec[2][0], translation_val, rel_rvec[0][0], rel_rvec[1][0], rel_rvec[2][0], rotation_val]
                
                #total_successes += 1
            except Exception as e:
                #print(f"Error with ARuco corners in image {i}.")
                #print(e)
                # rel_rvec, rel_tvec = (np.nan, np.nan, np.nan), (np.nan, np.nan, np.nan)
                # translation_val = np.nan
                # rotation_val = np.nan
                row_data = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
            
            # put into numpy array
            # tvec (3), tmag, rvec (3), rmag
            
            pose_data[i] = row_data

        return np.around(pose_data, decimals=3)


    def _calc_single_pose(self, corner_set):
        """
        Estimates pose in a single image. 
        """
        # if np.all(np.isnan(corner_set)):
        #     print("all are nan")
        
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers([corner_set], self.marker_side_dims, self.mtx, self.dist)

        pose = np.concatenate((rvec, tvec))
        
        return pose #[rvec, tvec]


    def _unit_vector(self, vector):
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)


    def _angle_between(self, v1, v2):
        """ Returns the angle in radians between vectors 'v1' and 'v2'::

                example 1) angle_between((1, 0, 0), (0, 1, 0))
                1.5707963267948966
                example 2) angle_between((1, 0, 0), (1, 0, 0))
                0.0
                example 3) angle_between((1, 0, 0), (-1, 0, 0))
                3.141592653589793
                *ahem* https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
                (look at highest voted answer, then scroll down to sgt_pepper and crizCraig's answer
        """
        v1_u = self._unit_vector(v1)
        v2_u = self._unit_vector(v2)

        minor = np.linalg.det(
            np.stack((v1_u[-2:], v2_u[-2:]))
        )

        if minor == 0:
            sign = 1
        else:
            sign = -np.sign(minor)

        dot_p = np.dot(v1_u, v2_u)
        dot_p = min(max(dot_p, -1.0), 1.0)
        return sign * np.arccos(dot_p)

        # # sgt_pepper
        # if minor == 0:
        #     raise NotImplementedError('Too odd vectors =(')
        # return np.sign(minor) * np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
        # # original
        #return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    def _relative_position(self, rvec1, tvec1, rvec2, tvec2):
        rvec1, tvec1 = np.expand_dims(rvec1.squeeze(),1), np.expand_dims(tvec1.squeeze(),1)
        rvec2, tvec2 = np.expand_dims(rvec2.squeeze(),1), np.expand_dims(tvec2.squeeze(),1)
        invRvec, invTvec = self._inverse_perspective(rvec2, tvec2)

        orgRvec, orgTvec = self._inverse_perspective(invRvec, invTvec)

        info = cv2.composeRT(rvec1, tvec1, invRvec, invTvec)
        composedRvec, composedTvec = info[0], info[1]

        composedRvec = composedRvec.reshape((3, 1))
        composedTvec = composedTvec.reshape((3, 1))

        return composedRvec, composedTvec

    def _inverse_perspective(self, rvec, tvec):
        """
        found you! https://aliyasineser.medium.com/calculation-relative-positions-of-aruco-markers-eee9cc4036e3
        """
        # print(rvec)
        # print(np.matrix(rvec[0]).T)
        R, _ = cv2.Rodrigues(rvec)
        R = np.matrix(R).T
        invTvec = np.dot(-R, np.matrix(tvec))
        invRvec, _ = cv2.Rodrigues(R)
        return invRvec, invTvec


