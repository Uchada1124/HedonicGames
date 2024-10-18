import pytest
from core_utils import get_subsets, get_remaining_group  # テスト対象の関数をインポート

def test_get_subsets():
    """
    get_subsets 関数が n=3 のプレイヤーリストに対して期待される全ての部分集合を返すかをテストする。
    """
    players = [1, 2, 3]
    expected_subsets = [
        [1], [2], [3],
        [1, 2], [1, 3], [2, 3],
        [1, 2, 3]
    ]
    
    subsets = get_subsets(players)
    
    for expected in expected_subsets:
        assert sorted(expected) in [sorted(subset) for subset in subsets], f"Expected {expected} to be in subsets"

def test_get_remaining_group():
    """
    get_remaining_group 関数が指定された deviation_candidate を除いた後の正しい残りのプレイヤーグループを返すかをテストする。
    """
    # テストケース1: パーティション[[1, 2], [3]]から[1]が離脱した場合
    partition = [[1, 2], [3]]
    deviation_candidate = [1]
    expected_remaining = [2, 3]
    
    remaining = get_remaining_group(partition, deviation_candidate)
    
    assert sorted(remaining) == sorted(expected_remaining), f"Expected remaining to be {expected_remaining}, but got {remaining}"
    
    # テストケース2: パーティション[[1, 2], [3]]から[2, 3]が離脱した場合
    deviation_candidate = [2, 3]
    expected_remaining = [1]
    
    remaining = get_remaining_group(partition, deviation_candidate)
    
    assert sorted(remaining) == sorted(expected_remaining), f"Expected remaining to be {expected_remaining}, but got {remaining}"
