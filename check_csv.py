import pandas as pd
import ast

def main():
    # n=3~13のPartitionがcoalition-wise pessimistic coreであるかとpartition-wise pessimistic coreであるかを判定したcsv
    df = pd.read_csv('./input/n_3_13.csv')
    # print(df.head())
    # print(print(df.isnull().all()))
    
    # Coalition-wise pessimistic coreだが, partition-wise pessimistic coreではないpartitionのdf
    target_df = df[(df['Coalition-wise'] == 'Yes') & (df['Partition-wise'] == 'No')].copy()
    # print(target_df)
    target_df.to_csv('./output/coalition_true_partition_false_core_results.csv', index=False)

    # その中からパーティション内の提携の数が2の時のパーティション
    target_df['Partition'] = target_df['Partition'].apply(ast.literal_eval)
    two_partition_df = target_df[target_df['Partition'].apply(lambda x: len(x) == 2)]
    # print(two_partition_df)
    two_partition_df.to_csv('./output/two_partitions_core_analysis_n3_13.csv', index=False)

if __name__ == '__main__':
    main()
