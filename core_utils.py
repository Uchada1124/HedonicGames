import itertools
import partition_utils

def get_subsets(players):
    """
    与えられたプレイヤーのリストから非空部分集合を全て生成する。

    :param players: 部分集合を生成するプレイヤーのリスト。
    :return: 非空の全ての部分集合を含むリスト。
    """
    n = len(players)
    all_combinations = itertools.product(range(2), repeat=n)

    subsets = []
    for combination in all_combinations:
        subset = [players[i] for i in range(n) if combination[i] == 1]
        if subset:
            subsets.append(subset)
    
    return subsets

def get_remaining_group(partition, deviation_candidate):
    """
    指定した deviation_candidate を除いた後の残りのプレイヤーグループを生成する。

    :param partition: 現在のプレイヤーのパーティション（グループのリスト）。
    :param deviation_candidate: パーティションから除外するプレイヤーのリスト。
    :return: deviation_candidate を除いた後のプレイヤーを含むリスト。
    """
    remaining_group = []

    for group in partition:
        updated_group = [player for player in group if player not in deviation_candidate]
        if updated_group:
            remaining_group.extend(updated_group)

    return remaining_group