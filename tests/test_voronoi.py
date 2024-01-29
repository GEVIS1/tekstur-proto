from tekstur.voronoi import voronoi
from PIL.Image import Image
from random import randint

import pytest

safe_width = 10
safe_height = 10
safe_seed = 5

def test_voronoi_returns_image():
    assert isinstance(voronoi(safe_width, safe_height, safe_seed), Image)

def test_voronoi_fails_with_invalid_width():
    invalid_width = -1
    with pytest.raises(ValueError) as invalid_width_result:
        voronoi(invalid_width, safe_height, safe_seed)
    assert str(invalid_width_result.value) == "Width and height must be >= 0"

def test_voronoi_fails_with_invalid_height():
    invalid_height = -1
    with pytest.raises(ValueError) as invalid_height_result:
        voronoi(safe_width, invalid_height, safe_seed)
    assert str(invalid_height_result.value) == "Width and height must be >= 0"

def test_voronoi_width_correctly_set():
    width_correctly_set_width = randint(1,10000)
    width_correctly_set_image = voronoi(width_correctly_set_width, safe_height, safe_seed)
    assert width_correctly_set_image.size == (width_correctly_set_width, safe_height)

def test_voronoi_height_correctly_set():
    height_correctly_set_height = randint(1,10000)
    height_correctly_set_image = voronoi(safe_width, height_correctly_set_height, safe_seed)
    assert height_correctly_set_image.size == (safe_width, height_correctly_set_height)

def test_voronoi_generate_seeds():
    pass