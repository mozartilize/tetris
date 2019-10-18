import random


S = [[
    ".....",
    ".....",
    "..00.",
    ".00..",
    "....."
], [
    ".....",
    "..0..",
    "..00.",
    "...0.",
    "....."
]]

Z = [[
    ".....",
    ".....",
    ".00..",
    "..00.",
    "....."
], [
    ".....",
    "..0..",
    ".00..",
    ".0...",
    "....."
]]

I = [[  # noqa
    "..0..",
    "..0..",
    "..0..",
    "..0..",
    "....."
], [
    ".....",
    "0000.",
    ".....",
    ".....",
    "....."
]]

O = [[  # noqa
    ".....",
    ".....",
    ".00..",
    ".00..",
    "....."
]]

J = [[
    ".....",
    ".0...",
    ".000.",
    ".....",
    "....."
], [
    ".....",
    "..00.",
    "..0..",
    "..0..",
    "....."
], [
    ".....",
    ".....",
    ".000.",
    "...0.",
    "....."
], [
    ".....",
    "..0..",
    "..0..",
    ".00..",
    "....."
]]

L = [[
    ".....",
    "...0.",
    ".000.",
    ".....",
    "....."
], [
    ".....",
    "..0..",
    "..0..",
    "..00.",
    "....."
], [
    ".....",
    ".....",
    ".000.",
    ".0...",
    "....."
], [
    ".....",
    ".00..",
    "..0..",
    "..0..",
    "....."
]]
T = [[
    ".....",
    "..0..",
    ".000.",
    ".....",
    "....."
], [
    ".....",
    "..0..",
    "..00.",
    "..0..",
    "....."
], [
    ".....",
    ".....",
    ".000.",
    "..0..",
    "....."
], [
    ".....",
    "..0..",
    ".00..",
    "..0..",
    "....."
]]

SHAPES = {
    "S": [S, (0, 255, 0)],
    "Z": [Z, (255, 0, 0)],
    "I": [I, (0, 255, 255)],
    "O": [O, (255, 255, 0)],
    "J": [J, (255, 165, 0)],
    "L": [L, (0, 0, 255)],
    "T": [T, (128, 0, 128)]
}


class Shape:

    @classmethod
    def new_shape(cls):
        return cls(random.choice(list(SHAPES.keys())))

    def __init__(self, shape_name):
        self._shape_name = shape_name
        self._shape_type = SHAPES[self._shape_name][0]
        self._color = SHAPES[self._shape_name][1]
        self._rotation = 0

    @property
    def shape(self):
        return self._shape_type[self._rotation]

    def rotate_right(self):
        self._rotation += 1
        if self._rotation > len(self._shape_type) - 1:
            self._rotation = 0
        return self.shape

    def rotate_left(self):
        self._rotation -= 1
        if self._rotation < 0:
            self._rotation = len(self._shape_type) - 1
        return self.shape

    @property
    def variants(self):
        return self._shape_type

    @property
    def name(self):
        return self._shape_name

    @property
    def rotation(self):
        return self._rotation

    @property
    def color(self):
        return self._color
