import partition_utils
import core_utils

def check_partition_wise_pessimistic_deviation(partition, deviation_candidate): 
    """
    deviation_candidateの全ての部分集合 (partition pattern) に対して、remaining の全ての分割において
    deviation_candidate のスコアが改善する場合を確認し、deviation が可能かどうかを判断する。

    :param partition: 現在のプレイヤーのパーティション (リストのリスト)。
    :param deviation_candidate: 離脱を検討するプレイヤーの部分集合 (リスト)。
    :return: 1つでもスコアが改善するパターンがあれば True、それ以外は False。
    """
    remaining = core_utils.get_remaining_group(partition, deviation_candidate)
    current_scores = partition_utils.score_partition_as_dict(partition)
    deviation_partitions = list(partition_utils.get_partitions(deviation_candidate))

    for partition_pattern in deviation_partitions:
        all_improve = True

        if len(remaining) == 0:
            new_partition = partition_pattern
            new_scores = partition_utils.score_partition_as_dict(new_partition)

            for player in deviation_candidate:
                if not (current_scores[player] > new_scores[player]):
                    all_improve = False
                    break

        else:
            for remaining_partition in partition_utils.get_partitions(remaining):
                new_partition = partition_pattern + remaining_partition
                new_scores = partition_utils.score_partition_as_dict(new_partition)

                for player in deviation_candidate:
                    if not (current_scores[player] > new_scores[player]):
                        all_improve = False
                        break

                if not all_improve:
                    break

        if all_improve:
            return True

    return False

def print_all_partition_wise_pessimistic_deviation(data, subsets):
    """
    全てのパーティションと各サブセット (subsets) に対して、deviation が可能かどうかを出力する。

    :param data: プレイヤーのリスト。
    :param subsets: data から生成された全ての部分集合のリスト。
    """
    partitions = list(partition_utils.get_partitions(data))
    for partition in partitions:
        print(f"Partition: {partition}")
        for subset in subsets:
            result = check_partition_wise_pessimistic_deviation(partition, subset)
            print(f"Subset: {subset}, Deviation: {result}")

def find_and_print_pessimistic_core(data, subsets):
    """
    全ての代表パーティションに対して、全ての部分集合のデビエーションをチェックし、
    1つでもデビエーションが成立しないパーティションをペシミスティックコアとして出力する。

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
            result = check_partition_wise_pessimistic_deviation(partition, subset)
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
    メイン関数として、与えられたプレイヤーのデータを使ってペシミスティックコアの探索を行う。
    """
    n = 6
    data = list(range(1, n+1))

    subsets = core_utils.get_subsets(data)

    find_and_print_pessimistic_core(data, subsets)

if __name__ == '__main__':
    main()
