import time
import multiprocessing


def calculate(no):
    return sum(i * i for i in range(no))


def find_sum(number_list):
    with multiprocessing.Pool() as pool:
        pool.map(calculate, number_list)


if __name__ == "__main__":
    numbers = [5000000 + x for x in range(20)]
    start_time = time.time()
    find_sum(numbers)
    duration = time.time() - start_time
    print(f"Duration {duration} seconds")
