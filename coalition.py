from collections import defaultdict
import csv

def partition(collection):
    if len(collection) == 1:
        yield [collection]
        return

    first = collection[0]
    for smaller in partition(collection[1:]):
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[first] + subset] + smaller[n+1:]
        yield [[first]] + smaller

def symmetry(scores):
    return tuple(sorted(scores))

def main():
    data = [1, 2, 3, 4, 5]

    symmetric_partitions = defaultdict(list)

    for p in partition(data):
        n = (len(p) + 1) ** 2
        scores = [n * len(group) for group in p]
        sym_scores = symmetry(scores)
        symmetric_partitions[sym_scores].append((p, scores))

    for sym_scores, partitions in symmetric_partitions.items():
        print(f"Symmetric Group with Scores {sym_scores}:")
        for part, scores in partitions:
            print(f"  Partition {part}: Scores {scores}")

if __name__ == '__main__':
    main()