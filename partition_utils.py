def get_partitions(players):
    """
    プレイヤーのリストから全ての可能なパーティションを再帰的に生成する。

    :param players: パーティションを行うプレイヤーのリスト。
    :yield: 各可能なパーティション。
    """
    if len(players) == 1:
        yield [players]
        return

    first = players[0]
    for smaller in get_partitions(players[1:]):
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[first] + subset] + smaller[n+1:]
        yield [[first]] + smaller

def score_partition_as_list(partition):
    """
    指定されたパーティション内の各プレイヤーのスコアを計算し、リストとして返す。

    :param partition: グループごとに分けられたプレイヤーのパーティション。
    :return: 各プレイヤーのスコアを順に格納したリスト。
    """
    n = (len(partition) + 1) ** 2
    scores = []
    for group in partition:
        group_score = n * len(group)
        for player in group:
            scores.append(group_score)
    return scores

def score_partition_as_dict(partition):
    """
    指定されたパーティション内の各プレイヤーのスコアを計算し、辞書として返す。

    :param partition: グループごとに分けられたプレイヤーのパーティション。
    :return: 各プレイヤーをキー、そのプレイヤーのスコアを値とする辞書。
    """
    n = (len(partition) + 1) ** 2
    scores_dict = {}
    for group in partition:
        group_score = n * len(group)
        for player in group:
            scores_dict[player] = group_score
    return scores_dict

def score_partitions(partitions, return_type='list'):
    """
    複数のパーティションのスコアを計算し、指定された形式で返す（リストまたは辞書）。

    :param partitions: スコアを計算するパーティションのリスト。
    :param return_type: スコアの返却形式（'list' または 'dict'）。デフォルトは 'list'。
    :return: パーティションをキーとし、そのスコアを値とする辞書（形式は return_type に依存）。
    """
    partition_scores_dict = {}

    for partition in partitions:
        if return_type == 'dict':
            partition_scores_dict[tuple(map(tuple, partition))] = score_partition_as_dict(partition)
        else:
            partition_scores_dict[tuple(map(tuple, partition))] = score_partition_as_list(partition)

    return partition_scores_dict

def symmetry(scores):
    """
    パーティションのシンメトリーを分類するための一意のキーを作成する。

    :param scores: パーティションのスコアリスト。
    :return: シンメトリーの分類に使用するためにソートされたスコアのタプル。
    """
    return tuple(sorted(scores))

def group_by_symmetries(partition_scores):
    """
    パーティションをシンメトリーのスコアに基づいてグループ化する。

    :param partition_scores: パーティションをキー、スコアを値とする辞書。
    :return: シンメトリーキー（ソートされたスコアのタプル）をキー、パーティションリストを値とする辞書。
    """
    symmetries_dict = {}
    for partition, scores in partition_scores.items():
        key = symmetry(scores)
        if key not in symmetries_dict:
            symmetries_dict[key] = []
        symmetries_dict[key].append(partition)
    return symmetries_dict

def get_representative_partitions(grouped_symmetries):
    """
    各シンメトリーグループから代表的なパーティションを抽出し、リスト形式に変換して返す。

    :param grouped_symmetries: シンメトリーキーをキー、パーティションリストを値とする辞書。
    :return: 各シンメトリーグループの代表パーティション（リストのリスト形式）。
    """
    representative_partitions = []

    for symmetry_key, partitions in grouped_symmetries.items():
        if partitions:
            representative_partition = [list(group) for group in partitions[0]]
            representative_partitions.append(representative_partition)

    return representative_partitions

def main():
    """
    パーティションの生成、スコアの計算、シンメトリーグループの作成、
    そして代表パーティションの抽出までの一連の手順を実行する。
    """
    # サンプルデータ
    data = [1, 2, 3]

    # データの全ての可能なパーティションを取得
    partitions = list(get_partitions(data))
    for partition in partitions:
        print(partition)

    # 各パーティションのスコアをリスト形式で計算
    scores_list = score_partitions(partitions)
    print("Scores as List:")
    for partition, scores in scores_list.items():
        print(f"Partition: {partition}, Scores: {scores}")

    # 各パーティションのスコアを辞書形式で計算
    scores_dict = score_partitions(partitions, return_type='dict')
    print("Scores as Dict:")
    for partition, scores in scores_dict.items():
        print(f"Partition: {partition}, Scores: {scores}")

    # スコアに基づいてパーティションをシンメトリーグループ化
    grouped_symmetries = group_by_symmetries(scores_list)
    for symmetry_key, partitions in grouped_symmetries.items():
        print(f"Symmetry Scores: {symmetry_key}")
        for partition in partitions:
            print(f"  Partition: {partition}")

    # シンメトリーグループから代表パーティションを抽出
    representative_partitions = get_representative_partitions(grouped_symmetries)
    print("Representative Partitions:")
    for partition in representative_partitions:
        print(partition)

if __name__ == '__main__':
    main()
