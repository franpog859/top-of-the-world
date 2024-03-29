from calculate_tops import *

def test_project_onto_line():
    # given
    test_data_list = [
        (XYZ(1, 1, 1), XYZ(0, 0, 0), XYZ(1, 0, 0), XYZ(1, 0, 0)),
        (XYZ(-1, 1, 1), XYZ(0, 0, 0), XYZ(1, 0, 0), XYZ(-1, 0, 0)),
        (XYZ(1, 1, 1), XYZ(0, 0, 0), XYZ(1, 1, 1), XYZ(1, 1, 1)),
        (XYZ(1, 1, 1), XYZ(0, 0, 0), XYZ(1, 0, 1), XYZ(1, 0, 1)),
        (XYZ(1, 1, 1), XYZ(1, 0, 0), XYZ(0, 0, 0), XYZ(1, 0, 0)),
        (XYZ(-1, 1, 1), XYZ(-1, 0, 0), XYZ(0, 0, 0), XYZ(-1, 0, 0)),
        (XYZ(1, 1, 1), XYZ(1, 1, 1), XYZ(0, 0, 0), XYZ(1, 1, 1)),
    ]
    for xyz, a, b, expected_projection in test_data_list:
        # when
        projection = xyz.project_onto_line(a, b)
        # then
        assert projection == expected_projection


def test_filter_only_tops():
    # given
    test_data_list = [
        (XYZ(3, 3, 0), True),
        (XYZ(1, 4, 0), True),
        (XYZ(1, 4, 0), False),
        (XYZ(4, 1, 0), True),
        (XYZ(-5, -5, 0), True),
        (XYZ(0, 0, 1), True),
        (XYZ(3, 1, 0), False),
        (XYZ(1, 1, 0), False),
        (XYZ(-1, -2, 0), False),
        (XYZ(3, 2, 0), False),
    ]
    points = [data[0] for data in test_data_list]
    expected_tops = [data[0] for data in test_data_list if data[1]]
    # when
    tops = filter_only_tops(points)
    # then
    assert tops == expected_tops


def test_get_top_for_direction():
    # given
    test_data_list = [
        (XYZ(3, 3, 0), XYZ(3, 3, 0)),
        (XYZ(1, 4, 0), XYZ(1, 4, 0)),
        (XYZ(4, 1, 0), XYZ(4, 1, 0)),
        (XYZ(3, 1, 0), XYZ(4, 1, 0)),
        (XYZ(-5, -5, 0), XYZ(-5, -5, 0)),
    ]
    xyz_list = [test_data[0] for test_data in test_data_list]
    for direction, expected_top in test_data_list:
        # when
        top = get_top_for_direction(direction, xyz_list)
        # then
        assert top == expected_top


def test_are_on_the_same_side_relative_to_center():
    # given
    test_data_list = [
        (XYZ(1, 1, 1), XYZ(1, 1, 1), True),
        (XYZ(1, 1, 1), XYZ(-1, -1, -1), False),
        (XYZ(1, 1, 1), XYZ(2, 2, 2), True),
        (XYZ(-1, -1, -1), XYZ(-2, -2, -2), True),
        (XYZ(-1, -1, -1), XYZ(1, 1, 1), False),
        (XYZ(0, 0, 1), XYZ(0, 0, 2), True),
        (XYZ(0, 0, 1), XYZ(0, 0, -2), False),
        (XYZ(0, 1, 0), XYZ(0, 2, 0), True),
        (XYZ(0, 1, 0), XYZ(0, -2, 0), False),
    ]
    for a, b, expected_result in test_data_list:
        # when
        result = are_on_the_same_side_relative_to_center(a, b)
        # then
        assert result == expected_result


def test_convert_tops_to_dto():
    # given
    chunk_size = 1000
    test_top_list = [
        XYZ(1001, 2001, 4000),
        XYZ(1006, 2001, 4999),
        XYZ(-1001, -2999, -4000),
    ]
    expected_dto = [
        {
            'index': {
                'x': 1000,
                'y': 2000,
                'z': 4000,
            },
            'tops': [
                {
                   'x': 1001,
                   'y': 2001,
                   'z': 4000,
                },
                {
                   'x': 1006,
                   'y': 2001,
                   'z': 4999,
                }
            ]
        },
        {
            'index': {
                'x': -2000,
                'y': -3000,
                'z': -4000,
            },
            'tops': [
                {
                   'x': -1001,
                   'y': -2999,
                   'z': -4000,
                }
            ]
        },
    ]
    # when
    dto = convert_tops_to_dto(test_top_list, chunk_size)
    # then
    assert dto == expected_dto
