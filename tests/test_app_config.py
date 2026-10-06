from utils.config import CITIES, CITY_COORDS


def test_cities_are_defined():
    assert isinstance(CITIES, list)
    assert len(CITIES) > 0
    assert len(CITIES) == len(set(CITIES))


def test_every_city_has_coordinates():
    for city in CITIES:
        assert city in CITY_COORDS
        coords = CITY_COORDS[city]
        assert {"lat", "lon"}.issubset(coords.keys())
        assert isinstance(coords["lat"], (int, float))
        assert isinstance(coords["lon"], (int, float))
