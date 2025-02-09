
# The Python Standard Library.
from typing import Union
import datetime
from dateutil import relativedelta

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

def birthdayFormatted(birthday: datetime.datetime) -> str:
    """
    Returns a formatted string representing the time since the given birthday.

    This function calculates the time elapsed since the provided birthday and returns
    a human-readable string in the format 'XX years, XX months, XX days'. If the current
    date matches the birthday (same day and month), a birthday emoji 🎂 is appended to
    the string.

    Parameters
    ----------
    birthday : datetime.datetime
        The date of birth to calculate the time elapsed from.

    Returns
    -------
    str
        A formatted string representing the time elapsed since the birthday.

    Examples
    --------
    >>> from datetime import datetime
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
