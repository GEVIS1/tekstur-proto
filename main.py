
from PIL import Image, ImageDraw
from tekstur.voronoi import voronoi, euclidean_distance
from math import dist, inf

if __name__ == "__main__":
    # im = voronoi(500, 500, 5)
    # im.save('test.png')
    canvas_size = 1000
    img = Image.new("RGB", (canvas_size, canvas_size))
    size = 50
    position = canvas_size/4
    def new_point(x, y):
        p0 = x,y
        p1 = (p0[0] + size, p0[1] + size)
        pc = (p0[0] + (size / 2), p0[1] + (size / 2))    

        return p0, p1, pc
    
    p0, p1, pc = new_point(position, position)
    q0, q1, qc = new_point(canvas_size-position, canvas_size-position)
    d0, d1, dc = new_point(150,750)
    p0, p1, pc = new_point(750,450)
    canvas = ImageDraw.Draw(img)

    distance = euclidean_distance(pc, qc)

    text = f"Distance: {distance}"
    textlength = canvas.textlength(text, font_size=60)
    canvas.text((canvas_size/2-(textlength/2),canvas_size/2-(textlength/2)), text, font_size=60)

    canvas.line((pc, qc), width=5)

    canvas.ellipse((p0, p1), "red")
    canvas.ellipse((q0, q1), "green")
    canvas.ellipse((d0, d1), "blue", "black")
    canvas.ellipse((p0, p1), "#606")
    img.save("test.png")

    "--------------"
    points = [pc, qc, dc, pc]
    def find_closest_point(points, point, img) -> tuple[tuple[int,int], tuple[int,int,int]]:
        closest = None

        for pnt in points:
            if closest is None:
                closest = (euclidean_distance(point,pnt), pnt, img.getpixel(pnt))
            elif new_dist := euclidean_distance(point, pnt) < closest[0]:
                closest = (new_dist, pnt, img.getpixel(pnt))

        return (closest[1], closest[2])

    for y in range(canvas_size):
        for x in range(canvas_size):
            point = x,y
            pix = img.getpixel(point)
            [_, color] = find_closest_point(points, point, img)
            canvas.point(point,color)

    "--------------"
    canvas.ellipse((p0, p1), "red", "black")
    canvas.ellipse((q0, q1), "green", "black")
    canvas.ellipse((d0, d1), "blue", "black")
    canvas.ellipse((p0, p1), "#606", "black")
    img.save("test2.png")