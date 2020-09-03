"""
Lösung zu Aufgabe 2 des 38. Bundeswettbewerbs Informatik von

Florian Rädiker
"""
from functools import lru_cache


@lru_cache()
def split_number(number):
    number_startswith_0 = number[0] == "0"
    length = len(number)
    if length < 6:
        if length == 5:
            possibilities = []
            second_block = number[2:]
            second_block_0 = second_block[0] == "0"
            if second_block_0 == 0:
                return number[:2] + "-" + second_block, number_startswith_0
            possibilities.append((number[:2] + "-" + second_block, number_startswith_0 + second_block_0))

            second_block = number[3:]
            second_block_0 = second_block[0] == "0"
            if second_block_0 == 0:
                return number[:3] + second_block, number_startswith_0
            possibilities.append((number[:3] + "-" + second_block, number_startswith_0 + second_block_0))
        else:
            return number, number_startswith_0
    else:
        possibilities = []

        blocks, count = split_number(number[4:])
        if count == 0:
            return number[:4] + "-" + blocks, number_startswith_0
        count += number_startswith_0
        possibilities.append((number[:4] + "-" + blocks, count))

        blocks, count = split_number(number[3:])
        if count == 0:
            return number[:3] + "-" + blocks, number_startswith_0
        count += number_startswith_0
        possibilities.append((number[:3] + "-" + blocks, count))

        blocks, count = split_number(number[2:])
        if count == 0:
            return number[:2] + "-" + blocks, number_startswith_0
        count += number_startswith_0
        possibilities.append((number[:2] + "-" + blocks, count))
    return min(possibilities, key=lambda x: x[1])


if __name__ == "__main__":
    import time

    with open("beispieldaten/nummern.txt", "r") as f:
        numbers = (line.strip() for line in f.readlines() if line.strip() != "")
    t1 = time.perf_counter_ns()
    for number in numbers:
        if not number.startswith("#"):
            print("############")
            print(number)
            t1 = time.perf_counter()
            blocks, count = split_number(number)
            t2 = time.perf_counter()
            count = int(count)  # if count is still bool (0 or 1)
            print(blocks)
            print("Nullblöcke:", count)
            print("Time: {:.7f}".format(t2 - t1), end="\n\n")
