# aruco_tool
Library for using ARuCo tags.

## Dependencies
* **pandas**
* **numpy**
* **cv2** (*need opencv-contrib-python package for aruco*)

## Workflow
Aruco detects corners of the code, then converts that to pose. 

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
```

### Converting corner data to pose data
TBD