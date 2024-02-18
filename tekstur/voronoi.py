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

#TODO: Check if math dist is faster than this
def euclidean_distance(p: Seed, q: Seed) -> float:
    q1, q2 = q.xy
    p1, p2 = p.xy
    return sqrt(((q1 - p1) ** 2) + ((q2 - p2) ** 2))

def generate_seeds_random(image: Image, seeds: int, size: int = 10, distance_threshold: float = 3) -> list[Seed]:
    width, height = image.size

    seed_list: list[Seed] = []
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

def generate_seeds_grid(image: Image, seeds: int, size: int = 10) -> list[Seed]:
    grid_col = sqrt(seeds)

    if grid_col % 1 != 0:
        raise ValueError("Number of seeds must be a perfect square")
    
    width, height = image.size
    grid_gap = width / grid_col

    seed_list: list[Seed] = [[[] for _ in range(int(grid_col))] for _ in range(int(grid_col))]

    col, row = 0, 0

    for seed_n in range(seeds):
        x0 = col * grid_gap
        x1 = (col * grid_gap) + grid_gap
        y0 = row * grid_gap
        y1 = (row * grid_gap) + grid_gap
        x = randint(x0, x1)
        y = randint(y0, y1)
        colour = f"rgb({randint(0,255)},{randint(0,255)},{randint(0,255)})"
        new_seed = Seed(x, y, colour, size)

        seed_list[row][col].append(new_seed)

        col += 1
        if col == grid_col:
            col = 0
            row += 1

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


def fill_area_around_seeds_random(image: Image, seeds: list[Seed]) -> Image:
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

def find_grid_indices(x, y, grid_gap, width, height) -> tuple[int,int]:
    # TODO: Check for robustness
    col = int(x // grid_gap)
    row = int(y // grid_gap)

    if col >= width:
        col = width - 1
    if row >= height:
        row = height - 1

    return col, row

def find_neighbors(row: int, col: int, height: int, width: int, seeds: list[list[Seed]]):
    neighbors = []
    for neighbor_row in range(-1, 2):
        for neighbor_col in range(-1, 2):
            if (new_row := row + neighbor_row) >= 0 \
                and new_row < len(seeds) \
                and (new_col := col + neighbor_col) >= 0 \
                and new_col < len(seeds[0]):
                neighbors.append(*seeds[new_row][new_col])
    return neighbors

def fill_area_around_seeds_grid(image: Image, seeds: list[list[Seed]], grid_gap: int) -> Image:
    width, height = image.size
    canvas = ImageDraw.Draw(image)

    for y in range(height):
        for x in range(width):
            point = x, y
            col, row = find_grid_indices(x, y, grid_gap, width, height)
            pix = image.getpixel(point)
            if pix == (0, 0, 0):
                neighbors = find_neighbors(row, col, height, width, seeds)
                
                [_, color] = find_closest_seed(neighbors, point, image)    
                canvas.point(point, color)

    return image

def draw_seeds_on_image(image, seeds):
    canvas = ImageDraw.Draw(image)
    flattened_seeds = []
    for sublist in seeds:
        for seed in sublist:
            flattened_seeds.append(*seed)
    print(flattened_seeds)

    for seed in flattened_seeds:
        canvas.ellipse(seed.bounds, seed.color, "white", 2)

    return image

def voronoi(width: int, height: int, seeds: int, grid: bool = False, random_seed: int = None, mode: str = "RGB", draw_seeds: bool = False) -> Image:
    """
    Generate an image with a voronoi pattern, returns an Image of a
    voronoi pattern with the specified number of seeds.
    """

    if random_seed:
        if not isinstance(random_seed, (int, float, str, bytes, bytearray)):
            raise ValueError(f"random_seed expects one of the following types: (int, float, str, bytes, bytearray), but got type: ({type(random_seed)})")
        
        seed(random_seed)

    image = Image.new(mode,(width, height))

    if grid:
        seed_list_grid = generate_seeds_grid(image, seeds, 10)
        if draw_seeds:
            image = draw_seeds_on_image(image, seed_list_grid)
    else:
        seed_list = generate_seeds_random(image, seeds, 10)
        if draw_seeds:
            image = draw_seeds_on_image(image, seed_list)
    
    

    # TODO: Optimize by only checking seeds in pixel's square and neighbouring squares on the grid
    # TODO: Rewrite in Fortune's algorithm
    if grid:
        image = fill_area_around_seeds_grid(image, seed_list_grid, width / sqrt(seeds))
    else:
        image = fill_area_around_seeds_random(image, seed_list)
    return image
