

class ArucoCode:
    """
    Object which stores the data for one ARuCo tag in a series of images
    """
    
    def __init__(self, id_num, data_attributes, file_folder=None):
        """ 

        """
        self.id = id_num
        self.name = data_attributes  # TODO: a dictionary that contains the relevant name data -> since different projects will have different attributes for the data
        self.file_loc = file_folder # location of the data, if none, it will do it in the current location

        self.corners = None  # TODO: maybe it should be an empty pandas dataframe? So I can add things to the dataframe easily?
        self.poses = None

    def compute_poses(self):
        """
        Take the corner data stored on the object and convert it to poses 
        """
        pass