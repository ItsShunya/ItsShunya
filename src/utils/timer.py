# The Python Standard Library.
import time

def perf_counter(funct, *args):
    """
    Calculates the execution time of a function and returns both the result and the time taken.

    This function measures the time taken for a given function to execute with specified arguments.
    It returns a tuple containing the function's result and the time differential in seconds.

    Parameters
    ----------
    funct : callable
        The function to be timed.
    *args : tuple, optional
        Variable-length arguments to be passed to `funct`.

    Returns
    -------
    tuple
        A tuple containing:
        - funct_return : any
            The result of the executed function.
        - time_diff : float
            The time taken for the function to execute, in seconds.

    Examples
    --------
    >>> def add(a, b):
    ...     return a + b
    >>> result, time_taken = perf_counter(add, 1, 2)
    >>> print(f"Result: {result}, Time: {time_taken:.6f} seconds")
    Result: 3, Time: 0.000001 seconds
    """
    start = time.perf_counter()
    funct_return = funct(*args)
    return funct_return, time.perf_counter() - start
