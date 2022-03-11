# aruco_tool
Library for using ARuCo tags.

# Installation
## Dependencies
Highly recommend installing these packages separately before pip installing this package.
* **pandas**
* **numpy**
* **cv2** (*need opencv-contrib-python package for aruco*)
* **matplotlib**

## Quick-Start Guide
Aruco detects corners of the code, then converts that to pose. Right now, the pose is calculated relatively, as a differential from the first pose detected of the id. Please see documentation for more details.

Will update this with more analysis modes in the future.

When entering file folder locations, please use absolute paths.


### Finding corners
```python
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250) # or another dictionary
    aruco_params = aruco.DetectorParameters_create()
    cf = CornerFinder("absolute/folder/location", ar_dict=aruco_dict, ar_params=aruco_params, data_name="optional label", desired_ids=None)
    ids_found = cf.corner_analysis()
```

Data is stored as numpy arrays in an `ArucoCorner` object. There is one `ArucoCorner` object generated for each aruco code found.
```python
    ac = ids_found[0]

    ac.id  # stores the aruco id number
    ac.folder_loc # stores where the data was collected
    ac.corners # numpy array of corners found
    df = ac.gen_corners_df() # generates a pandas dataframe of the corners
```

### Converting corner data to pose data
```python
    pdetect = PoseDetector(ac (ArucoCorner obj), opencv-camera-calibration, opencv_radial_and_tangential_dists, marker_side_dimensions (float), processing_freq (float, not-used))
    aloc = pdetect.find_marker_locations()

```

Data is stored as numpy arrays in an `ArucoLoc` object. Repeat this process for each `ArucoCorner` object you get from the CornerFinder.
```python
    aloc.id  # stores the aruco id number
    aloc.folder_loc  # stores where the data was collected
    aloc.poses  # numpy array of poses: [x, y, z, magnitude of translation, roll, pitch, yaw, relative magnitude of rotation] -> all relative from initial image
    aloc.gen_poses_df()  # generates a pandas dataframe of the corners
```


### Stream-lined process
Aruco_tool also provides simple, one-line functions for aruco analysis, located in the `ArucoFunc` object. The functions above are mainly designed for sets of images, however these functions provide the ability to selectively run on one image.
```python
    from aruco_tool import ArucoFunc
    af = ArucoFunc(opencv-camera-calibration, opencv_radial_and_tangential_dists, marker_side_dimensions (float))  # stores analysis variables, by default provides my attributes
    
    # run on a single image with one id to track
    pose_array = af.single_image_analysis_single_id("absolute/file/location", desired_id_num)

    # run on a set of images with one id to track
    aruco_loc = af.full_analysis_single_id("absolute/folder/location", desired_id_num)

    # run on a single image, track multiple ids or grab all ids in img
    set_of_aruco_locs = af.single_image_analysis("absolute/file/location", desired_ids=None (list)) # if none, grabs all ids in image, otherwise you can specify using a list

    # run on a set of images, track multiple ids or grab all ids in imgs
    set_of_aruco_locs = af.full_analysis("absolute/folder/location", desired_ids=None (list))
```

### Extra Helper Functions
Aruco_tool also provides extra functions for visualization and debugging. These functions can be imported directly.
```python
    from aruco_tool import load_corners, load_poses, show_image

    a_corner_obj = load_corners("absolute/file/location")
    a_loc_obj = load_poses("absolute/file/location")  # loads csv of pose data into an ArucoLoc object
    show_image(["absolute/file/location", include_corners (bool), marker_size (float))  # shows an image, can choose to show detected corners on the image with the indicated marker size

```

## TODO
TBD