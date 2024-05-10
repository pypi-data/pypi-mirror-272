import time
import sys

if sys.platform == "win32":
    timer = time.perf_counter
else:
    timer = time.time


def convert(data, mode="speed"):
    if mode == "speed":
        if data > 1000000:
            result = str(round(data / 1000000, 2)) + " M/S"
        elif data > 1000:
            result = str(round(data / 1000, 2)) + " K/S"
        else:
            result = str(int(data)) + "/s"
    elif mode == "elapsed":
        if data >= 1:
            result = str(round(data, 2)) + "s"
        if data >= 1e-3:
            result = str(round(data * 1e3, 1)) + "ms"
        elif data >= 1e-6:
            result = str(round(data * 1e6, 1)) + "us"
        else:
            result = str(round(data * 1e9, 1)) + "ns"
    return result


def vfunc(func, args=(), mode="speed"):

    if mode not in ["speed", "elapsed"]:
        print("'mode' parameter can only value as 'speed' or 'elapsed'.")
        return False

    try:
        start_time = timer()
        func(*args)
        run_time = timer() - start_time
    except:
        print("Errors found in the function under test.")
        return False

    try:
        count = int(1 / run_time) + 1
    except ZeroDivisionError:
        count = 1e9

    stat = []

    while True:
        start_time = timer()
        for i in range(count):
            func(*args)
        run_time = timer() - start_time

        if mode == "speed":
            stat.append(count / run_time)
        else:
            stat.append(run_time / count)

        result = convert(stat[-1], mode)
        avg = convert(sum(stat) / len(stat), mode)

        print(" " * 45, end="\r")
        print(result)
        print("repeat: {}  ".format(len(stat)), "average = {}".format(avg), end="\r")

