import pygame as pg
from math import *

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 900, 700
pg.display.set_caption("   3D projection in pg!")
screen = pg.display.set_mode((WIDTH, HEIGHT))


def matmul(a, b):
    if len(a[0]) != len(b):
        print("Error:\nRows do not match coloms.")
    else:
        answer = []
        for i in a:
            colum = []
            for j in range(0, len(b[0])):
                sum = 0
                for k in range(0, len(b)):
                    sum += i[k] * b[k][j]
                colum.append(sum)
            answer.append(colum)
        return answer


projection_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 0]]


class Cube:
    def __init__(self, x, y, z, w, h, l, xr=0, yr=0, zr=0, color="blue"):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.l = l
        self.xr = xr
        self.yr = yr
        self.zr = zr
        self.color = color
        points = []
        points.append([[-w / 2], [-h / 2], [l / 2]])
        points.append([[w / 2], [-h / 2], [l / 2]])
        points.append([[w / 2], [h / 2], [l / 2]])
        points.append([[-w / 2], [h / 2], [l / 2]])
        points.append([[-w / 2], [-h / 2], [-l / 2]])
        points.append([[w / 2], [-h / 2], [-l / 2]])
        points.append([[w / 2], [h / 2], [-l / 2]])
        points.append([[-w / 2], [h / 2], [-l / 2]])
        self.points = points


def update(obj):
    xr = obj.xr
    yr = obj.yr
    zr = obj.zr
    rx = [
        [cos(xr), 0, sin(xr)],
        [0, 1, 0],
        [-sin(xr), 0, cos(xr)],
    ]
    ry = [
        [1, 0, 0],
        [0, cos(yr), -sin(yr)],
        [0, sin(yr), cos(yr)],
    ]
    rz = [
        [cos(zr), -sin(zr), 0],
        [sin(zr), cos(zr), 0],
        [0, 0, 1],
    ]
    for i in obj.points:
        pos = matmul(rz, i)
        pos = matmul(ry, pos)
        pos = matmul(rx, pos)
        pos[0][0] += obj.x
        pos[1][0] += obj.y
        pg.draw.circle(screen, obj.color, (pos[0][0], pos[1][0]), 5)


objects = {
    'test': Cube(100, 100, 400, 90, 90, 0, 0, 0, 0, "red"),
    'test1': Cube(200, 200, 500, 90, 90, 90, 0, 0, 0)
}
clock = pg.time.Clock()

while True:
    clock.tick(60)
    screen.fill(BLACK)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
        #if event.type == :
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        for i in objects:
            objects[i].xr -= 0.01
    if keys[pg.K_RIGHT]:
        for i in objects:
            objects[i].xr += 0.01
    mouse_presses = pg.mouse.get_pressed()
    mx, my = pg.mouse.get_rel()
    if mouse_presses[0]:
        mx *= 0.005
        my *= 0.005
        print(f"({mx},{my}")
        for i in objects:
            objects[i].xr += mx
            objects[i].yr += my
        x, y = pg.mouse.get_pos()
        pg.mouse.set_pos([x, y])

    for i in objects:
        update(objects[i])
    #print(f"({pos[0]},{pos[1]})")

    pg.display.update()
