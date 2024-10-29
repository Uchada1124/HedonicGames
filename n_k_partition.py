import utils.core_utils as core_utils
import partition_wise_pessimistic_core
import coalition_wise_pessimistic_core
import csv

def bool_to_yes_no(value):
    """
    True/False を Yes/No に変換する関数
    """
    return "Yes" if value else "No"

def output_to_cli(k, n, coalition_is_core, partition_is_core):
    """
    CLIに出力する関数
    """
    print(f"\nResults for k = {k}")
    print(f"The {k}, n-{k} partition for {n} players:")
    print(f"  coalition-wise: {bool_to_yes_no(coalition_is_core)}")
    print(f"  partition-wise: {bool_to_yes_no(partition_is_core)}")

def output_to_csv(k, results, filename="output.csv"):
    """
    CSVに出力する関数。kごとに区切って出力。
    """
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([f"k = {k}"])
        writer.writerow(["n", "coalition-wise", "partition-wise"])
        for n, coalition_is_core, partition_is_core in results:
            writer.writerow([n, bool_to_yes_no(coalition_is_core), bool_to_yes_no(partition_is_core)])
        writer.writerow([])  # 空行で区切り

def main():
    """
    CLIまたはCSV出力に対応したメイン関数
    """
    output_type = "csv"  # "cli" or "csv"
    filename = "./output/n_k_partition_output.csv"
    start = 3
    end = 12
    k_values = [1, 2, 3, 4, 5, 6]  # チェックする k の値のリスト（例として1人提携と2人提携を確認）

    # CSVファイルの初期化
    if output_type == "csv":
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Calculation of pessimistic core for various k and n"])

    for k in k_values:
        print(f"\nChecking for k = {k}")
        results = []  # この k における n の結果を保存

        for n in range(start, end + 1):
            if k >= n:
                continue  # kがn以上の場合はスキップ

            print(f"  Checking for n = {n} with partition {k}, {n-k}")
            data = list(range(1, n + 1))
            target = [list(range(1, k + 1)), list(range(k + 1, n + 1))]  # k人と n-k 人のパーティション
            subsets = core_utils.get_subsets(data)

            partition_is_core = True
            coalition_is_core = True

            for subset in subsets:
                if partition_is_core:
                    partition_wise_result = partition_wise_pessimistic_core.check_partition_wise_pessimistic_deviation(target, subset)
                if coalition_is_core:
                    coalition_wise_result = coalition_wise_pessimistic_core.check_coalition_wise_pessimistic_deviation(target, subset)
                
                if partition_wise_result:
                    partition_is_core = False
                if coalition_wise_result:
                    coalition_is_core = False
                
                if not partition_is_core and not coalition_is_core:
                    break

            # 結果をリストに追加
            results.append((n, coalition_is_core, partition_is_core))

        # CLIまたはCSVに出力
        if output_type == "cli":
            for n, coalition_is_core, partition_is_core in results:
                output_to_cli(k, n, coalition_is_core, partition_is_core)
        elif output_type == "csv":
            output_to_csv(k, results, filename)

if __name__ == '__main__':
    main()
