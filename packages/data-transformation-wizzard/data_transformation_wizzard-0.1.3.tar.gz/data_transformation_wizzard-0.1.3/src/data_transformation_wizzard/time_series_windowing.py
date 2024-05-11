import numpy as np


def window1d(
    input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1
) -> list[list | np.ndarray]:
    """
    This function performs a windowing operation on a 1-dimensional input array.
    Parameters:
    input_array (Union[List[float], np.ndarray]): The 1-dimensional input array consisting of numbers.
    size (int): The size of each window. This must be a positive integer.
    shift (int, optional): The number of positions to shift the window at each step. This must be a positive integer. Defaults to 1.
    stride (int, optional): The number of positions to step within each window. This must be a positive integer. Defaults to 1.
    Returns:
    Union[List[Union[List[float], np.ndarray]], np.ndarray]: A list or numpy array of windows, matching the input format.
    Raises:
    TypeError: If input_array is not a list or numpy array.
    ValueError: If input_array does not contain only integers or floats, or if size, shift, or stride are not positive integers.
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

    # Determine the output type based on the input type
    output_type = np.ndarray if isinstance(input_array, np.ndarray) else list

    # Convert input_array to numpy array
    input_array = np.array(input_array)

    # Iterate over the input_array with a step size of shift
    output = []
    i = 0
    while i + (size - 1) * stride < len(input_array):
        window = input_array[i : i + (size - 1) * stride + 1 : stride]
        if len(window) == size:
            output.append(window)
        i += shift

    # Convert output to the same type as input
    return output_type(output)
