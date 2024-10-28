import utils.core_utils as core_utils
import partition_wise_pessimistic_core
import coalition_wise_pessimistic_core
import csv

def bool_to_yes_no(value):
    """
    True/False を Yes/No に変換する関数
    """
    return "Yes" if value else "No"

def output_to_cli(n, coalition_is_core, partition_is_core):
    """
    CLIに出力する関数
    """
    print(f"The 1, n-1 partition for {n} players:")
    print(f"  coalition-wise: {bool_to_yes_no(coalition_is_core)}")
    print(f"  partition-wise: {bool_to_yes_no(partition_is_core)}")

def output_to_csv(n, coalition_is_core, partition_is_core, filename="output.csv"):
    """
    CSVに出力する関数
    """
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([n, bool_to_yes_no(coalition_is_core), bool_to_yes_no(partition_is_core)])

def main():
    """
    CLIまたはCSV出力に対応したメイン関数
    """
    output_type = "csv"  # "cli" or "csv"
    filename = "./output/n_k_partition_output.csv"
    start = 3
    end = 12

    # CSVファイルの場合、ヘッダーを書き込む
    if output_type == "csv":
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["n", "coalition-wise", "partition-wise"])

    for n in range(start, end + 1):
        print(f"\nChecking for n = {n}")
        data = list(range(1, n+1))
        target = [[1], list(range(2, n+1))]  # パーティション [1, n-1]
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

        # CLIまたはCSVに出力
        if output_type == "cli":
            output_to_cli(n, coalition_is_core, partition_is_core)
        elif output_type == "csv":
            output_to_csv(n, coalition_is_core, partition_is_core, filename)

if __name__ == '__main__':
    main()
