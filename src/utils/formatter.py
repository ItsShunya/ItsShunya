from typing import Union

def toPlural(unit: int) -> str:
    """
    Returns a properly formatted plural suffix based on the input unit.

    Parameters
    ----------
    unit : int
        The number to determine the plural form for.

    Returns
    -------
    str
        The plural suffix ('s' if unit is not 1, otherwise an empty string).

    Examples
    --------
    >>> stringtoPlural(5)
    's'
    >>> stringtoPlural(1)
    ''
    """
    return 's' if unit != 1 else ''

def timeDiffFormatted(query_type: str, difference: float, funct_return: bool = False, whitespace: int = 0) -> Union[str, bool]:
    """
    Prints a formatted time difference and optionally returns a formatted result.

    Parameters
    ----------
    query_type : str
        The type of query for which the time difference is displayed.
    difference : float
        The computed time difference to be formatted and displayed.
    funct_return : bool, optional
        Determines whether to return a formatted string. Default is False.
    whitespace : int, optional
        The width for left-aligned formatting of the returned string. Default is 0.

    Returns
    -------
    Union[str, bool]
        Returns the formatted time difference string if ``whitespace`` is nonzero, 
        otherwise returns ``funct_return`` unmodified.
    """
    print('{:<23}'.format('   ' + query_type + ':'), sep='', end='')
    print('{:>12}'.format('%.4f' % difference + ' s ')) if difference > 1 else print('{:>12}'.format('%.4f' % (difference * 1000) + ' ms'))
    if whitespace:
        return f"{'{:,}'.format(funct_return): <{whitespace}}"
    return funct_return