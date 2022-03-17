

from aruco_tool import load_corners, load_poses


def test_import_corners():
    """
    Test that aruco corner object is created well on import
    """
    ar_corner = load_corners("test_corners_id3.csv", 3)

    assert ar_corner.id == 3
    assert ar_corner.data_len == 6


def test_import_poses():
    """
    Test that aruco pose object is created well on import 
    """
    ar_loc = load_poses("test_poses_id3.csv", 3)

    assert ar_loc.id == 3
    assert ar_loc.data_len == 6
