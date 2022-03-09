import os 
import cv2
import numpy as np
from pathlib import Path
from cv2 import aruco
import pdb
from .aruco_corner import ArucoCorner


class CornerFinder:
    """
    Takes a set of images and finds the ARuCo tag corners in the image. Will generate ArucoCode objects to store data.
    Just point it to data, give it ids to care about, then it will do its thing
    """
    def __init__(self, folder_loc, data_name=None, ar_dict=None, ar_params=None, desired_ids=None):
        """
        Analyzes for aruco corners in the folder that you point to. Outputs data in ArucoCorner object form, one for each aruco id detected
        """
        self.home_directory = Path(__file__).parent.absolute()
        self.data_folder = folder_loc
        self.data_name = data_name
        self.corner_data = None
        self.aruco_dict = ar_dict
        self.aruco_params = ar_params
        self.desired_ids = desired_ids

        # TODO: need to add processing frequency too?


    def corner_analysis(self):
        """
        Returns set of ArucoCorner objects that store data for each id detected in the data stream 
        """
        all_corners = self._find_corners(desired_ids=self.desired_ids)
        self.corner_data = all_corners

        # now we will separate the corner data into ArucoCorner objects
        return self._separate_corners(data_name=self.data_name)


    def _separate_corners(self, data_name=None):
        """
        Package each id into its own ArucoCorner object
        """
        corners_separated = []
        for k in self.corner_data:
            c_data = self.corner_data[k]

            c_obj = ArucoCorner(k, c_data, data_attributes=data_name, file_folder=self.data_folder) # TODO: for now, handled as a string. Later, handle as a dict
            corners_separated.append(c_obj)

        return corners_separated


    def _find_corners(self, desired_ids=None):
        """
        Analyzes a set of images and finds the corners 
        """
        if self.aruco_dict is None:
            ar_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

        if self.aruco_params is None:
            ar_params = aruco.DetectorParameters_create()

        img_names = self._get_image_files()
        num_imgs = len(img_names)

        # store all data here
        stream_data = dict()

        # predefine the size of the dictionary based on desired ids
        if desired_ids:
            for id in desired_ids:
                stream_data[id] = np.full((num_imgs, 4, 2), np.nan) # make predefined dictionary full of nan values
        
        # otherwise, analyze the first image, grab the ids it finds in the first image, and predefine based on that
        # if an id appears later, we will add it to the stream_data dict manually, with np.nan values for all previous images
        elif desired_ids is None:
            first_img = self._analyze_single_image(f"{self.data_folder}/{img_names[0]}", ar_dict, ar_params)

            for id in first_img.keys():
                stream_data[id] = np.full((num_imgs, 4, 2), np.nan) # make predefined dictionary full of nan values


        for j, im in enumerate(img_names):
            im_data = self._analyze_single_image(f"{self.data_folder}/{im}", ar_dict, ar_params, desired_ids=desired_ids)

            if im_data is not None:
                for k in im_data.keys():

                    if k not in stream_data.keys():
                        back_list = np.full((num_imgs, 4, 2), np.nan)
                        stream_data[k] = back_list

                    stream_data[k][j] = im_data[k]

        return stream_data


    def _get_image_files(self, idx_limit=None, idx_bot=0):
        """
        Retrieve list of image names, sorted. Grabs all jpg files and sorts them, so its strongly recommended that image naming scheme adheres to sort function
        """
        # TODO: be smarter about indices. If bot != 0, then bot-1 | if idx_limit != len(files), then lim + 1
        os.chdir(self.data_folder)
        files = [f for f in os.listdir('.') if f[-3:] == 'jpg']
        files.sort()

        #print(f"Num of image files in folder: {len(files)}")
        if idx_limit is not None:
            if idx_bot != 0:
                idx_bot = idx_bot-1  # this is so that we can include idx_bot

            if idx_limit != len(files):  # so that we can include idx_limit
                idx_limit = idx_limit + 1

            try:
                files = files[idx_bot:idx_limit]

            except Exception as e:
                print("get_images error: ")
                print(e)

        # change directory so we can continue in terminal
        os.chdir(self.home_directory)

        return files


    def _analyze_single_image(self, file_name, ar_dict, ar_params, desired_ids=None):
        """
        Analyzes a single image... 
        """
        img = cv2.imread(file_name)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        bboxs, ids, rejected = aruco.detectMarkers(gray, ar_dict, parameters = ar_params)

        id_data = dict()
        for id, box in zip(ids, bboxs):
            if desired_ids is not None and id in desired_ids:
                id_data[id[0]] = box[0]
            if desired_ids is None:
                id_data[id[0]] = box[0]

        # double check that all desired ids are accounted for
        if desired_ids is not None:
            for idd in desired_ids:
                if idd not in id_data.keys():
                    id_data[idd] = np.array([[np.nan, np.nan], [np.nan, np.nan], [np.nan, np.nan], [np.nan, np.nan]])
        
        # if it doesn't find any desired ids, return None
        # if not id_data:
        #     id_data = None

        return id_data

if __name__ == "__main__":
    t1 = CornerFinder("tests/stream_appear/")
    data = t1._find_corners()
    print(data[0])