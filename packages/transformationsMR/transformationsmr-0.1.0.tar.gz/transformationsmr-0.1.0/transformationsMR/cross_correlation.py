import numpy


def convolution2d(input_matrix, kernel, stride=1):
    """
    Performs a 2D convolution using a given kernel on a matrix.

    Parameters:
        input_matrix (numpy.ndarray): 2D input matrix
        kernel (numpy.ndarray): 2D convolution kernel
        stride (int, default=1): stride for moving the kernel

    Returns:
        output (numpy.ndarray): result of 2D convolution

    Raises:
        ValueError: in case incorrect type of matrix is provided
                    or stride value is not positive
    """
    if not isinstance(input_matrix, numpy.ndarray) or not isinstance(
        kernel, numpy.ndarray
    ):
        raise ValueError("input_matrix and kernel must be Numpy arrays")

    if input_matrix.ndim != 2 or kernel.ndim != 2:
        raise ValueError("input_matrix and kernel must be 2D arrays")

    if stride <= 0:
        raise ValueError("Stride must be a positive number")

    input_height, input_width = input_matrix.shape
    kernel_height, kernel_width = kernel.shape
    output_height = (input_height - kernel_height) // stride + 1
    output_width = (input_width - kernel_width) // stride + 1
    output = numpy.zeros((output_height, output_width))

    for i in range(0, input_height - kernel_height + 1, stride):
        for j in range(0, input_width - kernel_width + 1, stride):
            output[i // stride, j // stride] = numpy.sum(
                input_matrix[i : i + kernel_height, j : j + kernel_width]
                * kernel
            )

    return output
