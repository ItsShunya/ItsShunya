"""Time-related utilities, such as time conversions."""

from datetime import datetime

def human_uptime(
    birthday: datetime
) -> str:
    """
    Convert a birthday into a human-readable uptime string.

    Parameters
    ----------
    birthday : datetime:
        Date of birth.

    Returns
    -------
    str
        Uptime string in years / months / days.
    """
    now = datetime.now()
    delta = now - birthday

    years = delta.days // 365
    months = (delta.days % 365) // 30
    days = (delta.days % 365) % 30

    return f"{years}y {months}m {days}d"
