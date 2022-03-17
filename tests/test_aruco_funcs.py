

from aruco_tool import ArucoFunc


def test_single_image_analysis():
    """
    Tests single image analysis, finds all codes 
    """
    af = ArucoFunc()
    a_loc_list = af.single_image_analysis("img_single.jpg")

    assert len(a_loc_list) == 1

    a_loc_list2 = af.single_image_analysis("img_mult.jpg")

    assert len(a_loc_list2) == 4


def test_full_image_analysis():
    """
    Tests full image analysis on a data stream, finds all codes 
    """
    af = ArucoFunc()
    a_loc_list = af.full_analysis("stream_simple")

    assert len(a_loc_list) == 1

    a_loc_list2 = af.full_analysis("stream_mult")

    assert len(a_loc_list2) == 3
    assert a_loc_list2[0].data_len == 6

