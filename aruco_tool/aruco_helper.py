import cv2
from cv2 import aruco
import pdb
from corner_finder import CornerFinder

class ArucoHelper:
    """
    Helper class with static functions designed to help a user review or debug images with aruco data 
    """

    @staticmethod
    def view_data_video(acode, include_corners=False, include_pose=False):
        """
        Shows image stream as a video. Useful for debugging. 
        """
        pass 

    @staticmethod
    def show_image(file_loc, include_corners=False):
        """
        Show an image 
        """
        img = cv2.imread(file_loc, cv2.IMREAD_COLOR)

        if include_corners:
            ar_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
            ar_params = aruco.DetectorParameters_create()

            cf = CornerFinder("")
            c_data = cf._analyze_single_image("tests/img_single.jpg", ar_dict, ar_params)

            for k in c_data.keys():
                pdb.set_trace()
                up_left = c_data[k][0]
                down_right = c_data[k][3]

                cv2.rectangle(img, pt1=(200,200), pt2=(300,300), color=(0,0,255), thickness=-1)
                

        img = cv2.imread(file_loc, cv2.IMREAD_COLOR)
        cv2.imshow("test", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    ArucoHelper.show_image("tests/img_single.jpg", include_corners=True)
