import cv2
from cv2 import aruco
import pdb
import pandas as pd
import numpy as np
from .corner_finder import CornerFinder
from .aruco_corner import ArucoCorner
from .aruco_loc import ArucoLoc

class ArucoHelper:
    """
    Helper class with static functions designed to help a user review or debug images with aruco data 
    """

    @staticmethod
    def load_corners(file_loc, id):
        """
        Loads corner data that was saved as a csv previously, returns an ArucoCorner obj with imported data
        """
        # import csv
        df = pd.read_csv(file_loc)  # TODO: should I parse the file_loc for information like id and folder loc?

        # get numpy array
        data = df.to_numpy()

        # reformat to aruco-style corners array
        data_len = len(data)

        # can't include the frame number that you get from pandas
        corners = np.reshape(data[:, 1:9], (data_len, 4, 2)) # TODO: need to double check I have right order
        
        return ArucoCorner(id, corners)


    @staticmethod
    def load_poses(file_loc, id):
        """
        Loads pose data that was saved as a csv previously, returns an ArucoLoc obj with imported data
        """
        df = pd.read_csv(file_loc)  # TODO: should I parse the file_loc for information like id and folder loc?
        
        # convert dataframe to numpy array, format is correct
        data = df.to_numpy()

        # reformat to aruco-style corners array
        data_len = len(data)

	    # can't include the frame number that you get from pandas
        poses = data[:, 1:9] # TODO: need to double check I have right order

        return ArucoLoc(id, data)


    @staticmethod
    def show_image(file_loc, include_corners=False, marker_size=3):
        """
        Show an image, can include the detected corners as red squares
        """
        img = cv2.imread(file_loc, cv2.IMREAD_COLOR)

        if include_corners:
            ar_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
            ar_params = aruco.DetectorParameters_create()

            cf = CornerFinder("")
            c_data = cf._analyze_single_image(file_loc, ar_dict, ar_params)

            for k in c_data.keys():

                for cs in c_data[k]:
                    x1 = cs[0]-marker_size
                    y1 = cs[1]+marker_size

                    x2 = cs[0]+marker_size
                    y2 = cs[1]-marker_size

                    # TODO: enable user to set color?
                    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), -1)
                
        cv2.imshow(f"{file_loc}", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    @staticmethod
    def view_data_video(acode, include_corners=False):
        """
        Shows image stream as a video. Useful for debugging. 
        """
        try:
            # get folder location of the aruco code
            folder_loc = acode.folder_loc
        except:
            raise Exception("ArucoCorner object does not have a folder location associated with it")

        pass

        
        

