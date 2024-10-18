import itertools
import csv
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

def write_to_csv(partitions, scores_list, core_status, filename="output.csv"):
    """
    ペシミスティックコアの結果（パーティション、スコア、コアかどうか）をCSVに出力する関数。

    :param partitions: 各代表パーティションのリスト。
    :param scores_list: 各パーティションのスコアリスト。
    :param core_status: ペシミスティックコアかどうかのステータスリスト。
    :param filename: CSVファイルの名前（デフォルト: "output.csv"）。
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

def get_output_function(output_type="cli"):
    """
    出力のための関数を返す。
    
    :param output_type: 出力方法（"cli" または "csv"）
    :return: CLIまたはCSV出力の関数
    """
    if output_type == "csv":
        return write_to_csv
    return print_to_cli
