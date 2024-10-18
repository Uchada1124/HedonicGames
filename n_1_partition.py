import core_utils
import partition_wise_pessimistic_core

def main():
    n = 7
    data = list(range(1, n+1))
    subsets = core_utils.get_subsets(data)
    cnt = 0
    target = [[1],[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]]
    for subset in subsets:
            result = partition_wise_pessimistic_core.check_partition_wise_pessimistic_deviation(target, subset)
            print(f"Result: {result}")
            if result: cnt+=1

    print(cnt)

if __name__ == '__main__':
      main()