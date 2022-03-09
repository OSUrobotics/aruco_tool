import pandas as pd
import numpy as np


class ArucoCorner:
    """
    Object which holds corner data for a specific aruco tag id
    """
    
    def __init__(self, id_num, corners, data_attributes=None, file_folder=None):
        """ 
        Creates the object. Will also save the data as a pandas dataframe
        """
        self.id = id_num
        self.name = data_attributes  # TODO: a dictionary that contains the relevant name data -> since different projects will have different attributes for the data
        self.file_loc = file_folder # location of the data, if none, it will do it in the current location

        self.corners = corners
        #self.corners_df = self.get_corners_df(corners)

    
    def reshape_corners(self):
        return self.corners.reshape(6, 8)


    def gen_corners_df(self):
        """
        Return corner data as a dataframe. Columns: x1, y1, ..., x4, y4
        """
        reshaped_c = self.reshape_corners()
        return pd.DataFrame(reshaped_c, columns=["x1","y1","x2","y2","x3","y3","x4","y4"])


    def yield_corners(self):
        """
        Yields the corners for each row, as numpy array
        """
        for r in self.corners:
            yield r


    # def moving_average(self, window_size=3):
    #     """
    #     Runs a moving average on the data 
    #     """
    #     # TODO: numpy doesn't work how I want it to, pandas has how I want it to but it eliminates all the nan values...
    #     corners = self.reshape_corners()
    #     kernel_size = window_size
    #     kernel = np.ones(kernel_size) / kernel_size
    #     #d = list(range(1, len(corned))) + list(range(len(corned), 0, -1))

    #     cm = np.convolve(corners, kernel, 'same')
    #     return cm
    #     # mask = np.all(np.isnan(cm), axis=1)
    #     # return cm[~mask]


    def save_corners(self, file_name_overwrite=None):
        """
        Saves pose data as a new csv file
        :param file_name_overwrite: optional parameter, will save as generate_name unless a different name is specified
        """
        data = self.gen_corners_df()

        if file_name_overwrite is None:
            file_name = f"{self.id}_corners_{self.file_loc.replace('/', '_')}"
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

    def _moving_average(self, window_size=3):
        """
        Runs a moving average on the corner data. Saves moving average data into new columns with f_ prefix.
        Overwrites previous moving average calculations.
        :param window_size: size of moving average. Defaults to 3.
        """
        # TODO: makes a bunch of nan values at end of data
        corners = self.gen_corners_df()

        filtered_df = pd.DataFrame()
        filtered_df["frame"] = corners.index

        filtered_df["x1"] = corners["x1"].rolling(
            window=window_size, min_periods=1).mean()
        filtered_df["y1"] = corners["y1"].rolling(
            window=window_size, min_periods=1).mean()

        filtered_df["x2"] = corners["x2"].rolling(
            window=window_size, min_periods=1).mean()
        filtered_df["y2"] = corners["y2"].rolling(
            window=window_size, min_periods=1).mean()

        filtered_df["x3"] = corners["x3"].rolling(
            window=window_size, min_periods=1).mean()
        filtered_df["y3"] = corners["y3"].rolling(
            window=window_size, min_periods=1).mean()

        filtered_df["x4"] = corners["x4"].rolling(
            window=window_size, min_periods=1).mean()
        filtered_df["y4"] = corners["y4"].rolling(
            window=window_size, min_periods=1).mean()

        filtered_df = filtered_df.round(4)
        filtered_df = filtered_df.set_index("frame")

        return filtered_df.to_numpy()

    # def filter_corners(self, window_size=3):
    #     """
    #     Overwrite the corner data with filtered version
    #     """
    #     self.corners = self._moving_average(window_size)



