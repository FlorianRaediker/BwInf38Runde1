"""
Lösung zu Aufgabe 3 des 38. Bundeswettbewerbs Informatik von

Florian Rädiker
"""
import itertools
from functools import lru_cache


@lru_cache()
def create_beaver_distributions(beaver_count):
    generation = [(0, second_count, beaver_count-second_count) for second_count in range(beaver_count//2+1)]
    all_distributions = {dist: None for dist in generation}
    generations = [generation]
    while True:
        generation = []
        for parent in generations[-1]:
            for beaver_dist_permutation in itertools.permutations(parent):
                if beaver_dist_permutation[0] % 2 == 0 and beaver_dist_permutation[0] != 0:
                    half = beaver_dist_permutation[0] // 2
                    new_beaver_dist = tuple(sorted((half, beaver_dist_permutation[1] + half, beaver_dist_permutation[2])))
                    if new_beaver_dist not in all_distributions:
                        generation.append(new_beaver_dist)
                        all_distributions[new_beaver_dist] = parent
        if not generation:
            break
        generations.append(generation)
    return generations, all_distributions


def generate_beaver_distributions(beaver_count):
    last_generation = [(0, second_count, beaver_count-second_count) for second_count in range(beaver_count//2+1)]
    for beaver_dist in last_generation:
        yield 0, beaver_dist
    generation_num = 1
    all_distributions = set(last_generation)
    while True:
        generation = []
        for parent in last_generation:
            for beaver_dist_permutation in itertools.permutations(parent):
                if beaver_dist_permutation[0] % 2 == 0 and beaver_dist_permutation[0] != 0:
                    half = beaver_dist_permutation[0] // 2
                    new_beaver_dist = tuple(sorted((half, beaver_dist_permutation[1] + half, beaver_dist_permutation[2])))
                    if new_beaver_dist not in all_distributions:
                        yield generation_num, new_beaver_dist
                        generation.append(new_beaver_dist)
                        all_distributions.add(new_beaver_dist)
        if not generation:
            break
        last_generation = generation
        generation_num += 1


def get_LLL_generate(beaver_dist):
    beaver_dist = tuple(sorted(beaver_dist))
    for i, beaver_distribution in generate_beaver_distributions(sum(beaver_dist)):
        if beaver_dist == beaver_distribution:
            return i
    raise ValueError("No beaver distribution found")


def get_LLL(beaver_dist):
    beaver_dist = tuple(sorted(beaver_dist))
    generations, _ = create_beaver_distributions(sum(beaver_dist))
    for i, generation in enumerate(generations):
        if beaver_dist in generation:
            return i
    raise ValueError


def get_telepaartien(beaver_dist):
    beaver_dist = tuple(sorted(beaver_dist))
    _, dists = create_beaver_distributions(sum(beaver_dist))
    way = [beaver_dist]
    while True:
        beaver_dist = dists[way[-1]]
        if beaver_dist is None:
            return way
        way.append(beaver_dist)


if __name__ == "__main__":
    for dist in (
            (2, 4, 7),
            (3, 5, 7),
            (80, 64, 32)
    ):
        print(f"LLL ({dist[0]},{dist[1]},{dist[2]}) = {get_LLL(dist)}")
        print(f"Telepaartien für ({dist[0]},{dist[1]},{dist[2]}): {get_telepaartien(dist)}")
    print("\n n | L(n)")
    for n in range(1, 101):
        beaver_distributions, all_dists = create_beaver_distributions(n)
        lll = len(beaver_distributions) - 1
        print(f"{n:2} | {lll:2}  (size={len(all_dists)})")
        for l in beaver_distributions:
            print(l)
        print()
