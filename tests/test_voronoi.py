from tekstur.voronoi import voronoi
from PIL.Image import Image

def test_voronoi():
    assert isinstance(voronoi(10, 10, 5), Image)