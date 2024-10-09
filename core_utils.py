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

def check_deviation(partition, deviation_candidate):
    """
    deviation_candidate が現在のパーティションから離脱することによってスコアが改善するかをチェックする。

    :param partition: 現在のプレイヤーのパーティション。
    :param deviation_candidate: 離脱を検討するプレイヤーの部分集合。
    :return: スコアがすべての条件で改善する場合 True、それ以外は False。
    """
    remaining = get_remaining_group(partition, deviation_candidate)

    current_scores = partition_utils.score_partition_as_dict(partition)

    if len(remaining) == 0:
        new_partition = [deviation_candidate]
        new_scores = partition_utils.score_partition_as_dict(new_partition)

        for player in deviation_candidate:
            if not (current_scores[player] > new_scores[player]):
                return False

        return True

    for remaining_partition in partition_utils.get_partitions(remaining):
        new_partition = [deviation_candidate] + remaining_partition
        new_scores = partition_utils.score_partition_as_dict(new_partition)

        for player in deviation_candidate:
            if not (current_scores[player] > new_scores[player]):
                return False
            
    return True

def print_all_deviation(data, subsets):
    """
    各パーティションに対して、各サブセットがデビエーションするかどうかを出力する。

    :param data: プレイヤーのリスト。
    :param subsets: data から生成された全ての部分集合のリスト。
    """
    partitions = list(partition_utils.get_partitions(data))
    for partition in partitions:
        print(f"Partition: {partition}")
        for subset in subsets:
            result = check_deviation(partition, subset)
            print(f"Subset: {subset}, Deviation: {result}")