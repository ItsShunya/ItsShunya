# The Python Standard Library.
from pathlib import Path

# Local project imports.
from config.config import ConfigParser
from svg.svg_generator import SvgGenerator
from utils import format, time

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
        format.toDotLine("os", cfg.user.operative_system or "unknown")
    )
    y += line_height
    svg.create_text_element(
        x, y,
        format.toDotLine("uptime", time.human_uptime(cfg.user.birthday))
    )
    y += line_height
    svg.create_text_element(
        x, y,
        format.toDotLine("host", cfg.user.position or "unknown")
    )

    # [ dev ]
    y += line_height * 2
    svg.create_text_element(x, y, "[ dev ]")
    y += line_height
    svg.create_text_element(
        x, y,
        format.toDotLine("langs", " · ".join(cfg.languages.programming))
    )
    y += line_height
    svg.create_text_element(
        x, y,
        format.toDotLine("tooling", " · ".join(cfg.activities.software))
    )
    y += line_height
    svg.create_text_element(
        x, y,
        format.toDotLine("editor", cfg.user.ide or "unknown")
    )

    # [ github ] (static placeholders — inject stats later)
    y += line_height * 2
    svg.create_text_element(x, y, "[ github ]")
    y += line_height
    svg.create_text_element(x, y, format.toDotLine("repos", "15 (+25)"))
    y += line_height
    svg.create_text_element(x, y, format.toDotLine("commits", "2,527"))
    y += line_height
    svg.create_text_element(x, y, format.toDotLine("stars", "12"))

    # [ contact ]
    y += line_height * 2
    svg.create_text_element(x, y, "[ contact ]")
    y += line_height
    svg.create_text_element(
        x, y,
        format.toDotLine("mail", cfg.contact.personal_mail or "-")
    )
    y += line_height
    svg.create_text_element(
        x, y,
        format.toDotLine("work", cfg.contact.work_mail or "-")
    )
    y += line_height
    svg.create_text_element(
        x, y,
        format.toDotLine("linkedin", cfg.contact.linkedin or "-")
    )
    y += line_height
    svg.create_text_element(
        x, y,
        format.toDotLine("discord", cfg.contact.discord or "-")
    )

    # Save SVG
    svg.save("profile.svg")


if __name__ == "__main__":
    main()
