from random import seed, randint
from PIL import Image

def generate_seeds(image: Image, seeds: int) -> Image:
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
