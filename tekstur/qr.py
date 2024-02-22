from tekstur.static import naive_static

# What
def fake_qr(width, height, colors=[(0,0,0),(255,255,255)]):
    data = naive_static(width, height, colors)
    b = (0,0,0)
    w = (255,255,255)
    qr = [
        [b,b,b,b,b,b,b,None,None,None,None,None,None,None,b,b,b,b,b,b,b],
        [b,w,w,w,w,w,b,None,None,None,None,None,None,None,b,w,w,w,w,w,b],
        [b,w,b,b,b,w,b,None,None,None,None,None,None,None,b,w,b,b,b,w,b],
        [b,w,b,b,b,w,b,None,None,None,None,None,None,None,b,w,b,b,b,w,b],
        [b,w,b,b,b,w,b,None,None,None,None,None,None,None,b,w,b,b,b,w,b],
        [b,w,w,w,w,w,b,None,None,None,None,None,None,None,b,w,w,w,w,w,b],
        [b,b,b,b,b,b,b,w,   b,   w,   b,   w,   b,   w,   b,b,b,b,b,b,b],
        [None for _ in range(21)],
        [*[None for _ in range(6)], b, *[None for _ in range(14)]],
        [None for _ in range(21)],
        [*[None for _ in range(6)], b, *[None for _ in range(14)]],
        [None for _ in range(21)],
        [*[None for _ in range(6)], b, *[None for _ in range(14)]],
        [None for _ in range(21)],
        [b,b,b,b,b,b,b,None,None,None,None,None,None,None,b,b,b,b,b,b,b],
        [b,w,w,w,w,w,b,None,None,None,None,None,None,None,b,w,w,w,w,w,b],
        [b,w,b,b,b,w,b,None,None,None,None,None,None,None,b,w,b,b,b,w,b],
        [b,w,b,b,b,w,b,None,None,None,None,None,None,None,b,w,b,b,b,w,b],
        [b,w,b,b,b,w,b,None,None,None,None,None,None,None,b,w,b,b,b,w,b],
        [b,w,w,w,w,w,b,None,None,None,None,None,None,None,b,w,w,w,w,w,b],
        [b,b,b,b,b,b,b,None,None,None,None,None,None,None,b,b,b,b,b,b,b],
    ]

    for y in range(len(qr)):
        for x in range(len(qr[0])):
            if qr[y][x] is not None:
                data[y][x] = qr[y][x]

    return data