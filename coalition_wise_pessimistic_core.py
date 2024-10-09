import partition_utils
import core_utils

def find_pessimistic_core(data, subsets):
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
            result = core_utils.check_deviation(partition, subset)
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
    data = [1, 2, 3, 4, 5, 6]

    subsets = core_utils.get_subsets(data)

    find_pessimistic_core(data, subsets)

if __name__ == '__main__':
    main()
