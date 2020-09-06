from closest_top import *


def test_calculate_base_index():
    # given
    test_data_list = [
        (np.array([0, 0, 0]), 100, np.array([0, 0, 0])),
        (np.array([101, 0, 0]), 100, np.array([100, 0, 0])),
        (np.array([101, 0, 0]), 50, np.array([100, 0, 0])),
        (np.array([0, 101, 0]), 100, np.array([0, 100, 0])),
        (np.array([0, 0, 101]), 100, np.array([0, 0, 100])),
        (np.array([101, 0, 101]), 100, np.array([100, 0, 100])),
        (np.array([201, 0, 201]), 100, np.array([200, 0, 200])),
        (np.array([-1, 0, 0]), 100, np.array([-100, 0, 0])),
        (np.array([-1, -1, 0]), 100, np.array([-100, -100, 0])),
        (np.array([-101, -101, 0]), 100, np.array([-200, -200, 0])),
    ]
    for xyz, chunk_size, expected_index in test_data_list:
        print(xyz, chunk_size, expected_index)
        # when
        index = calculate_base_index(xyz, chunk_size)
        # then
        np.testing.assert_array_equal(index, expected_index)


def test_calculate_indexes_for_level():
    # given
    test_data_list = [
        (np.array([0, 0, 0]), 0, 100),
        (np.array([0, 0, 0]), 1, 100),
        (np.array([0, 0, 0]), 2, 100),
        (np.array([0, 0, 0]), 3, 100),
    ]
    for base_index, level, chunk_size in test_data_list:
        print(base_index, level, chunk_size)
        # when
        indexes = calculate_indexes_for_level(base_index, level, chunk_size)
        # then
        assert len(indexes) == (level * 2 + 1)**3 - ((level - 1) * 2 + 1)**3 if level > 0 else 1

        if level > 0:
            level_lower_indexes = calculate_indexes_for_level(base_index, level - 1, chunk_size)
            for index in indexes:
                # See https://stackoverflow.com/questions/33217660/checking-if-a-numpy-array-contains-another-array
                assert (index == level_lower_indexes).all(axis=1).any() == False


def test_calculate_closest_top():
    # given
    test_data_list = [
        (np.array([0, 0, 0]), [np.array([1, 0, 0]), np.array([2, 0, 0])], np.array([1, 0, 0])),
        (np.array([0, 0, 0]), [np.array([2, 0, 0]), np.array([1, 0, 0])], np.array([1, 0, 0])),
        (np.array([0, 0, 0]), [np.array([2, 0, 0]), np.array([-1, 0, 0])], np.array([-1, 0, 0])),
        (np.array([0, 0, 0]), [], None),
    ]
    for xyz, tops, expected_closest_top in test_data_list:
        print(xyz, tops, expected_closest_top)
        # when 
        closest_top = calculate_closest_top(xyz, tops)
        # then
        np.testing.assert_array_equal(closest_top, expected_closest_top)


def test_calculate_distance():
    # given
    a = np.array([3, 0, 0])
    b = np.array([0, 4, 0])
    expected_distance = 5
    # when
    distance = calculate_distance(a, b)
    # then
    assert distance == expected_distance


def test_swap_closest_top():
    # given
    test_data_list = [
        (np.array([1, 0, 0]), np.array([2, 0, 0]), np.array([0, 0, 0]), np.array([1, 0, 0])),
        (np.array([2, 0, 0]), np.array([1, 0, 0]), np.array([0, 0, 0]), np.array([1, 0, 0])),
        (None, np.array([1, 0, 0]), np.array([0, 0, 0]), np.array([1, 0, 0])),
        (np.array([1, 0, 0]), None, np.array([0, 0, 0]), np.array([1, 0, 0])),
        (None, None, np.array([0, 0, 0]), None),
    ]
    for new_top, previous_top, xyz, expected_closest_top in test_data_list:
        print(new_top, previous_top, xyz, expected_closest_top)
        # when 
        closest_top = swap_closest_top(new_top, previous_top, xyz)
        # then
        np.testing.assert_array_equal(closest_top, expected_closest_top)

def test_should_return_closest_top():
    # given
    test_data_list = [
        (np.array([21, 20, 20]), np.array([20, 20, 20]), 0, 100, True),
        (None, np.array([20, 20, 20]), 0, 100, False),
        (np.array([20, 20, 20]), np.array([5, 5, 5]), 0, 100, False),
        (np.array([20, 20, 20]), np.array([5, 5, 5]), 1, 100, True),
    ]
    for closest_top, xyz, level, chunk_size, expected_should_return in test_data_list:
        print(closest_top, xyz, level, chunk_size, expected_should_return)
        # when
        should_return = should_return_closest_top(closest_top, xyz, level, chunk_size)
        # then
        assert should_return == expected_should_return


def test_calculate_shortest_distance_to_the_edge():
    # given
    test_data_list = [
        (np.array([1, 20, 20]), 0, 50, 1),
        (np.array([1, 20, 20]), 1, 50, 51),
        (np.array([1, 20, 20]), 2, 50, 101),
        (np.array([1, 20, 20]), 0, 100, 1),
        (np.array([20, 1, 20]), 0, 50, 1),
        (np.array([20, 20, 1]), 0, 50, 1),
        (np.array([101, 120, 120]), 0, 50, 1),
        (np.array([-1, 20, 20]), 0, 50, 1),
        (np.array([20, -1, 20]), 0, 50, 1),
        (np.array([20, 20, -1]), 0, 50, 1),
        (np.array([-1, -20, -20]), 0, 50, 1),
        (np.array([-20, -49, -20]), 0, 50, 1),
        (np.array([-20, -149, -20]), 0, 50, 1),
    ]
    for xyz, level, chunk_size, expected_distance in test_data_list:
        print(xyz, level, chunk_size, expected_distance)
        # when 
        distance = calculate_shortest_distance_to_the_edge(xyz, level, chunk_size)
        # then
        assert distance == expected_distance


def test_convert_xyz_to_latlong():
    # given
    xyz = np.array([6371000000, 0, 0])
    # when
    latitude, longitude = convert_xyz_to_latlong(xyz)
    # then
    assert type(latitude) == float
    assert type(longitude) == float
    assert latitude == 0.0
    assert longitude == 0.0
