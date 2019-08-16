import concurrent.futures

counter = 0


def increment_counter():
    global counter
    counter += 1


if __name__ == '__main__':
    test_data = [x for x in range(5000)]
    # global counter
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        pool.map(increment_counter, test_data)
    print(f'Counter is: {counter}')

