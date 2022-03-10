import cv2
from cv2 import aruco
import pdb
from .corner_finder import CornerFinder
from .aruco_corner import ArucoCorner
from .aruco_loc import ArucoLoc

class ArucoHelper:
    """
    Helper class with static functions designed to help a user review or debug images with aruco data 
    """

    @staticmethod()
    def load_corners(self, file_loc):
        """
        Loads corner data that was saved as a csv previously, returns an ArucoCorner obj with imported data
        """
        pass


    @staticmethod()
    def load_poses(self, file_loc, id):
        """
        Loads pose data that was saved as a csv previously, returns an ArucoLoc obj with imported data
        """
        df = pd.read_csv(file_loc)  # TODO: should I parse the file_loc for information like id and folder loc?
        
        # convert dataframe to numpy array
        data = df.to_numpy()

        return ArucoLoc(id, data)


    @staticmethod
    def view_data_video(acode, include_corners=False, include_pose=False):
        """
        Shows image stream as a video. Useful for debugging. 
        """
        pass


    @staticmethod
    def show_image(file_loc, include_corners=False, marker_size=3):
        """
        Show an image 
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

                    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), -1)
                
        cv2.imshow(f"{file_loc}", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


