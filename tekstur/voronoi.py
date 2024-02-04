from random import seed, randint
from math import sqrt
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

def euclidean_distance(p: Seed, q: Seed) -> float:
    q1, q2 = q.xy
    p1, p2 = p.xy
    return sqrt(((q1 - p1) ** 2) + ((q2 - p2) ** 2))

def generate_seeds(image: Image, seeds: int, size: int = 10, distance_threshold: float = 3) -> Image:
    width, height = image.size

    seed_list = []
    while len(seed_list) < seeds:
        x, y = randint(0 + size, width - size), randint(0 + size, height - size)
        colour = f"rgb({randint(0,255)},{randint(0,255)},{randint(0,255)})"
        new_seed = Seed(x,y, colour, size)
        appendable = True

        # TODO: Rewrite
        for seed in seed_list:
            distance = euclidean_distance(seed, new_seed)
            if distance < distance_threshold:
                appendable = False
    
        if appendable:
            seed_list.append(new_seed)

    return seed_list

def find_closest_seed(seeds, point, img) -> tuple[Seed, tuple[int,int,int]]:
    closest = None
    if not isinstance(point, Seed):
        x, y = point
        point = Seed(x, y, "black")

    for seed in seeds:
        if closest is None:
            closest = (euclidean_distance(point,seed), seed, seed.color)
        elif (new_dist := euclidean_distance(point, seed)) < closest[0]:
            closest = (new_dist, seed, seed.color)

    return (closest[1], closest[2])


def fill_area_around_seeds(image: Image, seeds: list[Seed]) -> Image:
    width, height = image.size
    canvas = ImageDraw.Draw(image)

    for y in range(height):
        for x in range(width):
            point = x, y
            pix = image.getpixel(point)
            if pix == (0, 0, 0):
                [_, color] = find_closest_seed(seeds, point, image)
                canvas.point(point, color)

    return image

def draw_seeds_on_image(image, seeds):
    canvas = ImageDraw.Draw(image)

    for seed in seeds:
        canvas.ellipse(seed.bounds, seed.color, "white", 2)

    return image

def voronoi(width: int, height: int, seeds: int, random_seed: int = None, mode: str = "RGB", draw_seeds: bool = False) -> Image:
    """
    Generate an image with a voronoi pattern, returns an Image of a
    voronoi pattern with the specified number of seeds.
    """

    if random_seed:
        if not isinstance(random_seed, (int, float, str, bytes, bytearray)):
            raise ValueError(f"random_seed expects one of the following types: (int, float, str, bytes, bytearray), but got type: ({type(random_seed)})")
        
        seed(random_seed)

    image = Image.new(mode,(width, height))
    # TODO: Generate grid and randomly place seed in each square
    seed_list = generate_seeds(image, seeds, 10)
    if draw_seeds:
        image = draw_seeds_on_image(image, seed_list)

    # TODO: Optimize by only checking seeds in pixel's square and neighbouring squares on the grid
    image = fill_area_around_seeds(image, seed_list)
    return image
