from random import seed, randint
from math import dist
from PIL import Image, ImageDraw

def generate_seeds(image: Image, seeds: int, size: int = 10, distance_threshold: float = 3) -> Image:
    canvas = ImageDraw.Draw(image)
    width, height = image.size

    seed_list = []
    while len(seed_list) < seeds:
        x, y = randint(0 + size, width - size), randint(0 + size, height - size)
        print(f"{len(seed_list)=}")

        for derp in seed_list:
            print(derp)


        print(f"{x=},{y=}")
        
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

    for xy in seed_list:
        canvas.ellipse(xy, "red", size)

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

    image = Image.new(mode,(width, height))
    image = generate_seeds(image, seeds)
    return image
