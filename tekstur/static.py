from random import randint

def naive_static(width, height, colors=[(0,0,0),(255,255,255)]):
    image_data = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(colors[randint(0, len(colors)-1)])
        image_data.append(row)
    return image_data