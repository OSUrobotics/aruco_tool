import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pdb

class ArucoLoc:
    """
    Object which holds pose data for a specific aruco tag id
    """
    
    def __init__(self, id_num, poses, data_attributes=None, file_folder=None):
        """ 
        Creates the object. 
        """
        # TODO: add aruco dictionary and params to this, so pose_detector can use it later
        self.id = id_num
        self.name = data_attributes  # TODO: a dictionary that contains the relevant name data -> since different projects will have different attributes for the data
        self.folder_loc = file_folder # location of the data, if none, it will do it in the current location

        self.poses = poses
        self.data_len = len(poses)
        #self.corners_df = self.get_corners_df(corners)


    def yield_poses(self):
        """
        Yields each row of poses, as a numpy array 
        """
        # TODO: skip rows of all nans?
        for i, r in enumerate(self.poses):
            yield i, r


    def gen_poses_df(self):
        """
        Generates pandas dataframe of data 
        """
        return pd.DataFrame(self.poses, columns=["x","y","z","tmag","roll","pitch","yaw","rmag"]) # TODO: double check again that order is correct


    def save_poses(self, file_name_overwrite=None):
        """
        Saves data as a dataframe. 
        """
        data = self.gen_poses_df()

        if file_name_overwrite is None:
            file_name = f"{self.id}_ar_poses_{self.folder_loc.replace('/', '_')}"
            new_file_name = file_name + ".csv"

        else:
            new_file_name = file_name_overwrite + ".csv"

        data.to_csv(new_file_name, index=True)
        # print(f"CSV File generated with name: {new_file_name}")


    def get_init_pose(self):
        """ 
        """
        pass


    def filter_corners(self, window_size=10):
        """
        Overwrite the corner data with filtered version
        """
        self.poses = self._moving_average(window_size)


    def _moving_average(self, window_size=10):
        """
        Runs a moving average on the data, using the pandas df method.
        """
        poses = self.poses
         # what we want to do is remove any nans at the end of a file (if the id disapeared), run the moving average, and then add them back - the moving average function overwrites nan's at the end of a data stream
        for i in range(self.data_len-1, 0, -1):
            # looking for when the rows stop being all nan values, if there are any
            if not np.all(np.isnan(poses[i, :])):
                data_stop = i
                break

        if data_stop == self.data_len-1: # if there were no nan rows at the end, just carry on...
            actual_data = poses
            data_cut = None
        else: # ...otherwise actually cut the data
            data_cut = self.data_len - data_stop + 1
            actual_data = poses[0:data_cut, :]

        actual_df = pd.DataFrame(actual_data, columns=["x1","y1","x2","y2","x3","y3","x4","y4"])

        # I convert to dataframes because the pandas implementation for moving average is exactly what I need
        filtered_df = pd.DataFrame()
        filtered_df["frame"] = actual_df.index

        filtered_df["x"] = actual_df["x"].rolling(
            window=window_size, min_periods=1).mean()
        filtered_df["y"] = actual_df["y"].rolling(
            window=window_size, min_periods=1).mean()
        filtered_df["z"] = actual_df["z"].rolling(
            window=window_size, min_periods=1).mean()
        filtered_df["tmag"] = actual_df["tmag"].rolling(
            window=window_size, min_periods=1).mean()

        filtered_df["roll"] = actual_df["roll"].rolling(
            window=window_size, min_periods=1).mean()
        filtered_df["pitch"] = actual_df["pitch"].rolling(
            window=window_size, min_periods=1).mean()
        filtered_df["yaw"] = actual_df["yaw"].rolling(
            window=window_size, min_periods=1).mean()
        filtered_df["rmag"] = actual_df["rmag"].rolling(
            window=window_size, min_periods=1).mean()

        filtered_df = filtered_df.round(4)
        filtered_df = filtered_df.set_index("frame")

        # ok, cut back to numpy array and add the rows of nan back
        filtered_data = filtered_df.to_numpy()

        if data_cut is not None:
            # if we cut before, now we should add back the nan rows!
            full_filtered_data = np.full((6,8), np.nan)
            full_filtered_data[0:data_cut, :] = filtered_data
        else:
            full_filtered_data = filtered_data

        return full_filtered_data


    def plot_trajectory(self):
        """
        Plots translation data (x, y)
        """
        poses = self.gen_poses_df()
        plt.plot(poses['x'], poses['y'])




