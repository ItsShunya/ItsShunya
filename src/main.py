# The Python Standard Library.
from datetime import datetime
from pathlib import Path

# Local project imports.
from config.config import ConfigParser
from svg.svg_generator import SvgGenerator


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def human_uptime(birthday: datetime) -> str:
    """
    Convert a birthday into a human-readable uptime string.

    Args:
        birthday (datetime): Date of birth.

    Returns:
        str: Uptime string in years / months / days.
    """
    now = datetime.now()
    delta = now - birthday

    years = delta.days // 365
    months = (delta.days % 365) // 30
    days = (delta.days % 365) % 30

    return f"{years}y {months}m {days}d"


def dot_line(key: str, value: str, width: int = 40) -> str:
    """
    Create a dot-filled key/value line.

    Args:
        key (str): Left-hand label.
        value (str): Right-hand value.
        width (int): Total width before value.

    Returns:
        str: Formatted line.
    """
    dots = "." * max(1, width - len(key))
    return f"{key} {dots} {value}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Generate the riced shell SVG profile.
    """
    # Load configuration
    config_path = Path("config/ItsShunya.yaml")
    cfg = ConfigParser.from_yaml_file(config_path)

    # Initialize SVG
    svg = SvgGenerator(width=1000, height=650)

    y = 40
    line_height = 18
    x = 40

    # Header prompt
    svg.create_text_element(
        x, y,
        "┌─[ victor@luque ]─[ ~/dev ]"
    )
    y += line_height
    svg.create_text_element(
        x, y,
        "└─❯ ./profile.sh"
    )
    y += line_height
    svg.create_text_element(
        x, y,
        "────────────────────────────────────────────"
    )

    # Banner
    y += line_height * 2
    banner = [
        "███████╗██╗  ██╗██╗   ██╗███╗   ██╗██╗   ██╗ █████╗ ",
        "██╔════╝██║  ██║██║   ██║████╗  ██║╚██╗ ██╔╝██╔══██╗",
        "███████╗███████║██║   ██║██╔██╗ ██║ ╚████╔╝ ███████║",
        "╚════██║██╔══██║██║   ██║██║╚██╗██║  ╚██╔╝  ██╔══██║",
        "███████║██║  ██║╚██████╔╝██║ ╚████║   ██║   ██║  ██║",
        "╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝",
    ]
    svg.create_multiple_tspan(x, y, banner)
    y += line_height * (len(banner) + 1)

    # [ system ]
    svg.create_text_element(x, y, "[ system ]")
    y += line_height
    svg.create_text_element(
        x, y,
        dot_line("os", cfg.user.operative_system or "unknown")
    )
    y += line_height
    svg.create_text_element(
        x, y,
        dot_line("uptime", human_uptime(cfg.user.birthday))
    )
    y += line_height
    svg.create_text_element(
        x, y,
        dot_line("host", cfg.user.position or "unknown")
    )

    # [ dev ]
    y += line_height * 2
    svg.create_text_element(x, y, "[ dev ]")
    y += line_height
    svg.create_text_element(
        x, y,
        dot_line("langs", " · ".join(cfg.languages.programming))
    )
    y += line_height
    svg.create_text_element(
        x, y,
        dot_line("tooling", " · ".join(cfg.activities.software))
    )
    y += line_height
    svg.create_text_element(
        x, y,
        dot_line("editor", cfg.user.ide or "unknown")
    )

    # [ github ] (static placeholders — inject stats later)
    y += line_height * 2
    svg.create_text_element(x, y, "[ github ]")
    y += line_height
    svg.create_text_element(x, y, dot_line("repos", "15 (+25)"))
    y += line_height
    svg.create_text_element(x, y, dot_line("commits", "2,527"))
    y += line_height
    svg.create_text_element(x, y, dot_line("stars", "12"))

    # [ contact ]
    y += line_height * 2
    svg.create_text_element(x, y, "[ contact ]")
    y += line_height
    svg.create_text_element(
        x, y,
        dot_line("mail", cfg.contact.personal_mail or "-")
    )
    y += line_height
    svg.create_text_element(
        x, y,
        dot_line("work", cfg.contact.work_mail or "-")
    )
    y += line_height
    svg.create_text_element(
        x, y,
        dot_line("linkedin", cfg.contact.linkedin or "-")
    )
    y += line_height
    svg.create_text_element(
        x, y,
        dot_line("discord", cfg.contact.discord or "-")
    )

    # Save SVG
    svg.save("profile.svg")


if __name__ == "__main__":
    main()
