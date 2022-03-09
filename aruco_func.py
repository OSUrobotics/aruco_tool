import cv2

class ArucoFunc:
    """
    Class which holds aruco corner analysis functions and settings
    """
    def __init__(self, mtx=None, dist=None):
        """ 
        Input camera settings for aruco analysis
        """

        # camera calibration
        if mtx is None:
            self.mtx = np.array(((617.0026849655, -0.153855356, 315.5900337131),  # fx, s,cx
                                (0, 614.4461785395, 243.0005874753),  # 0,fy,cy
                                (0, 0, 1)))
        else:
            self.mtx = mtx
        
        if dist is None:
            # k1,k2,p1,p2 ie radial dist and tangential dist
            self.dist = np.array((0.1611730644, -0.3392379107, 0.0010744837, 0.000905697))
        else:
            self.dist = dist

    def single_image_analysis(file_loc, desired_ids=None):
        """ 
        Analyzes a single image for corners
        """
        image = cv2.imread(f)

        # make image black and white
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # get estimated aruco pose
        corners, ids, _ = aruco.detectMarkers(image=image_gray, dictionary=aruco_dict,
                                                parameters=aruco_params, cameraMatrix=self.mtx,
                                                distCoeff=self.dist)


        print(ids)
        if desired_ids is None:
            desired_ids = ids

        for idx, id in enumerate(ids):
            if id in desired_ids:
                pass



        # print(ids)
        try:  # TODO: need to redo this for aruco_tool
            if 2 not in ids:
                print(ids)
                print("FOUND WRONG ARUCO CODE, CANT FIND CORRECT ONE")
                raise ValueError("Did not find correct aruco code.")

            if len(ids) > 1:
                # TODO: so this works, but maybe add some better tracking of this by considering ids and their index
                print(f"More than one aruco tag found at frame {i}!")
                corners = corners[0]

            c = corners[0].squeeze()

        except Exception as e:
            print(f"Failed to find an aruco code at frame {i}!")
            print(e)
            # make corners of None to make sure that we log the failed attempt to find aruco code
            c = np.array([[None, None], [None, None], [None, None], [None, None]])
            # pdb.set_trace()

