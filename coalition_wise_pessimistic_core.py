import itertools
import partition_utils

def get_subsets(players):
    n = len(players)
    all_combinations = itertools.product(range(2), repeat=n)

    subsets = []
    for combination in all_combinations:
        subset = [players[i] for i in range(n) if combination[i] == 1]
        if subset:
            subsets.append(subset)
    
    return subsets

def get_remaining_group(partition, deviation_candidate):
    remaining_group = []

    for group in partition:
        updated_group = [player for player in group if player not in deviation_candidate]
        if updated_group:
            remaining_group.extend(updated_group)

    return remaining_group

def check_deviation(partition, deviation_candidate):
    remaining = get_remaining_group(partition, deviation_candidate)

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

def print_all_deviation(data, subsets):
    partitions = list(partition_utils.get_partitions(data))
    for partition in partitions:
        print(f"Partition: {partition}")
        for subset in subsets:
            result = check_deviation(partition, subset)
            print(f"Subset:{subset}, Deviation:{result}")

def find_pessimistic_core(data, subsets):
    partitions = list(partition_utils.get_partitions(data))
    scores_list = partition_utils.score_partitions(partitions)
    grouped_symmetries = partition_utils.group_by_symmetries(scores_list)
    representative_partitions = partition_utils.get_representative_partitions(grouped_symmetries)

    for partition in representative_partitions:
        print(f"Partition: {partition}")
        
        all_false = True
        for subset in subsets:
            result = check_deviation(partition, subset)
            print(f"Subset: {subset}, Deviation: {result}")
            
            if result:
                all_false = False
                break
        
        if all_false:
            print(f"Partition: {partition} is a Pessimistic Core")



def main():
    # Example usage
    data = [1, 2, 3, 4, 5]

    subsets = get_subsets(data)
    # print_all_deviation(data, subsets)
    find_pessimistic_core(data, subsets)

if __name__ == '__main__':
    main()
