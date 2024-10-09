import partition_utils
import core_utils

def check_coalition_wise_pessimistic_deviation(partition, deviation_candidate):
    """
    deviation_candidate が現在のパーティションから離脱することによってスコアが改善するかをチェックする。

    :param partition: 現在のプレイヤーのパーティション。
    :param deviation_candidate: 離脱を検討するプレイヤーの部分集合。
    :return: スコアがすべての条件で改善する場合 True、それ以外は False。
    """
    remaining = core_utils.get_remaining_group(partition, deviation_candidate)

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


def print_all_coalition_wise_pessimistic_deviation(data, subsets):
    """
    各パーティションに対して、各サブセットがデビエーションするかどうかを出力する。

    :param data: プレイヤーのリスト。
    :param subsets: data から生成された全ての部分集合のリスト。
    """
    partitions = list(partition_utils.get_partitions(data))
    for partition in partitions:
        print(f"Partition: {partition}")
        for subset in subsets:
            result = core_utils.check_coalition_wise_pessimistic_deviation(partition, subset)
            print(f"Subset: {subset}, Deviation: {result}")


def find_and_print_pessimistic_core(data, subsets):
    """
    各代表パーティションに対して、全てのサブセットに対するデビエーションの結果をチェックし、
    全てのデビエーションが False であれば、そのパーティションをペシミスティックコアとする。

    :param data: プレイヤーのリスト。
    :param subsets: data から生成された全ての部分集合のリスト。
    """
    partitions = list(partition_utils.get_partitions(data))
    scores_list = partition_utils.score_partitions(partitions)
    grouped_symmetries = partition_utils.group_by_symmetries(scores_list)
    representative_partitions = partition_utils.get_representative_partitions(grouped_symmetries)

    for partition in representative_partitions:
        print(f"\nPartition: {partition}")
        
        all_false = True
        for subset in subsets:
            result = check_coalition_wise_pessimistic_deviation(partition, subset)
            print(f"Subset: {subset}, Deviation: {result}")
            
            if result:
                all_false = False
                break
        
        if all_false:
            print(f"Partition: {partition} is a Pessimistic Core")
        else:
            print(f"Partition: {partition} is not a Pessimistic Core")

def main():
    """
    メイン関数として、プレイヤーのデータを使ってペシミスティックコアの探索を行う。
    """
    n = 5
    data = list(range(1, n+1))

    subsets = core_utils.get_subsets(data)

    find_and_print_pessimistic_core(data, subsets)

if __name__ == '__main__':
    main()
