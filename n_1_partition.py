import core_utils
import partition_wise_pessimistic_core
import coalition_wise_pessimistic_core 

def main():
    start = 3
    end = 12

    for n in range(start, end + 1):
        print(f"\nChecking for n = {n}")
        data = list(range(1, n+1))
        target = [[1], list(range(2, n+1))]
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
                print(f"The 1, n-1 partition for {n} players:")
                print(f"  coalition-wise: False")
                print(f"  partition-wise: False")
                break
        else:
            print(f"The 1, n-1 partition for {n} players:")
            print(f"  coalition-wise: {coalition_is_core}")
            print(f"  partition-wise: {partition_is_core}")

if __name__ == '__main__':
    main()
