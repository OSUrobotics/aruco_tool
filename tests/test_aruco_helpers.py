

from aruco_tool import load_corners, load_poses
import pandas as pd
import numpy as np
from pathlib import Path


def test_import_corners():
    """
    Test that aruco corner object is created well on import
    """
    file = str(Path(__file__).parent.resolve() / "test_corners_id3.csv")
    ar_corner = load_corners(file, 3)

    assert ar_corner.id == 3
    assert ar_corner.data_len == 6


def test_import_poses():
    """
    Test that aruco pose object is created well on import 
    """
    file = str(Path(__file__).parent.resolve() / "test_poses_id3.csv")
    ar_loc = load_poses(file, 3)

    assert ar_loc.id == 3
    assert ar_loc.data_len == 6
