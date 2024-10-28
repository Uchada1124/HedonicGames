# import utils.partition_utils as partition_utils
# import utils.core_utils as core_utils
# import csv

# def check_coalition_wise_pessimistic_deviation(partition, deviation_candidate):
#     """
#     deviation_candidate（プレイヤーの部分集合）が現在のパーティションから離脱することによって
#     スコアが改善されるかをチェックする関数。

#     :param partition: 現在のプレイヤーのパーティション（リストのリスト）。
#     :param deviation_candidate: 離脱を検討するプレイヤーの部分集合（リスト）。
#     :return: スコアが全ての条件で改善される場合 True、それ以外は False を返す。
#     """
#     remaining = core_utils.get_remaining_group(partition, deviation_candidate)
#     current_scores = partition_utils.score_partition_as_dict(partition)

#     if len(remaining) == 0:
#         new_partition = [deviation_candidate]
#         new_scores = partition_utils.score_partition_as_dict(new_partition)

#         for player in deviation_candidate:
#             if not (current_scores[player] > new_scores[player]):
#                 return False
#         return True

#     for remaining_partition in partition_utils.get_partitions(remaining):
#         new_partition = [deviation_candidate] + remaining_partition
#         new_scores = partition_utils.score_partition_as_dict(new_partition)

#         for player in deviation_candidate:
#             if not (current_scores[player] > new_scores[player]):
#                 return False

#     return True

# def process_coalition_wise_pessimistic_core(data, subsets):
#     """
#     ペシミスティックコアをチェックし、パーティション、スコア、コアかどうかのリストを生成する関数。
    
#     :param data: プレイヤーのリスト。
#     :param subsets: 全ての部分集合を含むリスト。
#     :return: パーティション、スコアリスト、コアかどうかのリストをタプルで返す。
#     """
#     partitions = list(partition_utils.get_partitions(data))
#     scores_list = partition_utils.score_partitions(partitions)
#     grouped_symmetries = partition_utils.group_by_symmetries(scores_list)
#     representative_partitions = partition_utils.get_representative_partitions(grouped_symmetries)

#     core_status_list = []
#     all_scores = []

#     for partition in representative_partitions:
#         all_false = True
#         for subset in subsets:
#             result = check_coalition_wise_pessimistic_deviation(partition, subset)
#             if result:
#                 all_false = False
#                 break

#         core_status = "Yes" if all_false else "No"
#         core_status_list.append(core_status)
#         all_scores.append(partition_utils.score_partition_as_list(partition))
    
#     return representative_partitions, all_scores, core_status_list

# def write_to_csv(partitions, scores_list, core_status, filename="colition_wise_pessimistic_core_output.csv"):
#     """
#     ペシミスティックコアの結果（パーティション、スコア、コアかどうか）をCSVに出力する関数。

#     :param partitions: 各代表パーティションのリスト。
#     :param scores_list: 各パーティションのスコアリスト。
#     :param core_status: ペシミスティックコアかどうかのステータスリスト。
#     :param filename: CSVファイルの名前。デフォルトは "colition_wise_pessimistic_core_output.csv"。
#     """
#     with open(filename, mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(["Partition", "Scores", "Pessimistic Core"])
#         for partition, score, core in zip(partitions, scores_list, core_status):
#             writer.writerow([partition, score, core])

# def print_to_cli(partitions, scores_list, core_status):
#     """
#     ペシミスティックコアの結果（パーティション、スコア、コアかどうか）をCLIに出力する関数。

#     :param partitions: 各代表パーティションのリスト。
#     :param scores_list: 各パーティションのスコアリスト。
#     :param core_status: ペシミスティックコアかどうかのステータスリスト。
#     """
#     for partition, score, core in zip(partitions, scores_list, core_status):
#         print(f"Partition: {partition}")
#         print(f"Scores: {score}")
#         print(f"Pessimistic Core: {core}")
#         print("-" * 50)

# def find_and_output_pessimistic_core(data, subsets, output_type="cli", filename="./output/colition_wise_pessimistic_core_output.csv"):
#     """
#     ペシミスティックコアの結果をCLIまたはCSVに出力する関数。

#     :param data: プレイヤーのリスト。
#     :param subsets: 全ての部分集合を含むリスト。
#     :param output_type: 出力方法を指定（"cli" または "csv"）。
#     :param filename: CSV出力の場合のファイル名（デフォルトは "./output/colition_wise_pessimistic_core_output.csv"）。
#     """
#     partitions, scores_list, core_status_list = process_coalition_wise_pessimistic_core(data, subsets)
#     output_function = core_utils.get_output_function(output_type)
#     if output_type == "csv":
#         output_function(partitions, scores_list, core_status_list, filename)
#     else:
#         output_function(partitions, scores_list, core_status_list)

# def main():
#     """
#     メイン関数として、プレイヤーのデータを使ってペシミスティックコアの探索を行い、結果を出力する。
#     出力はCLIまたはCSVで指定可能。
#     """
#     n = 6
#     data = list(range(1, n+1))
#     subsets = core_utils.get_subsets(data)
#     # output_type="cli"
#     output_type = "csv"
#     find_and_output_pessimistic_core(data, subsets, output_type)

# if __name__ == '__main__':
#     main()

import utils.partition_utils as partition_utils
import utils.core_utils as core_utils
import csv
from fractions import Fraction

def check_coalition_wise_pessimistic_deviation(partition, deviation_candidate):
    """
    deviation_candidate（プレイヤーの部分集合）が現在のパーティションから離脱することによって
    スコアが改善されるかをチェックする関数。
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

def convert_scores_to_fraction(scores):
    """
    スコアリストを分数に変換する関数。
    20なら1/20のように変換。0の場合はゼロのまま保持。
    
    :param scores: スコアリスト。
    :return: 分数に変換されたスコアリスト。
    """
    return [str(Fraction(1, s)) if s != 0 else '0' for s in scores]

def process_coalition_wise_pessimistic_core(data, subsets):
    """
    ペシミスティックコアをチェックし、パーティション、スコア、コアかどうかのリストを生成する関数。
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
            result = check_coalition_wise_pessimistic_deviation(partition, subset)
            if result:
                all_false = False
                break

        core_status = "Yes" if all_false else "No"
        core_status_list.append(core_status)
        all_scores.append(partition_utils.score_partition_as_list(partition))
    
    return representative_partitions, all_scores, core_status_list

def write_to_csv(partitions, scores_list, core_status, filename="colition_wise_pessimistic_core_output.csv"):
    """
    ペシミスティックコアの結果（パーティション、スコア、コアかどうか）をCSVに出力する関数。
    スコアは逆数の分数に変換されて出力される。
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Partition", "Reciprocal Scores", "Pessimistic Core"])
        for partition, score, core in zip(partitions, scores_list, core_status):
            reciprocal_scores = convert_scores_to_fraction(score)
            writer.writerow([partition, reciprocal_scores, core])

def print_to_cli(partitions, scores_list, core_status):
    """
    ペシミスティックコアの結果（パーティション、スコア、コアかどうか）をCLIに出力する関数。
    """
    for partition, score, core in zip(partitions, scores_list, core_status):
        reciprocal_scores = convert_scores_to_fraction(score)
        print(f"Partition: {partition}")
        print(f"Reciprocal Scores: {reciprocal_scores}")
        print(f"Pessimistic Core: {core}")
        print("-" * 50)

def find_and_output_pessimistic_core(data, subsets, output_type="cli", filename="./output/coalition_wise_pessimistic_core_output.csv"):
    """
    ペシミスティックコアの結果をCLIまたはCSVに出力する関数。

    :param data: プレイヤーのリスト。
    :param subsets: 全ての部分集合を含むリスト。
    :param output_type: 出力方法を指定（"cli" または "csv"）。
    :param filename: CSV出力の場合のファイル名（デフォルトは "./output/coalition_wise_pessimistic_core_output.csv"）。
    """
    partitions, scores_list, core_status_list = process_coalition_wise_pessimistic_core(data, subsets)
    if output_type == "csv":
        write_to_csv(partitions, scores_list, core_status_list, filename)
    else:
        print_to_cli(partitions, scores_list, core_status_list)

def main():
    """
    メイン関数として、プレイヤーのデータを使ってペシミスティックコアの探索を行い、結果を出力する。
    出力はCLIまたはCSVで指定可能。
    """
    n = 8
    data = list(range(1, n+1))
    subsets = core_utils.get_subsets(data)
    output_type = "csv"  # CLIで出力する場合は "cli" に変更
    find_and_output_pessimistic_core(data, subsets, output_type)

if __name__ == '__main__':
    main()
