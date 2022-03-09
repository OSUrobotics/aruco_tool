

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
        self.file_loc = file_folder # location of the data, if none, it will do it in the current location

        self.poses = poses
        self.data_len = len(poses)
        #self.corners_df = self.get_corners_df(corners)

