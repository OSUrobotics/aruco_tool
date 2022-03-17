

from aruco_tool import ArucoFunc
from pathlib import Path


def test_single_image_analysis():
    """
    Tests single image analysis, finds all codes 
    """
    af = ArucoFunc()
    file = str(Path(__file__).parent.resolve() / "img_single.jpg")
    a_loc_list = af.single_image_analysis(file)

    assert len(a_loc_list) == 1

    file2 = str(Path(__file__).parent.resolve() / "img_mult.jpg")
    a_loc_list2 = af.single_image_analysis(file2)

    assert len(a_loc_list2) == 4


def test_full_image_analysis():
    """
    Tests full image analysis on a data stream, finds all codes 
    """
    af = ArucoFunc()
    folder = str(Path(__file__).parent.resolve() / "stream_simple/")
    a_loc_list = af.full_analysis(folder)

    assert len(a_loc_list) == 1

    folder2 = str(Path(__file__).parent.resolve() / "stream_mult/")
    a_loc_list2 = af.full_analysis(folder2)

    assert len(a_loc_list2) == 3
    assert a_loc_list2[0].data_len == 6

