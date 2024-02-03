from random import seed, randint
from math import dist, sqrt
from PIL import Image, ImageDraw

class Seed():
    def __init__(self, x: int, y: int, color: str, size: float = 5):
        self.x = x - size
        self.y = y - size
        self.color = color
        self.size = size

    @property
    def xy(self):
        return self.x, self.y
    
    @property
    def center(self):
        half_size = self.size / 2
        return self.x + half_size, self.y + half_size

    @property
    def bounds(self):
        return self.x, self.y, self.x + self.size, self.y + self.size

def euclidean_distance(p: tuple[float, float], q: tuple[float,float]) -> float:
    if len(p) == 2:
        p1, p2 = p
    else:
        p1, p2, _, _ = p
    if len(q) == 2:
        q1, q2 = q
    else:
        q1, q2, _, _ = q
    return sqrt(((q1 - p1) ** 2) + ((q2 - p2) ** 2))

def generate_seeds(image: Image, seeds: int, size: int = 10, distance_threshold: float = 3) -> Image:
    width, height = image.size

    seed_list = []
    while len(seed_list) < seeds:
        x, y = randint(0 + size, width - size), randint(0 + size, height - size)

        appendable = True

        # TODO: Rewrite or squash infinite loop bug
        for x0, y0, x1, y1 in seed_list:
            distance = dist((x0, x1), (y0, y1))
            print(f"{distance=} {distance_threshold=} {distance < distance_threshold=}")
            if distance < distance_threshold:
                appendable = False
        
        xy = x, y, x + size, y + size

        if appendable:
            seed_list.append(xy)

    return seed_list

def find_closest_point(points, point, img, size) -> tuple[tuple[int,int], tuple[int,int,int]]:
    closest = None

    for pnt in points:
        if closest is None:
            closest = (euclidean_distance(point,pnt), pnt, img.getpixel((pnt[0] + (size/2), pnt[1] + (size/2))))
        elif (new_dist := euclidean_distance(point, pnt)) < closest[0]:
            closest = (new_dist, pnt, img.getpixel((pnt[0] + size, pnt[1] + size)))

    return (closest[1], closest[2])


def fill_area_around_seeds(image: Image, seeds: list[Seed], size) -> Image:
    width, height = image.size
    canvas = ImageDraw.Draw(image)

    for y in range(height):
        for x in range(width):
            point = x,y
            #pix = img.getpixel(point)
            [_, color] = find_closest_point(seeds, point, image, size)
            canvas.point(point, color)

    return image

def draw_seeds(image, seeds):
    canvas = ImageDraw.Draw(image)

    for seed in seeds:
        random_color = randint(0,255), randint(0,255), randint(0,255)
        canvas.ellipse(seed, random_color, "black", 2)

    return image

def voronoi(width: int, height: int, seeds: int, random_seed: int = None, mode: str = "RGB") -> Image:
    """
    Generate an image with a voronoi pattern, returns an Image of a
    voronoi pattern with the specified number of seeds.
    """

    if random_seed:
        if not isinstance(random_seed, (int, float, str, bytes, bytearray)):
            raise ValueError(f"random_seed expects one of the following types: (int, float, str, bytes, bytearray), but got type: ({type(random_seed)})")
        
        seed(random_seed)

    #TODO: Update to use seed class
    image = Image.new(mode,(width, height))
    seed_list = generate_seeds(image, seeds, 10)
    image = draw_seeds(image, seed_list)
    image = fill_area_around_seeds(image, seed_list, 10)
    image = draw_seeds(image, seed_list)
    return image
