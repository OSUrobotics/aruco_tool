

class ArucoCorner:
    """
    Object which holds corner data for a specific aruco tag id
    """
    
    def __init__(self, id_num, corners, data_attributes, file_folder=None):
        """ 

        """
        self.id = id_num
        self.name = data_attributes  # TODO: a dictionary that contains the relevant name data -> since different projects will have different attributes for the data
        self.file_loc = file_folder # location of the data, if none, it will do it in the current location

        self.corners = corners


    def compute_poses(self):
        """
        Take the corner data stored on the object and convert it to poses 
        """
        pass