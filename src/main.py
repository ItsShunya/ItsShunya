"""Main entry point for generating the riced shell SVG profile."""

from pathlib import Path

from ascii.banner import BANNERS, DEFAULT_BANNER
from ascii.logos import LOGOS, DEFAULT_LOGO

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

    # Header prompt with multi-colored elements
    svg.create_colored_text(
        x, y,
        [
            ("┌─[", "accent1"),
            (" victor", "prompt"),
            ("@", "accent2"),
            ("luque", "accent3"),
            (" ]─[", "accent1"),
            (" ~/dev", "string"),
            (" ]", "accent1"),
        ]
    )
    y += line_height

    svg.create_colored_text(
        x, y,
        [
            ("└─", "accent1"),
            ("❯", "warning"),
            (" ./profile.sh", "command"),
        ]
    )
    y += line_height

    svg.create_text_element(
        x, y,
        "────────────────────────────────────────────",
        "separator"
    )

    # Banner (and optional logo)
    y += line_height * 2

    # Uncomment to add ASCII logo on the left:
    # logo = LOGOS[DEFAULT_LOGO]  # or use a specific logo like LOGOS["terminal"]
    # svg.create_ascii_logo(x, y, logo, line_height)
    # banner_x = 200  # Shift banner to the right to make room for logo
    # banner = BANNERS[DEFAULT_BANNER]
    # svg.create_multiple_tspan(banner_x, y, banner, "highlight")

    # Standard banner without logo:
    banner = BANNERS[DEFAULT_BANNER]
    # Add indentation to banner
    banner = ["  " + line for line in banner]
    svg.create_multiple_tspan(x, y, banner, "highlight")
    y += line_height * (len(banner) + 1)

    # [ system ]
    svg.create_colored_text(x, y, [("[", "accent1"), (" system ", "string"), ("]", "accent1")])
    y += line_height
    svg.create_colored_text(
        x, y,
        format.toDotLine("os", cfg.user.operative_system or "unknown")
    )
    y += line_height
    svg.create_colored_text(
        x, y,
        format.toDotLine("uptime", time.human_uptime(cfg.user.birthday))
    )
    y += line_height
    svg.create_colored_text(
        x, y,
        format.toDotLine("host", cfg.user.position or "unknown")
    )

    # [ dev ]
    y += line_height * 2
    svg.create_colored_text(x, y, [("[", "accent1"), (" dev ", "string"), ("]", "accent1")])
    y += line_height
    svg.create_colored_text(
        x, y,
        format.toDotLine("langs", " · ".join(cfg.languages.programming))
    )
    y += line_height
    svg.create_colored_text(
        x, y,
        format.toDotLine("tooling", " · ".join(cfg.activities.software))
    )
    y += line_height
    svg.create_colored_text(
        x, y,
        format.toDotLine("editor", cfg.user.ide or "unknown")
    )

    # [ github ]
    y += line_height * 2
    svg.create_colored_text(x, y, [("[", "accent1"), (" github ", "string"), ("]", "accent1")])
    y += line_height
    svg.create_colored_text(x, y, format.toDotLine("repos", "15 (+25)"))
    y += line_height
    svg.create_colored_text(x, y, format.toDotLine("commits", "2,527"))
    y += line_height
    svg.create_colored_text(x, y, format.toDotLine("stars", "12"))

    # [ contact ]
    y += line_height * 2
    svg.create_colored_text(x, y, [("[", "accent1"), (" contact ", "string"), ("]", "accent1")])
    y += line_height
    svg.create_colored_text(
        x, y,
        format.toDotLine("mail", cfg.contact.personal_mail or "-")
    )
    y += line_height
    svg.create_colored_text(
        x, y,
        format.toDotLine("work", cfg.contact.work_mail or "-")
    )
    y += line_height
    svg.create_colored_text(
        x, y,
        format.toDotLine("linkedin", cfg.contact.linkedin or "-")
    )
    y += line_height
    svg.create_colored_text(
        x, y,
        format.toDotLine("discord", cfg.contact.discord or "-")
    )

    # Save SVG
    svg.save("profile.svg")


if __name__ == "__main__":
    main()
