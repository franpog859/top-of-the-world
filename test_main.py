from main import *


def test_geocoords_to_vectors():
    #given
    lat_long_elev_data = []
    x, y, latitude, longitude, elevation = 1, 1, 0, 0, 0 
    lat_long_elev_data.append((
        x, y, latitude, longitude, elevation
    ))
    x, y, latitude, longitude, elevation = 1, 1, 0, 0, 100
    lat_long_elev_data.append((
        x, y, latitude, longitude, elevation
    ))

    earth_radius_at_equator = 6378137.000000001
    expected_vectors = [
        (1, 1, earth_radius_at_equator, 0, 0),
        (1, 1, earth_radius_at_equator + 100, 0, 0),
    ]

    #when
    vectors = geocoords_to_vectors(lat_long_elev_data)

    #then
    assert vectors == expected_vectors


def test_get_tops_of_the_world():
    #given
    vectors = [
        (1, 1, 90, 0, 0),
        (1, 2, 100, 0, 0),
        (1, 3, 0, 90, 0),
        (1, 4, 0, 100, 0),
        (1, 5, 0, 0, 90),
        (1, 6, 0, 0, 100),
        (1, 7, 0, 0, 100),
    ]

    expected_tops_of_the_world = [
        (1, 2),
        (1, 4),
        (1, 6),
    ]

    #when
    tops_of_the_world = get_tops_of_the_world(vectors)

    #then
    assert tops_of_the_world == expected_tops_of_the_world


def test_get_top_for_vector():
    #given
    a = np.array([0,0,0])
    b = np.array([1,0,0])
    vectors = [
        (1, 1, 90, 0, 0),
        (1, 2, 100, 0, 0),
    ]

    expected_top = (1, 2, 100, 0, 0) #TODO: Top does not have to have the lat long elev data! Delete it

    #when
    top = get_top_for_vector(a, b, vectors)

    #then
    assert top == expected_top


# TODO: Add tests for other functions
