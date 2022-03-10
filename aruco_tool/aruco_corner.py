import pandas as pd
import numpy as np
import pdb


class ArucoCorner:
    """
    Object which holds corner data for a specific aruco tag id
    """
    
    def __init__(self, id_num, corners, data_attributes=None, file_folder=None):
        """ 
        Creates the object
        """
        # TODO: add aruco dictionary and params to this, so pose_detector can use it later
        self.id = id_num
        self.name = data_attributes  # TODO: a dictionary that contains the relevant name data -> since different projects will have different attributes for the data
        self.folder_loc = file_folder # location of the data, if none, it will do it in the current location

        self.corners = corners
        self.data_len = len(corners)
        #self.corners_df = self.get_corners_df(corners)

    
    def reshape_corners(self):
        return self.corners.reshape(self.data_len, 8)


    def gen_corners_df(self):
        """
        Return corner data as a dataframe. Columns: x1, y1, ..., x4, y4
        """
        reshaped_c = self.reshape_corners()
        return pd.DataFrame(reshaped_c, columns=["x1","y1","x2","y2","x3","y3","x4","y4"])


    def yield_corners(self, use_reshaped=True):
        """
        Yields the corners for each row, as numpy array
        """
        if use_reshaped:
            corners_to_use = self.reshape_corners()
        else:
            corners_to_use = self.corners

        for i, r in enumerate(corners_to_use):
            yield i, r


    def get_init_corner(self):
        """
        Gets the first corner that isn't a np.nan value 
        """
        for i, r in enumerate(self.corners):
            if not np.all(np.isnan(r)): # if the row is not all np.nan, then we want it
                return i, r


    def save_corners(self, file_name_overwrite=None):
        """
        Saves pose data as a new csv file
        :param file_name_overwrite: optional parameter, will save as generate_name unless a different name is specified
        """
        data = self.gen_corners_df()

        if file_name_overwrite is None:
            file_name = f"{self.id}_ar_corners_{self.folder_loc.replace('/', '_')}"
            new_file_name = file_name + ".csv"

        else:
            new_file_name = file_name_overwrite + ".csv"

        data.to_csv(new_file_name, index=True)
        # print(f"CSV File generated with name: {new_file_name}")


    # def corner_to_series(self, i, corn):
    #     """
    #     Convert standard numpy array of corners into pd.Series (to add to corners dataframe)
    #     """
    #     c1 = corn[0]
    #     c2 = corn[1]
    #     c3 = corn[2]
    #     c4 = corn[3]
    #     corner_series = pd.Series({"frame": i, "x1": c1[0], "y1": c1[1],
    #                              "x2": c2[0], "y2": c2[1],
    #                              "x3": c3[0], "y3": c3[1],
    #                              "x4": c4[0], "y4": c4[1]})
    #     return corner_series

    # def row_to_corner(self, corn):
    #     """
    #     Convert one row of dataframe into standard corner numpy array
    #     """
    #     i = corn.name
    #     #pdb.set_trace()
    #     c1 = [corn["x1"], corn["y1"]]
    #     c2 = [corn["x2"], corn["y2"]]
    #     c3 = [corn["x3"], corn["y3"]]
    #     c4 = [corn["x4"], corn["y4"]]
    #     return int(i), np.array([c1, c2, c3, c4], dtype=np.dtype("float32"))

    def filter_corners(self, window_size=3):
        """
        Overwrite the corner data with filtered version
        """
        self.corners = self._moving_average(window_size)

    def _moving_average(self, window_size=3):
        """
        Runs a moving average on the corner data. Saves moving average data into new columns with f_ prefix.
        Overwrites previous moving average calculations.
        :param window_size: size of moving average. Defaults to 3.
        """
        corners = self.reshape_corners()

        # what we want to do is remove any nans at the end of a file (if the id disapeared), run the moving average, and then add them back - the moving average function overwrites nan's at the end of a data stream
        for i in range(self.data_len-1, 0, -1):
            # looking for when the rows stop being all nan values, if there are any
            if not np.all(np.isnan(corners[i, :])):
                data_stop = i
                break

        if data_stop == self.data_len-1: # if there were no nan rows at the end, just carry on...
            actual_data = corners
            data_cut = None
        else: # ...otherwise actually cut the data
            data_cut = self.data_len - data_stop + 1
            actual_data = corners[0:data_cut, :]

        actual_df = pd.DataFrame(actual_data, columns=["x1","y1","x2","y2","x3","y3","x4","y4"])

        # I convert to dataframes because the pandas implementation for moving average is exactly what I need
        filtered_df = pd.DataFrame()
        filtered_df["frame"] = actual_df.index

        filtered_df["x1"] = actual_df["x1"].rolling(
            window=window_size, min_periods=1).mean()
        filtered_df["y1"] = actual_df["y1"].rolling(
            window=window_size, min_periods=1).mean()

        filtered_df["x2"] = actual_df["x2"].rolling(
            window=window_size, min_periods=1).mean()
        filtered_df["y2"] = actual_df["y2"].rolling(
            window=window_size, min_periods=1).mean()

        filtered_df["x3"] = actual_df["x3"].rolling(
            window=window_size, min_periods=1).mean()
        filtered_df["y3"] = actual_df["y3"].rolling(
            window=window_size, min_periods=1).mean()

        filtered_df["x4"] = actual_df["x4"].rolling(
            window=window_size, min_periods=1).mean()
        filtered_df["y4"] = actual_df["y4"].rolling(
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


