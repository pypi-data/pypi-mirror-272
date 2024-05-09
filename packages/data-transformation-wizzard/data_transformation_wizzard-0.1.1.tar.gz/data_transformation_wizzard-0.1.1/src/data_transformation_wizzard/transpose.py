def transpose2d(input_matrix: list[list[float]]) -> list[list[float]]:
    """
    Transpose a 2D matrix.

    Args:
    input_matrix (List[List[float]]): The input 2D matrix.

    Returns:
    List[List[float]]: The transposed 2D matrix.

    Raises:
    TypeError: If input_array is not a list of lists of numbers.
    ValueError: If input_array does not contain only numbers or if all inner lists do not have the same length.

    Example:
    >>> input_matrix = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    >>> transpose2d(input_matrix)
    [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
    """

    # Check if input is a list of lists
    if not all(isinstance(row, list) for row in input_matrix):
        raise TypeError("Input must be a list of lists")
    # Check if all elements of the list are numbers
    if not all(
        all(isinstance(num, (int, float)) for num in row)
        for row in input_matrix
    ):
        raise ValueError("All elements of the input list must be numbers")
    # Check if all inner lists have the same length
    if not all(len(row) == len(input_matrix[0]) for row in input_matrix):
        raise ValueError("All inner lists must have the same length")
    # Transpose the 2D matrix
    return [list(row) for row in zip(*input_matrix)]
