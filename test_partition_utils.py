import pytest
from partition_utils import (
    get_partitions,
    score_partition_as_list,
    score_partition_as_dict,
    score_partitions,
    symmetry,
    group_by_symmetries,
    get_representative_partitions
)

def test_get_partitions():
    # サンプルデータ [1, 2, 3] に対する全ての可能なパーティションをテスト
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
    # サンプルパーティション [[1, 2], [3]] に対するスコア計算（リスト形式）
    partition = [[1, 2], [3]]
    scores = score_partition_as_list(partition)
    # n = (2 + 1) ^ 2 = 9, グループごとのスコア: [18, 18, 9]
    expected_scores = [18, 18, 9]
    assert scores == expected_scores

def test_score_partition_as_dict():
    # サンプルパーティション [[1, 2], [3]] に対するスコア計算（辞書形式）
    partition = [[1, 2], [3]]
    scores_dict = score_partition_as_dict(partition)
    # 各プレイヤーに対応するスコア: 1と2が18、3が9
    expected_scores_dict = {1: 18, 2: 18, 3: 9}
    assert scores_dict == expected_scores_dict

def test_score_partitions():
    # サンプルデータ [[1, 2], [3]] と [[1], [2, 3]] に対するスコア計算
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
    # スコアの対称性をテスト
    scores = [18, 9, 18]
    result = symmetry(scores)
    expected_result = (9, 18, 18)
    assert result == expected_result

def test_group_by_symmetries():
    # パーティションをスコアに基づいてシンメトリーでグループ化
    partitions = [[[1, 2], [3]], [[1], [2, 3]]]
    scores_list = score_partitions(partitions)
    grouped = group_by_symmetries(scores_list)
    expected_grouped = {
        (9, 18, 18): [((1, 2), (3,)), ((1,), (2, 3))]
    }
    assert grouped == expected_grouped

def test_get_representative_partitions():
    # シンメトリーグループから代表パーティションを抽出するテスト
    grouped_symmetries = {
        (9, 18, 18): [((1, 2), (3,)), ((1,), (2, 3))],
        (16, 16, 16): [((1,), (2,), (3,))]
    }
    representative_partitions = get_representative_partitions(grouped_symmetries)
    # 期待される代表パーティション
    expected_representatives = [
        [[1, 2], [3]],
        [[1], [2], [3]]
    ]
    assert representative_partitions == expected_representatives

if __name__ == "__main__":
    pytest.main()
