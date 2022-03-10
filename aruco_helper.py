import cv2

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
        cv2.imshow("test", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    ArucoHelper.show_image("tests/img_single.jpg")
