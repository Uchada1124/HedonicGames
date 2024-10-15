import partition_utils
import core_utils
import csv

def check_partition_wise_pessimistic_deviation(partition, deviation_candidate): 
    """
    deviation_candidate の全ての部分集合 (partition pattern) に対して、remaining の全ての分割において
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

def process_partition_wise_pessimistic_core(data, subsets):
    """
    全ての代表パーティションに対してペシミスティックコアをチェックし、パーティション、スコア、コアかどうかのリストを生成する。

    :param data: プレイヤーのリスト。
    :param subsets: 全ての部分集合を含むリスト。
    :return: パーティション、スコアリスト、コアかどうかのリストをタプルで返す。
    """
    partitions = list(partition_utils.get_partitions(data))
    scores_list = partition_utils.score_partitions(partitions)
    grouped_symmetries = partition_utils.group_by_symmetries(scores_list)
    representative_partitions = partition_utils.get_representative_partitions(grouped_symmetries)

    core_status_list = []
    all_scores = []

    for partition in representative_partitions:
        all_false = True
        for subset in subsets:
            result = check_partition_wise_pessimistic_deviation(partition, subset)
            if result:
                all_false = False
                break

        core_status = "Yes" if all_false else "No"
        core_status_list.append(core_status)
        all_scores.append(partition_utils.score_partition_as_list(partition))
    
    return representative_partitions, all_scores, core_status_list

def write_to_csv(partitions, scores_list, core_status, filename="partition_wise_pessimistic_core_output.csv"):
    """
    ペシミスティックコアの結果（パーティション、スコア、コアかどうか）をCSVに出力する関数。

    :param partitions: 各代表パーティションのリスト。
    :param scores_list: 各パーティションのスコアリスト。
    :param core_status: ペシミスティックコアかどうかのステータスリスト。
    :param filename: CSVファイルの名前（デフォルト: "partition_wise_pessimistic_core_output.csv"）。
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Partition", "Scores", "Pessimistic Core"])
        for partition, score, core in zip(partitions, scores_list, core_status):
            writer.writerow([partition, score, core])

def print_to_cli(partitions, scores_list, core_status):
    """
    ペシミスティックコアの結果（パーティション、スコア、コアかどうか）をCLIに出力する関数。

    :param partitions: 各代表パーティションのリスト。
    :param scores_list: 各パーティションのスコアリスト。
    :param core_status: ペシミスティックコアかどうかのステータスリスト。
    """
    for partition, score, core in zip(partitions, scores_list, core_status):
        print(f"Partition: {partition}")
        print(f"Scores: {score}")
        print(f"Pessimistic Core: {core}")
        print("-" * 50)

def find_and_output_pessimistic_core(data, subsets, output_type="cli", filename="partition_wise_pessimistic_core_output.csv"):
    """
    ペシミスティックコアの結果をCLIまたはCSVに出力する。

    :param data: プレイヤーのリスト。
    :param subsets: 全ての部分集合を含むリスト。
    :param output_type: 出力方法を指定（"cli" または "csv"）。
    :param filename: CSV出力の場合のファイル名（デフォルト: "partition_wise_pessimistic_core_output.csv"）。
    """
    partitions, scores_list, core_status_list = process_partition_wise_pessimistic_core(data, subsets)

    if output_type == "cli":
        print_to_cli(partitions, scores_list, core_status_list)
    elif output_type == "csv":
        write_to_csv(partitions, scores_list, core_status_list, filename)

def main():
    """
    メイン関数として、与えられたプレイヤーのデータを使ってペシミスティックコアの探索を行い、結果を出力する。
    出力はCLIまたはCSVで指定可能。
    """
    n = 5
    data = list(range(1, n+1))
    subsets = core_utils.get_subsets(data)
    output_type = "cli"
    # output_type = "csv"
    find_and_output_pessimistic_core(data, subsets, output_type)

if __name__ == '__main__':
    main()
