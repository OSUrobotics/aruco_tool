

class ArucoCorner:
    """
    Object which holds corner data for a specific aruco tag id
    """
    
    def __init__(self, id_num, corners, data_attributes=None, file_folder=None):
        """ 

        """
        self.id = id_num
        self.name = data_attributes  # TODO: a dictionary that contains the relevant name data -> since different projects will have different attributes for the data
        self.file_loc = file_folder # location of the data, if none, it will do it in the current location

        self.corners = corners

    def get_corners_df():
        """
        Return corner data as a dataframe. Columns: x1, y1, x2, y2, ...
        """
        pass

    def save_corner_data():
        """
        Save corner data, in dataframe form (for starters)
        """
        pass

    def compute_poses(self):
        """
        Take the corner data stored on the object and convert it to poses 
        """
        pass