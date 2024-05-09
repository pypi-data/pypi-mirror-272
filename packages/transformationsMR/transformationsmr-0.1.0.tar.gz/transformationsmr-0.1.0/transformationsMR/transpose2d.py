def transpose2d(input_matrix):
    """
    Switches axis of a 2-dimensional tensors.

    Parameters:
        input_matrix (list[list[float]]): list of lists of real numbers

    Returns:
        transposed_matrix (list[list[float]]): transposed tensor

    Raises:
        ValueError: in case the tensor is of incorrect type
    """
    if not all(isinstance(row, list) for row in input_matrix):
        raise ValueError("Input matrix must be a tensor of real numbers")

    num_rows = len(input_matrix)
    num_cols = len(input_matrix[0])
    transposed_matrix = [[0 for _ in range(num_rows)] for _ in range(num_cols)]

    for i in range(num_rows):
        for j in range(num_cols):
            transposed_matrix[j][i] = input_matrix[i][j]

    return transposed_matrix
