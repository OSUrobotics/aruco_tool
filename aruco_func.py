import cv2
from cv2 import aruco
import pdb
import pandas as pd
import numpy as np
from corner_finder import CornerFinder
from aruco_corner import ArucoCorner
from pose_detector import PoseDetector
from aruco_loc import ArucoLoc

class ArucoFunc:
    """
    Class which holds aruco corner analysis functions (holistic functions, they include everything for easy start)
    """
    def __init__(self, mtx=None, dist=None):
        """ 
        Input camera settings for aruco analysis
        """

        # camera calibration
        if mtx is None:
            self.mtx = np.array(((617.0026849655, -0.153855356, 315.5900337131),  # fx, s,cx
                                (0, 614.4461785395, 243.0005874753),  # 0,fy,cy
                                (0, 0, 1)))
        else:
            self.mtx = mtx
        
        if dist is None:
            # k1,k2,p1,p2 ie radial dist and tangential dist
            self.dist = np.array((0.1611730644, -0.3392379107, 0.0010744837, 0.000905697))
        else:
            self.dist = dist
        
        # TODO: add a full and single image analysis for multiple ids

    def load_corners(self, file_loc):
        """
        Loads corner data that was saved as a csv previously, returns an ArucoCorner obj with imported data
        """
        pass


    def load_poses(self, file_loc, id):
        """
        Loads pose data that was saved as a csv previously, returns an ArucoLoc obj with imported data
        """
        df = pd.read_csv(file_loc)
        
        # convert dataframe to numpy array
        data = df.to_numpy()

        return ArucoLoc(id, data)


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

        pdetect = PoseDetector(id_c, self.mtx, self.dist, 0.03, 1)
        return pdetect.calc_poses()


    def single_image_analysis_single_id(self, file_loc, desired_id=None):
        """ 
        Analyzes a single image for a single aruco code, returns the pose
        """
        ar_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
        ar_params = aruco.DetectorParameters_create()

        cf = CornerFinder("")
        c_data = cf._analyze_single_image("tests/img_single.jpg", ar_dict, ar_params)
        print(c_data[desired_id])
        ac = ArucoCorner(0, c_data[desired_id])
        pdetect = PoseDetector(ac, self.mtx, self.dist, 0.03, 1)
        return pdetect._calc_single_pose(ac.corners)


if __name__ == "__main__":
    ar = ArucoFunc()
    print( ar.full_analysis_single_id("tests/stream_appear", 1) )
    #print( ar.single_image_analysis_single_id("tests/img_single.jpg", 2) )