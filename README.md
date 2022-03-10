# aruco_tool
Library for using ARuCo tags.

# Installation
## Dependencies
Highly recommend installing these packages separately before pip installing this package.
* **pandas**
* **numpy**
* **cv2** (*need opencv-contrib-python package for aruco*)
* **matplotlib**

## Workflow
Aruco detects corners of the code, then converts that to pose. Right now, the pose is calculated relatively, as a differential from the first pose detected of the id. Will update this with more analysis modes in the future.

When entering file folder locations, please use absolute paths for now.

### Finding corners
```python
    cf = CornerFinder("[Enter Folder with Images Here]")
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
    pdetect = PoseDetector(["1 ArucoCorner object"], ["Camera Calibration"], ["radial and tangential dists"], ["marker side dimensions"], ["processing freq (use 1)"])
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
    af = ArucoFunc(mtx, dist, marker_side_dims)  # stores analysis variables, by default provides my attributes
    
    # run on a single image with one id to track
    pose_array = af.single_image_analysis_single_id(["file location"], desired_id_num)

    # run on a set of images with one id to track
    aruco_loc = af.full_analysis_single_id(["folder location of files"], desired_id_num)

    # run on a single image, track multiple ids or grab all ids in img
    set_of_aruco_locs = af.single_image_analysis(["file location"], desired_ids=None) # if none, grabs all ids in image, otherwise you can specify using a list

    # run on a set of images, track multiple ids or grab all ids in imgs
    set_of_aruco_locs = af.full_analysis(["folder location of files"], desired_ids=None)
```

### Extra Helper Functions
Aruco_tool also provides extra functions for visualization and debugging.
```python
    ArucoHelper.load_poses(["file location"])  # loads csv of pose data into an ArucoLoc object
    ArucoHelper.show_image(["file location"], include_corners=False, marker_size=3)  # shows an image, can choose to show detected corners on the image with the indicated marker size

```

## TODO
TBD