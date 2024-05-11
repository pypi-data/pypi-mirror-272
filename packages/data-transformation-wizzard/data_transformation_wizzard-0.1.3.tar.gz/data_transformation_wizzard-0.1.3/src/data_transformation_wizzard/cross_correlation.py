import numpy as np


def convolution2d(
    input_matrix: list | np.ndarray, kernel: list | np.ndarray, stride: int = 1
) -> np.ndarray:
    """
    Apply 2D convolution to an input matrix with a given kernel and stride.

    Parameters:
    input_matrix (Union[List[float], np.ndarray]): The 2D input matrix consisting of numbers.
    kernel (Union[List[float], np.ndarray]): The kernel, a 2D array of real numbers.
    stride (int, optional): The stride, an integer that is greater than 0. Default is 1.

    Returns:
    Union[np.ndarray, List[List[float]]]: The output matrix, either a 2D Numpy array or a list of lists, matching the input type.

    Raises:
    TypeError: If input_matrix or kernel is not a list or numpy array.
    ValueError: If input_matrix or kernel does not contain only integers or floats, or if stride is not a positive int.
    """
    if not isinstance(input_matrix, (list, np.ndarray)):
        raise TypeError("input_matrix must be a list or numpy array")
    if not all(
        isinstance(i, (int, float, np.number))
        for sublist in input_matrix
        for i in sublist
    ):
        raise ValueError("input_matrix must contain only numbers")
    if not isinstance(kernel, (list, np.ndarray)):
        raise TypeError("kernel must be a list or numpy array")
    if not all(
        isinstance(i, (int, float, np.number))
        for sublist in kernel
        for i in sublist
    ):
        raise ValueError("kernel must contain only numbers")
    if not isinstance(stride, int) or stride < 1:
        raise ValueError("stride must be a positive integer")

    # Determine the output type based on the input type
    output_type = np.ndarray if isinstance(input_matrix, np.ndarray) else list

    # Convert input_matrix and kernel to numpy arrays
    input_matrix = (
        np.array(input_matrix, dtype=float)
        if not isinstance(input_matrix, np.ndarray)
        else input_matrix
    )
    kernel = (
        np.array(kernel, dtype=float)
        if not isinstance(kernel, np.ndarray)
        else kernel
    )

    # Dimensions of input matrix and kernel
    x_kern, y_kern = kernel.shape
    x_in, y_in = input_matrix.shape

    # Dimensions of output matrix
    x_out = (x_in - x_kern) // stride + 1
    y_out = (y_in - y_kern) // stride + 1

    # Starting point
    output_matrix = np.zeros((x_out, y_out))

    # Apply convolution
    for i in range(x_out):
        for j in range(y_out):
            output_matrix[i, j] = np.sum(
                input_matrix[
                    i * stride : i * stride + x_kern,
                    j * stride : j * stride + y_kern,
                ]
                * kernel
            )

    # Convert output to the same type as input
    return (
        output_matrix if output_type is np.ndarray else output_matrix.tolist()
    )
