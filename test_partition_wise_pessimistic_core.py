import pytest
from partition_wise_pessimistic_core import process_partition_wise_pessimistic_core  # テスト対象の関数をインポート
import core_utils

@pytest.mark.parametrize("n, expected_results", [
    (3, [
        ([[1, 2, 3]], "Yes"),
        ([[1], [2, 3]], "No"),
        ([[1], [2], [3]], "No")
    ]),
    (5, [
        ([[1, 2, 3, 4, 5]], "Yes"),
        ([[1], [2, 3, 4, 5]], "No"),
        ([[1, 2], [3, 4, 5]], "Yes"),
        ([[1], [2], [3, 4, 5]], "No"),
        ([[1], [2, 3], [4, 5]], "Yes"),
        ([[1], [2], [3], [4, 5]], "No"),
        ([[1], [2], [3], [4], [5]], "No")
    ])
])
def test_partition_wise_pessimistic_core(n, expected_results):
    """
    n=3およびn=5の時のペシミスティックコア判定の結果が期待通りか確認するテスト。
    """
    data = list(range(1, n+1))
    subsets = core_utils.get_subsets(data)

    partitions, _, core_status_list = process_partition_wise_pessimistic_core(data, subsets)

    for expected_partition, expected_core in expected_results:
        sorted_partitions = [sorted(part) for part in partitions]
        assert [sorted(part) for part in expected_partition] in sorted_partitions
        idx = sorted_partitions.index([sorted(part) for part in expected_partition])
        assert core_status_list[idx] == expected_core
