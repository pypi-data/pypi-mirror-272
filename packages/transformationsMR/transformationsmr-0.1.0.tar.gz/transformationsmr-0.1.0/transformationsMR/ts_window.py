import numpy


def window1d(input_array, size, shift=1, stride=1):
    """
    Slices an array of numbers into sizable pieces,
    providing shift between each couple of slices and
    step size inside them.

    Parameters:
        input_array (list[float]): list of real numbers
        size (int): maximum size of each window
        shift (int, default=1): difference between two windows' first numbers
        stride (int, default=1): step between input elements within a window

    Returns:
        windows (list[list[float]]): list of windows

    Raises:
        ValueError: in case incorrect input type or negative numbers provided
    """
    if not isinstance(input_array, (list, numpy.ndarray)):
        raise ValueError("Input must be a list or a 1D Numpy array")

    if size <= 0:
        raise ValueError("Window size must be a positive number")

    if shift <= 0:
        raise ValueError("Shift must be a positive number")

    if stride <= 0:
        raise ValueError("Stride must be a positive number")

    num_windows = (len(input_array) + shift) // shift + 1
    windows = []

    for i in range(num_windows):
        start = i * shift
        end = start + size * stride
        window = input_array[start:end:stride]
        windows.append(window)

    windows = [x for x in windows if x != []]
    return windows
