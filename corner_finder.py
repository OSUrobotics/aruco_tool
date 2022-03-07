import os 

class CornerFinder:
    """
    Takes a set of images and finds the ARuCo tag corners in the image. Will generate ArucoCode objects to store data.
    Just point it to data, give it ids to care about, then it will do its thing
    """
    def __init__(self, folder_loc):
        self.data_folder = folder_loc


    def find_corners(self):
        """
        Analyzes a set of images and finds the corners 
        """
        pass


    def _get_image_files(self, idx_limit=None, idx_bot=0):
        """
        Retrieve list of image names, sorted.
        """
        # TODO: be smarter about indices. If bot != 0, then bot-1 | if idx_limit != len(files), then lim + 1
        os.chdir(self.data_folder)
        files = [f for f in os.listdir('.') if f[-3:] == 'jpg']
        files.sort()

        #print(f"Num of image files in folder: {len(files)}")
        if idx_limit is not None:
            if idx_bot != 0:
                idx_bot = idx_bot-1  # this is so that we can include idx_bot

            if idx_limit != len(files):  # so that we can include idx_limit
                idx_limit = idx_limit + 1

            try:
                files = files[idx_bot:idx_limit]

            except Exception as e:
                print("get_images error: ")
                print(e)

        return files


    def _analyze_single_image(self, file_name, ar_dict, ar_params, desired_ids=None):
        """
        Analyzes a single image... 
        """
        img = cv2.imread(file_name)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        bboxs, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters = aruco_params)

        id_data = dict()
        for id, box in zip(ids, bboxs):
            if desired_ids is not None and id in desired_ids:
                id_data[id[0]] = box[0]

        # double check that all desired ids are accounted for
        for idd in desired_ids:
            if idd not in id_data.keys():
                id_data[idd] = np.array([[np.nan, np.nan], [np.nan, np.nan], [np.nan, np.nan], [np.nan, np.nan]])
        
        # if it doesn't find any desired ids, return None
        if not id_data:
            id_data = None

        return id_data

