import partition_utils
import core_utils

def check_partition_wise_pessimistic_deviation(partition, deviation_candidate):
    """
    deviation_candidate の全てのパーティション (分割パターン) に対して
    check_coalition_wise_pessimistic_deviation を実行し、1つでも deviation が
    成立するパターンがあれば True を返し、どれも成立しなければ False を返す。

    :param partition: 現在のプレイヤーのパーティション。
    :param deviation_candidate: 離脱を検討するプレイヤーの部分集合。
    :return: 1つでもスコアが改善するパターンがあれば True、それ以外は False。
    """
    deviation_partitions = list(partition_utils.get_partitions(deviation_candidate))

    for partition_pattern in deviation_partitions:
        if core_utils.check_coalition_wise_pessimistic_deviation(partition, partition_pattern):
            return True
    
    return False


def print_all_partition_wise_pessimistic_deviation(data, subsets):
    """
    各パーティションに対して、各サブセットがデビエーションするかどうかを出力する。

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
    メイン関数として、プレイヤーのデータを使ってペシミスティックコアの探索を行う。
    """
    n = 3
    data = list(range(1, n+1))

    subsets = core_utils.get_subsets(data)

    find_and_print_pessimistic_core(data, subsets)

if __name__ == '__main__':
    main()
