import argparse
import numpy as np
from tqdm import trange
import matplotlib.pyplot as plt


parse = argparse.ArgumentParser(description="小乌龟盲盒模拟程序")
parse.add_argument("-o", "--output", action="store_true", default=False)
parse.add_argument("-s", "--save", action="store_true", default=False)
parse.add_argument("-n", "--numbers", type=int, default=100000)
args = parse.parse_args()


OUTPUT = args.output
SAVE = args.save
MAX_ITER = args.numbers


def init_arr() -> np.ndarray:
    return np.zeros((3, 3), dtype=np.int8)


def add_arr(arr: np.ndarray, res: int, wish: int = 1):
    if res == 0:
        return arr, res
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if arr[i, j] == 0:
                arr[i, j] = np.random.randint(1, 10, dtype=np.int8)
                if arr[i, j] == wish:
                    res += 1
                    if OUTPUT:
                        print("\033[32m[info]: 许愿成功！\033[0m")
                res -= 1
                if res == 0:
                    return arr, res
            else:
                continue
    return arr, res


def test(arr: np.ndarray, res: int, gets: int):
    if (arr[0, 0] != 0) and (arr[0, 0] == arr[0, 1] == arr[0, 2]):
        arr[0, :] = np.zeros((1, 3), dtype=np.int8)
        res += 5
        gets += 3
        if OUTPUT:
            print("\033[32m[info]: 第一行三连！\033[0m")

    
    if (arr[1, 0] != 0) and (arr[1, 0] == arr[1, 1] == arr[1, 2]):
        arr[1, :] = np.zeros((1, 3), dtype=np.int8)
        res += 5
        gets += 3
        if OUTPUT:
            print("\033[32m[info]: 第二行三连！\033[0m")
    
    if (arr[2, 0] != 0) and (arr[2, 0] == arr[2, 1] == arr[2, 2]):
        arr[2, :] = np.zeros((1, 3), dtype=np.int8)
        res += 5
        gets += 3
        if OUTPUT:
            print("\033[32m[info]: 第三行三连！\033[0m")
    
    if (arr[0, 0] != 0) and (arr[0, 0] == arr[1, 0] == arr[2, 0]):
        arr[:, 0] = np.zeros((1, 3), dtype=np.int8)
        res += 5
        gets += 3
        if OUTPUT:
            print("\033[32m[info]: 第一列三连！\033[0m")
    
    if (arr[0, 1] != 0) and (arr[0, 1] == arr[1, 1] == arr[2, 1]):
        arr[:, 1] = np.zeros((1, 3), dtype=np.int8)
        res += 5
        gets += 3
        if OUTPUT:
            print("\033[32m[info]: 第二列三连！\033[0m")
    
    if (arr[0, 2] != 0) and (arr[0, 2] == arr[1, 2] == arr[2, 2]):
        arr[:, 2] = np.zeros((1, 3), dtype=np.int8)
        res += 5
        gets += 3
        if OUTPUT:
            print("\033[32m[info]: 第三列三连！\033[0m")
    
    if (arr[1, 1] != 0) and (arr[0, 0] == arr[1, 1] == arr[2, 2]):
        arr[0, 0] = arr[1, 1] = arr[2, 2] = 0
        res += 5
        gets += 3
        if OUTPUT:
            print("\033[32m[info]: 主对角线三连！\033[0m")
    
    if (arr[1, 1] != 0) and (arr[0, 2] == arr[1, 1] == arr[2, 0]):
        arr[0, 2] = arr[1, 1] = arr[2, 0] = 0
        res += 5
        gets += 3
        if OUTPUT:
            print("\033[32m[info]: 次对角线三连！\033[0m")
    
    tmp_lst = []
    tmp_pos = []
    tmp_idx = 0
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if arr[i, j] != 0:
                if arr[i, j] in tmp_lst:
                    if OUTPUT:
                        print(f"\033[32m[info]: {arr[i, j]} - {arr[i, j]}碰！\033[0m")
                    tmp_idx = tmp_lst.index(arr[i, j])
                    tmp_lst.pop(tmp_idx)
                    arr[tmp_pos.pop(tmp_idx)] = 0
                    arr[i, j] = 0
                    res += 1
                    gets += 2
                else:
                    tmp_lst.append(arr[i, j])
                    tmp_pos.append((i, j))
            else:
                continue
    
    if len(tmp_lst) == 9:
        if OUTPUT:
            print("\033[32m全家福！\033[0m")
        arr = init_arr()
        res += 5
        gets += 9
    
    return arr, res, gets


def final(arr: np.ndarray, gets: int) -> int:
    return gets + np.sum(arr != 0)


def start():
    res = 13
    gets = 0
    wish = np.random.randint(1, 10, dtype=np.int8)
    grid = init_arr()

    if OUTPUT:
        print(f"\033[32m[info]:许愿：{wish}\033[0m")

    while res > 0:
        grid, res = add_arr(grid, res, wish)
        if OUTPUT:
            print("矩阵:")
            print(grid)

        grid, res, gets = test(grid, res, gets)
        if OUTPUT:
            print("矩阵:")
            print(grid)
            print(f"res: {res}, gets: {gets}")
            print()
    
    gets = final(grid, gets)
    if OUTPUT:
        print(f"gets: {gets}")

    return gets


def count_integers():
    count_dict = {}
    for _ in trange(MAX_ITER, disable=OUTPUT):
        num = start()
        if num in count_dict:
            count_dict[num] += 1
        else:
            count_dict[num] = 1
    return count_dict


def plot_counts(count_dict):
    if OUTPUT or MAX_ITER < 10:
        return
    plt.figure(figsize=(10, 6))
    numbers = sorted(count_dict.keys())
    counts = [count_dict[num] for num in numbers]
    plt.bar(numbers, counts, color='skyblue')
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Frequency of Random Values')
    plt.xticks(rotation=45)
    plt.tight_layout()
    if SAVE:
        plt.savefig("./fig1.png")
    plt.show()

if __name__ == "__main__":
    count_result = count_integers()
    plot_counts(count_result)
