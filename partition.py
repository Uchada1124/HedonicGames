def partition(collection):
    if len(collection) == 1:
        yield [collection]
        return

    first = collection[0]
    for smaller in partition(collection[1:]):
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[first] + subset] + smaller[n+1:]
        yield [[first]] + smaller

def symmetry(collection):
    return tuple(sorted(tuple(sorted(group)) for group in collection))

def main():
    data = [1, 2, 3, 4, 5, 6]

    partition_scores_dict = {}

    for p in partition(data):
        n = (len(p) + 1) ** 2
        scores = [n * len(group) for group in p]
        partition_scores_dict[tuple(map(tuple, p))] = scores

    for part, scores in partition_scores_dict.items():
        print(f"Partition {part}: {scores}")

if __name__ == '__main__':
    main()