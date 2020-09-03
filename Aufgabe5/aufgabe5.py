"""
Lösung zu Aufgabe 5 des 38. Bundeswettbewerbs Informatik von

Florian Rädiker
"""
import itertools
import math
from typing import Iterable, Tuple
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    tqdm = lambda x: x


def approx_romino_count(n: int):
    return math.e ** (-4.3573 + 1.7768*n)


def rotate90(shape: Tuple[int, int], array: int):
    array_size = shape[0]*shape[1]
    array_size_plus_1 = array_size + 1
    height_minus_1 = shape[0] - 1
    x = 0
    for n in range(array_size):
        new_n = (n + (height_minus_1*(n+1))) % array_size_plus_1
        if (array >> n) & 1:
            x |= 1 << new_n
    return x


def rotate180(shape: Tuple[int, int], array: int):
    array_size = shape[0] * shape[1]
    array_size_minus_1 = array_size - 1
    x = 0
    for n in range(array_size):
        new_n = array_size_minus_1 - n
        if (array >> n) & 1:
            x |= 1 << new_n
    return x


def flip_lr(shape: Tuple[int, int], array: int):
    width = shape[1]
    new_array = 0
    for y in range(shape[0]):
        for x in range(width):
            y_pos = y*width
            n = y_pos + x
            new_n = y_pos + (width - 1 - x)
            if (array >> n) & 1:
                new_array |= 1 << new_n
    return new_array


def flip_ud(shape: Tuple[int, int], array: int):
    height = shape[0]
    height_minus_1 = height - 1
    width = shape[1]
    x = 0
    row_with_ones = (2**width - 1)
    for y in range(height):
        row = (array >> (y*width)) & row_with_ones
        new_y = height_minus_1 - y
        x |= row << new_y*width
    return x


def add_right(shape: Tuple[int, int], array: int):
    x = 0
    height = shape[0]
    width = shape[1]
    row_with_ones = (2 ** width - 1)
    for y in range(height):
        row = (array >> (y * width)) & row_with_ones
        x |= row << (y * width + y + 1)
    return x


def add_left(shape: Tuple[int, int], array: int):
    x = 0
    height = shape[0]
    width = shape[1]
    row_with_ones = (2 ** width - 1)
    for y in range(height):
        row = (array >> (y * width)) & row_with_ones
        x |= row << (y * (width + 1))
    return x


def add_bottom(shape: Tuple[int, int], array: int):
    return array << shape[1]


def array_to_str(shape: Tuple[int, int], array: int):
    res = ""
    width = shape[1]
    height = shape[0]
    for y in range(height-1, -1, -1):
        for x in range(width-1, -1, -1):
            res += "■ " if (array >> (y * width + x)) & 1 else "□ "
        res += "\n"
    return res[:-1]


class Romino:
    def __init__(self, shape: Tuple[int, int], array: int, edges: Iterable[Tuple[bool, Tuple[int, int]]]):
        self.shape = shape
        self.array = array
        self.edges = edges
        self._hash = (self.array << 8) + (self.shape[0] << 4) + self.shape[1]

    @staticmethod
    def new(shape: Tuple[int, int], array: int):
        # rotate, reflect array
        if shape[0] == shape[1]:
            array_rot180 = rotate180(shape, array)
            array_rot90 = rotate90(shape, array)
            array_rot90_rot180 = rotate180(shape, array_rot90)
            array = max(
                array,
                array_rot180,
                flip_lr(shape, array),
                flip_lr(shape, array_rot180),
                flip_ud(shape, array),
                flip_ud(shape, array_rot180),
                array_rot90,
                array_rot90_rot180,
                flip_lr(shape, array_rot90),
                flip_lr(shape, array_rot90_rot180),
                flip_ud(shape, array_rot90),
                flip_ud(shape, array_rot90_rot180)
            )
        else:
            if shape[0] > shape[1]:
                array = rotate90(shape, array)
                shape = (shape[1], shape[0])
            array_rot180 = rotate180(shape, array)
            array = max(
                array,
                array_rot180,
                flip_lr(shape, array),
                flip_lr(shape, array_rot180),
                flip_ud(shape, array),
                flip_ud(shape, array_rot180)
            )
        edges = set()
        is_valid = False
        for y in range(shape[0]):
            for x in range(shape[1]):
                if (array >> (y * shape[1] + x)) & 1:
                    y_down = y - 1
                    y_up = y + 1
                    x_down = x - 1
                    x_up = x + 1
                    if not is_valid:
                        surrounding_squares = ""  # v: filled diagonal square, e: filled edge, b: unfilled diagonal square, r: unfilled edge
                        for pos, i in zip(
                                ((y_up, x_down), (y_up, x), (y_up,   x_up),
                                                            (y,      x_up),
                                                            (y_down, x_up), (y_down, x), (y_down, x_down),
                                 (y, x_down)),
                                itertools.cycle([0, 1])):
                            if pos[0] == -1 or pos[1] == -1 or pos[0] >= shape[0] or pos[1] >= shape[1]:
                                # pos is outside array
                                edges.add((False, pos))
                                surrounding_squares += ["b", "r"][i]
                            else:
                                if not (array >> (pos[0] * shape[1] + pos[1])) & 1:
                                    edges.add((True, pos))
                                    surrounding_squares += ["b", "r"][i]
                                else:
                                    surrounding_squares += ["v", "e"][i]
                        surrounding_squares += surrounding_squares[:3]
                        if "rvr" in surrounding_squares:
                            is_valid = True
                    else:
                        for pos, i in zip(
                                ((y_up, x_down), (y_up, x), (y_up, x_up),
                                 (y, x_up),
                                 (y_down, x_up), (y_down, x), (y_down, x_down),
                                 (y, x_down)),
                                itertools.cycle([0, 1])):
                            try:
                                if pos[0] == -1 or pos[1] == -1 or pos[0] >= shape[0] or pos[1] >= shape[1]:
                                    raise IndexError
                                if not (array >> (pos[0] * shape[1] + pos[1])) & 1:
                                    edges.add((True, pos))
                            except IndexError:
                                # pos is outside array
                                edges.add((False, pos))
        if is_valid or shape == (1, 1):
            return Romino(shape, array, edges)
        return None

    def __str__(self):
        return array_to_str(self.shape, self.array)

    def __eq__(self, other):
        return self._hash == other._hash

    def __hash__(self):
        return self._hash

    def grow(self):
        new_rominos = set()
        for in_array, pos in self.edges:
            if in_array:
                new_array = self.array
                new_shape = self.shape
                n = (pos[0] * new_shape[1]) + pos[1]
            else:
                # pos is outside array
                if pos[0] == -1:
                    # y-pos is too small (-1)
                    if pos[1] == -1:
                        # x-pos is too big, pos is lower right corner
                        new_array = add_right((self.shape[0] + 1, self.shape[1]), add_bottom(self.shape, self.array))
                        new_shape = (self.shape[0] + 1, self.shape[1] + 1)
                        n = 0
                    elif pos[1] >= self.shape[1]:
                        # x-pos is too small (-1), pos is lower left corner
                        new_array = add_left((self.shape[0] + 1, self.shape[1]), add_bottom(self.shape, self.array))
                        new_shape = (self.shape[0] + 1, self.shape[1] + 1)
                        n = new_shape[1] - 1
                    else:
                        # x-pos is in array, pos is on bottom
                        new_array = add_bottom(self.shape, self.array)
                        new_shape = (self.shape[0] + 1, self.shape[1])
                        n = pos[1]
                elif pos[0] >= self.shape[0]:
                    # y-pos is too big
                    if pos[1] == -1:
                        # x-pos is too big, pos is upper right corner
                        new_array = add_right(self.shape, self.array)
                        new_shape = (self.shape[0] + 1, self.shape[1] + 1)
                        n = (new_shape[0] - 1) * (new_shape[1])
                    elif pos[1] >= self.shape[1]:
                        # x-pos is too small (-1), pos is upper left corner
                        new_array = add_left(self.shape, self.array)
                        new_shape = (self.shape[0] + 1, self.shape[1] + 1)
                        n = new_shape[0] * new_shape[1] - 1
                    else:
                        # x-pos is in array, pos is on top
                        new_array = self.array
                        new_shape = (self.shape[0] + 1, self.shape[1])
                        n = (new_shape[0] - 1) * new_shape[1] + pos[1]
                else:
                    # y-pos is in array
                    if pos[1] == -1:
                        # x-pos is too big, pos is on right
                        new_array = add_right(self.shape, self.array)
                        new_shape = (self.shape[0], self.shape[1] + 1)
                        n = pos[0]*new_shape[1]
                    elif pos[1] >= self.shape[1]:
                        # x-pos is too small (-1), pos is on left
                        new_array = add_left(self.shape, self.array)
                        new_shape = (self.shape[0], self.shape[1] + 1)
                        n = pos[0]*new_shape[1] + pos[1]
                    else:
                        # x-pos is in array
                        raise ValueError
            new_romino_array = new_array | 1 << n
            romino = Romino.new(new_shape, new_romino_array)
            if romino is not None:
                new_rominos.add(romino)
        return new_rominos


if __name__ == "__main__":
    romino1 = Romino.new((1, 1), 1)
    generation = {romino1}
    for i in range(2, 11):
        new_generation = set()
        for romino in tqdm(generation):
            new_generation.update(romino.grow())
        print("\n################")
        print(f"# {i}-Rominos")
        print("Anzahl:", len(new_generation))
        if i < 6:
            for romino in new_generation:
                print(romino, end="\n\n")
        generation = new_generation
        
        """for romino in new_generation:
            count = 0
            for xy in range(romino.shape[0]*romino.shape[1]):
                if (romino.array >> xy) & 1:
                    count += 1
            if count != i:
                print("!!!!!!")
                print(bin(romino.array))
                print(romino)"""  # uncomment to check count of squares for every new Romino
