import cv2
from cv2 import aruco
import pdb
import pandas as pd
import numpy as np
from .corner_finder import CornerFinder
from .aruco_corner import ArucoCorner
from .pose_detector import PoseDetector
from .aruco_loc import ArucoLoc


class ArucoFunc:
    """
    Class which holds aruco corner analysis functions (holistic functions, they include everything for easy start)
    """
    def __init__(self, mtx=None, dist=None, marker_side_dims=None):
        """ 
        Input camera settings for aruco analysis. Default parameters are for images not from cameras.
        """

        # camera calibration
        if mtx is None:
            # self.mtx = np.array(((617.0026849655, -0.153855356, 315.5900337131),  # fx, s,cx
            #                     (0, 614.4461785395, 243.0005874753),  # 0,fy,cy
            #                     (0, 0, 1)))
            self.mtx = np.array(((1, 1, 1),  # fx, s,cx
                                (0, 1, 1),  # 0,fy,cy
                                (0, 0, 1)))
        else:
            self.mtx = mtx
        
        if dist is None:
            # k1,k2,p1,p2 ie radial dist and tangential dist
            #self.dist = np.array((0.1611730644, -0.3392379107, 0.0010744837, 0.000905697))
            self.dist = np.array((0, 0, 0, 0))
        else:
            self.dist = dist

        if marker_side_dims is None:
            self.marker_side_dims = 0.03
        else:
            self.marker_side_dims = marker_side_dims
        
        # TODO: add a full and single image analysis for multiple ids

    
    def single_image_analysis_single_id(self, file_loc, desired_id):
        """ 
        Analyzes a single image for a single aruco code, returns the pose
        """
        ar_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
        ar_params = aruco.DetectorParameters_create()

        cf = CornerFinder("")
        c_data = cf._analyze_single_image(file_loc, ar_dict, ar_params)

        ac = ArucoCorner(0, c_data[desired_id])
        pdetect = PoseDetector(ac, self.mtx, self.dist, self.marker_side_dims, 1)
        return pdetect._calc_single_pose(ac.corners)


    def full_analysis_single_id(self, folder, desired_id):
        """
        Full pipeline from img to data, with relative positioning from initial pose
        """
        cf = CornerFinder(folder)
        c_list = cf.corner_analysis()

        id_c = None
        for cs in c_list:
            if cs.id == desired_id:
                id_c = cs
                break
        
        if id_c is None:
            return

        pdetect = PoseDetector(id_c, self.mtx, self.dist, self.marker_side_dims, 1)
        return pdetect.find_marker_locations()


    def single_image_analysis(self, file_loc, desired_ids=None):
        """ 
        Analyzes a single image for a single aruco code, returns the pose
        """
        ar_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
        ar_params = aruco.DetectorParameters_create()

        cf = CornerFinder("")
        c_data = cf._analyze_single_image(file_loc, ar_dict, ar_params, desired_ids=desired_ids)

        aruco_locs = dict()
        temp_key = list(c_data.keys())[0]
        ac = ArucoCorner(0, c_data[temp_key]) # this is a dummy ac obj, needed for pose detector
        pdetect = PoseDetector(ac, self.mtx, self.dist, self.marker_side_dims, 1)

        for k in c_data:
            k_pose = pdetect._calc_single_pose(c_data[k])

            aruco_locs[k] = k_pose

        return aruco_locs


    def full_analysis(self, folder, desired_ids=None):
        """
        Full pipeline from img to data, with relative positioning from initial pose
        """
        cf = CornerFinder(folder, desired_ids=desired_ids)
        c_list = cf.corner_analysis()

        aruco_locs = []

        for id_c in c_list:
            pdetect = PoseDetector(id_c, self.mtx, self.dist, self.marker_side_dims, 1)
            ar_loc = pdetect.find_marker_locations()
            aruco_locs.append(ar_loc)

        return aruco_locs
