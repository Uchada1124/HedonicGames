import utils.partition_utils as partition_utils
import utils.core_utils as core_utils
import csv
from fractions import Fraction
import time

def check_partition_wise_pessimistic_deviation(partition, deviation_candidate):
    """
    deviation_candidateが現在のパーティションから離脱することでスコアが改善するかをチェックする。
    """
    remaining = core_utils.get_remaining_group(partition, deviation_candidate)
    current_scores = partition_utils.score_partition_as_dict(partition)

    for partition_pattern in partition_utils.get_partitions(deviation_candidate):
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

def convert_scores_to_fraction(scores):
    """
    スコアリストを分数に変換する関数。
    """
    return [str(Fraction(1, s)) if s != 0 else '0' for s in scores]

def process_partition_wise_pessimistic_core(data, subsets):
    """
    partition-wiseペシミスティックコアをチェックし、パーティション、スコア、コアかどうかのリストを生成。
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

def write_to_csv(n, partitions, scores_list, core_status, filename="partition_wise_n_progress_output.csv"):
    """
    計算結果をCSVに書き込む関数。スコアは逆数で出力される。
    """
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([f"n={n}"])
        writer.writerow(["Partition", "Reciprocal Scores", "Pessimistic Core"])
        for partition, score, core in zip(partitions, scores_list, core_status):
            reciprocal_scores = convert_scores_to_fraction(score)
            writer.writerow([partition, reciprocal_scores, core])
        writer.writerow([])

def main():
    """
    メイン関数。8時間で計算できる最大のnを追跡し、進捗をCSVに出力。
    """
    filename = "./output/partition_wise_n_progress_output.csv"
    start_n = 3
    end_n = 100
    max_runtime = 8 * 60 * 60  # 8時間を秒で指定
    start_time = time.time()

    # CSVファイルの初期化
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Partition-wise Pessimistic Core Calculation Progress"])

    for n in range(start_n, end_n + 1):
        elapsed_time = time.time() - start_time
        if elapsed_time >= max_runtime:
            print(f"Time limit reached. Stopping at n = {n - 1}.")
            break

        print(f"\nChecking for n = {n}")
        data = list(range(1, n+1))
        subsets = core_utils.get_subsets(data)

        partitions, scores_list, core_status_list = process_partition_wise_pessimistic_core(data, subsets)
        write_to_csv(n, partitions, scores_list, core_status_list, filename)
        print(f"n = {n} processed and written to {filename}")

    print(f"Finished. Maximum n calculated: {n - 1}")

if __name__ == '__main__':
    main()
