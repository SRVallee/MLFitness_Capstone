import numpy as np

def update_average_with_one_value(average, size, value):
    return (size * average + value) / (size + 1)


def update_average_with_average(average_one, size_one, average_two, size_two):
    return (size_one * average_one + size_two * average_two) / (size_one + size_two)


def update_stdev(old_average, old_stdev, old_size, new_value):
    old_size += 1
    var = old_stdev ** 2
    temp = ((old_size - 2) * var + (new_value - update_average_with_one_value(old_average, old_size, new_value)) * (new_value - old_average)) / (old_size - 1)
    return np.sqrt(temp)