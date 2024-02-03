
from PIL import Image, ImageDraw
from tekstur.voronoi import voronoi, euclidean_distance
from math import dist, inf

if __name__ == "__main__":
    im = voronoi(500, 500, 5)
    im.save('test.png')