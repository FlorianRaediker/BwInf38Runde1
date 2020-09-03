"""
Lösung zur Junioraufgabe 2 des 38. Bundeswettbewerbs Informatik von

Florian Rädiker
"""
import time

import numpy as np


class MapGenerator:
    def __init__(self, fileobj):
        height = int(fileobj.readline())
        width = int(fileobj.readline())
        self.parts = np.zeros((height * 2, width * 2), dtype=np.dtype("B"))
        self.original_empty_parts = []
        self.no_bit_found_pos = None
        for y, line in enumerate(fileobj.readlines()):
            for x, character in enumerate(line.strip()):
                if character == "0":
                    self.parts[y, x] = 0
                elif character == "1":
                    self.parts[y, x] = 1
                elif character == "*":
                    self.parts[y, x] = 2
                    self.original_empty_parts.append((y, x))
                else:
                    raise ValueError(f"unknown part '{character}'")
        self.empty_parts = self.original_empty_parts.copy()

    def to_string(self, spacy=False, size=False, empty_color="\033[1;32m", not_found_color="\033[1;31m"):
        if size:
            res = f"{self.parts.shape[0] // 2}\n{self.parts.shape[1] // 2}\n"
        else:
            res = ""
        if spacy:
            res += "\n"
        for y in range(self.parts.shape[0]):
            for x in range(self.parts.shape[1]):
                pos = (y, x)
                if pos == self.no_bit_found_pos:
                    res += not_found_color
                elif pos in self.original_empty_parts:
                    res += empty_color
                res += ["0", "1", "*"][self.parts[y, x]]
                if empty_color or not_found_color:
                    res += "\033[1;m"
                if spacy and x != self.parts.shape[1] - 1:
                    if x % 2 == 0:
                        res += " "
                    else:
                        res += "   "
            if y != self.parts.shape[0] - 1:
                if spacy and y % 2 == 1:
                    res += "\n\n"
                else:
                    res += "\n"
        return res

    def _set_bit(self, y, x):
        surrounding = []
        if y % 2 == 0:
            surrounding.append((y - 1, x))
        else:
            surrounding.append(((y + 1, x)))
        if x % 2 == 0:
            surrounding.append((y, x - 1))
        else:
            surrounding.append((y, x + 1))
        possible_bit = None
        empty_surrounding = None
        for y_, x_ in surrounding:
            if 0 <= y_ < self.parts.shape[0] and 0 <= x_ < self.parts.shape[1]:
                bit = self.parts[y_, x_]
                if bit != 2:
                    if possible_bit is not None and bit != possible_bit:
                        # another bit was already set
                        self.no_bit_found_pos = (y, x)
                        raise ValueError(f"Keine Kachel für ({y / 2}, {x / 2}) gefunden")
                    possible_bit = bit
                else:
                    empty_surrounding = (y_, x_)
        if possible_bit is not None:
            self.parts[y, x] = possible_bit
            self.empty_parts.remove((y, x))
            if empty_surrounding:
                self._set_bit(*empty_surrounding)

    def fill_spaces(self, wildcard_fill=0):
        for y, x in self.original_empty_parts:
            if self.parts[y, x] == 2:
                self._set_bit(y, x)
        for pos in self.empty_parts:
            assert self.parts[pos[0], pos[1]] == 2
            self.parts[pos[0], pos[1]] = wildcard_fill


if __name__ == "__main__":
    print()
    while True:
        text = input("Bit, der bei mehreren Möglichkeiten gesetzt werden soll (0, 1 oder *): ")
        if text == "0":
            wildcard_fill = 0
            break
        elif text == "1":
            wildcard_fill = 1
            break
        elif text == "*":
            wildcard_fill = 2
            break
        print("Bitte '0', '1' oder '*' eingeben")

    t1 = time.perf_counter_ns()
    for file_num in ["", "1", "2", "3", "4", "5"]:
        filename = f"map{file_num}_compact.txt"
        print("################")
        print(filename)
        with open("beispieldaten/" + filename) as f:
            map_generator = MapGenerator(f)
        print(map_generator.to_string(True))
        try:
            map_generator.fill_spaces(wildcard_fill)
        except ValueError as e:
            print("\n", e.args[0], sep="")
        print("\nVervollständigt:")
        print(map_generator.to_string(True, True))
        print("\n")
    t2 = time.perf_counter_ns()
    print("Time:", t2-t1)
