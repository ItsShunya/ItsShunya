"""Formatting utils, mainly for beautifying strings."""

import datetime
from dateutil import relativedelta

def toPlural(
    unit: int
) -> str:
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

def timeDiffFormatted(
    query_type: str,
    difference: float,
    funct_return: bool = False,
    whitespace: int = 0,
) -> str | bool:
    """
    Print a formatted time difference and optionally return a formatted value.

    This function prints a human-readable representation of a time difference,
    choosing seconds or milliseconds depending on magnitude. Optionally, it
    returns either a left-aligned formatted string or the value of
    ``funct_return`` unchanged.

    Parameters
    ----------
    query_type : str
        Label associated with the measured operation, printed as a prefix.
    difference : float
        Time difference in seconds.
    funct_return : bool, optional
        Value to return when ``whitespace`` is zero. Defaults to ``False``.
    whitespace : int, optional
        If non-zero, the return value is a left-aligned string representation
        of ``funct_return`` padded to this width. Defaults to ``0``.

    Returns
    -------
    str | bool
        If ``whitespace`` is non-zero, returns a formatted string representation
        of ``funct_return`` padded to ``whitespace`` characters. Otherwise,
        returns ``funct_return`` unchanged.

    Notes
    -----
    - This function always produces console output as a side effect.
    - Time values greater than 1 second are displayed in seconds; smaller values
      are displayed in milliseconds.
    """
    print('{:<23}'.format('   ' + query_type + ':'), sep='', end='')
    print('{:>12}'.format('%.4f' % difference + ' s ')) if difference > 1 else print('{:>12}'.format('%.4f' % (difference * 1000) + ' ms'))
    if whitespace:
        return f"{'{:,}'.format(funct_return): <{whitespace}}"
    return funct_return

def birthdayFormatted(
    birthday: datetime.datetime
) -> str:
    """
    Return a formatted string representing the time since the given birthday.

    Calculates the time elapsed since the provided birthday and returns a
    human-readable string in the format ``'XX years, XX months, XX days'``.
    If today is the birthday (same day and month), a birthday emoji 🎂 is appended.

    Parameters
    ----------
    birthday : datetime.datetime
        The date of birth to calculate the time elapsed from.

    Returns
    -------
    str
        Formatted string representing the time elapsed since the birthday.

    Examples
    --------
    >>> from datetime import datetime
    >>> from dateutil import relativedelta
    >>> birthday = datetime(1990, 5, 15)
    >>> birthdayFormatted(birthday)
    '33 years, 0 months, 0 days 🎂'
    >>> current_date = datetime.today()
    >>> birthday = current_date - relativedelta.relativedelta(days=5)
    >>> birthdayFormatted(birthday)
    '0 years, 0 months, 5 days'
    """
    diff: relativedelta.relativedelta = relativedelta.relativedelta(datetime.datetime.today(), birthday)
    return '{} {}, {} {}, {} {}{}'.format(
        diff.years, 'year' + toPlural(diff.years),
        diff.months, 'month' + toPlural(diff.months),
        diff.days, 'day' + toPlural(diff.days),
        ' 🎂' if (diff.months == 0 and diff.days == 0) else ''
    )

def toDotLine(
    key: str,
    value: str,
    width: int = 40
) -> str:
    """
    Create a dot-filled key/value line.

    Parameters
    ----------
    key : str
        Left-hand label.
    value : str
        Right-hand value.
    width : int
        Total width before value.

    Returns
    -------
    str
        Formatted line.
    """
    dots = "." * max(1, width - len(key))
    return f"{key} {dots} {value}"
