import numpy as np


def window1d(
    input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1
) -> list[list | np.ndarray]:
    """
    Perform a windowing operation on a 1-dimensional input array.

    Args:
    input_array (list | np.ndarray): The 1-dimensional input array.
    size (int): The size of each window.
    shift (int, optional): The number of positions to shift the window at each step.
    stride (int, optional): The number of positions to step within each window.

    Returns:
    list[list | np.ndarray]: A list of windows, where each window is either a list or a numpy array.

    Raises:
    TypeError: If input_array is not a list or numpy array.
    ValueError: If input_array does not contain only integers or floats.
    """
    if not isinstance(input_array, (list, np.ndarray)):
        raise TypeError("input_array must be a list or numpy array")
    if not all(isinstance(i, (int, float, np.number)) for i in input_array):
        raise ValueError("input_array must contain only numbers")
    if not isinstance(size, int) or size < 1:
        raise ValueError("size must be an integer greater than 0")
    if not isinstance(shift, int) or shift < 1:
        raise ValueError("shift must be an integer greater than 0")
    if not isinstance(stride, int) or stride < 1:
        raise ValueError("stride must be an integer greater than 0")

    input_was_ndarray = isinstance(input_array, np.ndarray)
    input_array = np.array(input_array)

    output = []
    i = 0
    while i + (size - 1) * stride < len(input_array):
        window = input_array[i : i + (size - 1) * stride + 1 : stride]
        if len(window) == size:
            if input_was_ndarray:
                output.append(window)
            else:
                output.append(window.tolist())
        i += shift

    return output
