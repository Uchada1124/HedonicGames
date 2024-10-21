import pytest
from utils.partition_utils import (
    get_partitions,
    score_partition_as_list,
    score_partition_as_dict,
    score_partitions,
    symmetry,
    group_by_symmetries,
    get_representative_partitions
)

def test_get_partitions():
    players = [1, 2, 3]
    partitions = list(get_partitions(players))
    expected_partitions = [
        [[1, 2, 3]],
        [[1, 2], [3]],
        [[1, 3], [2]],
        [[2, 3], [1]],
        [[1], [2], [3]]
    ]
    assert sorted([sorted(p) for p in partitions]) == sorted([sorted(p) for p in expected_partitions])

def test_score_partition_as_list():
    partition = [[1, 2], [3]]
    scores = score_partition_as_list(partition)
    expected_scores = [18, 18, 9]
    assert scores == expected_scores

def test_score_partition_as_dict():
    partition = [[1, 2], [3]]
    scores_dict = score_partition_as_dict(partition)
    expected_scores_dict = {1: 18, 2: 18, 3: 9}
    assert scores_dict == expected_scores_dict

def test_score_partitions():
    partitions = [[[1, 2], [3]], [[1], [2, 3]]]
    scores_dict = score_partitions(partitions, return_type='dict')
    expected_scores_dict = {
        ((1, 2), (3,)): {1: 18, 2: 18, 3: 9},
        ((1,), (2, 3)): {1: 9, 2: 18, 3: 18}
    }
    assert scores_dict == expected_scores_dict

    scores_list = score_partitions(partitions)
    expected_scores_list = {
        ((1, 2), (3,)): [18, 18, 9],
        ((1,), (2, 3)): [9, 18, 18]
    }
    assert scores_list == expected_scores_list

def test_symmetry():
    scores = [18, 9, 18]
    result = symmetry(scores)
    expected_result = (9, 18, 18)
    assert result == expected_result

def test_group_by_symmetries():
    partitions = [[[1, 2], [3]], [[1], [2, 3]]]
    scores_list = score_partitions(partitions)
    grouped = group_by_symmetries(scores_list)
    expected_grouped = {
        (9, 18, 18): [((1, 2), (3,)), ((1,), (2, 3))]
    }
    assert grouped == expected_grouped

def test_get_representative_partitions():
    grouped_symmetries = {
        (9, 18, 18): [((1, 2), (3,)), ((1,), (2, 3))],
        (16, 16, 16): [((1,), (2,), (3,))]
    }
    representative_partitions = get_representative_partitions(grouped_symmetries)
    expected_representatives = [
        [[1, 2], [3]],
        [[1], [2], [3]]
    ]
    assert representative_partitions == expected_representatives

if __name__ == "__main__":
    pytest.main()
