"""
Lösung zur Junioraufgabe 1 des 38. Bundeswettbewerbs Informatik von

Florian Rädiker
"""
import re


class Parallelen:
    REGEX_WORD = re.compile(r"\w+")

    def __init__(self, words, index_second_half):
        self.words = words
        self.word_count = len(self.words)
        self.visited_indices = set()
        self.end_indices = set()
        self.index_second_half = index_second_half

    @staticmethod
    def from_file(fileobj, index_second_half):
        return Parallelen(Parallelen.REGEX_WORD.findall(fileobj.read()), index_second_half)

    def check(self):
        for start_index in range(self.index_second_half):
            print(f"\nStarte bei Wort '{self._get_word_info(start_index)}'")
            try:
                self.end_indices.add(self._walk_from_word(start_index))
                print()
            except ValueError:
                pass

    def _get_word_info(self, index):
        word = self.words[index]
        return f"{index}.\033[33m{word}\033[0m({len(word)})"

    def _walk_from_word(self, index):
        if index in self.visited_indices:
            print(f"Wort wurde bereits besucht")
            raise ValueError
        self.visited_indices.add(index)
        new_index = index + len(self.words[index])
        if new_index >= self.word_count:
            return index
        print("->", self._get_word_info(new_index), "", end="")
        return self._walk_from_word(new_index)


if __name__ == "__main__":
    with open("beispieldaten/parallelen.txt", "r") as f:
        parallelen = Parallelen.from_file(f, 43)
    parallelen.check()
    print(parallelen.end_indices)
    print([parallelen.words[i] for i in parallelen.end_indices])
    print("Besuchte Indizes:", sorted(parallelen.visited_indices))
