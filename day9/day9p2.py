#!/usr/bin/env python3

from itertools import combinations, chain
from turtle import Turtle
from typing import Sequence
# cheating? nah. using a well-tested library that is written in C? yeahhhhh!
from shapely.geometry import Polygon

def rectangle_size(coord1: tuple[int, int], coord2: tuple[int, int]) -> int:
    """
    Gets the size of a rectangle drawn between two points on a 2d plane.
    """
    # Only broken out to a function because its a little too long to write in a lambda
    return (abs(coord2[0] - coord1[0]) + 1) * (abs(coord2[1] - coord1[1]) + 1)

def polygon1_is_inside_polygon2(polygon1: Sequence[tuple[int | float, int | float]], polygon2: Sequence[tuple[int | float, int | float]]) -> bool:
    """
    Determines if polygon 1 is entirely inside of polygon 2.
    """
    # Two steps: 1. determine that all vertexes are inside polygon
    #            2. determine that all lines between vertex do not intersect lines of polygon
    # TODO
    shapely_polygon1 = Polygon(polygon1)
    shapely_polygon2 = Polygon(polygon2)
    return shapely_polygon2.contains(shapely_polygon1)

if __name__ == "__main__":
    # For part one, the real dataset is only 500 coordinates large.
    # 500 choose 2 is small enough that brute forcing it is trivial.
    # Plus, I haven't any idea how to do it without brute forcing. Oops.
    red_tiles: list[tuple[int, int]] = list()
    with open("./input", "tr") as input_fp:
        for line in input_fp.readlines():
            # I learned today that canonically AoC inputs do NOT end with a line break.
            # So, technically, the following clause is pointless. 
            # Still I think nano and vi often insert \n at the end of a file when saving if it's been edited.
            if not line:
                break
            red_tile = list(int(coord) for coord in line.strip().split(","))
            red_tiles.append(red_tile)
    # initialize visualization
    t = Turtle()
    t.speed(0)
    ts = t.getscreen()
    ts.bgcolor("gray")
    ts.tracer(0)
    max_dimension = max(chain.from_iterable(red_tiles))
    ts.setworldcoordinates(0, max_dimension, max_dimension, 0)
    t.hideturtle()
    t.pensize(1)
    t.penup()
    t.fillcolor("green")
    t.pencolor("green")

    # draw
    t.goto(*red_tiles[0])
    t.pendown()
    t.dot(3, "red")
    with t.fill():
        with t.poly():
            for tile in red_tiles[1:]:
                t.goto(*tile)
                t.dot(3, "red")
            t.goto(*red_tiles[0])
    t.penup()
    ts.update()
    green_tile_polygon: Sequence[tuple[float, float]] = t.get_poly()

    # ok, now we have the base polygon drawn
    # next, we need to find the size of each possible set of quads
    sizes_map = [
        (pair, rectangle_size(*pair))
        for pair
        in combinations(red_tiles, 2)
    ]
    sizes_map.sort(
        key=lambda p: p[1],
        reverse=True
    )
    for pair, size in sizes_map:
        # starting from the largest quad, we are going to
        # check if it fits inside of the polygon
        # if it does then we can break and get outta here
        coord1, coord2 = pair
        coord1x, coord1y = coord1
        coord2x, coord2y = coord2
        pair_quad_vertexes = [
            (coord1x, coord1y),
            (coord2x, coord1y),
            (coord2x, coord2y),
            (coord1x, coord2y)
        ]
        if polygon1_is_inside_polygon2(pair_quad_vertexes, green_tile_polygon):
            t.goto(coord1x, coord1y)
            t.pencolor("yellow")
            t.fillcolor("yellow")
            t.pendown()
            with t.fill():
                with t.poly():
                    t.goto(coord2x, coord1y)
                    t.goto(coord2x, coord2y)
                    t.goto(coord1x, coord2y)
                    t.goto(coord1x, coord1y)
            t.penup()
            print(size)
            break
    else:
        raise RuntimeError("Didn't find a polygon that fit inside!")
    ts.update()

    # show screen until a quit
    # I commented it out just so I could do a time test
    ts.mainloop()

