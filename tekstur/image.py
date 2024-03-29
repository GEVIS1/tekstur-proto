from PIL import Image

def save(data, filename, background=(0,0,0)):
    img = Image.new("RGB", (len(data[0]), len(data)), background)
    pixel_data = img.load()
    for y in range(len(data)):
        for x in range(len(data[0])):
            pixel_data[x, y] = data[y][x]
    img.save(filename)