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
    cfg = ConfigParser.from_yaml_file(Path("config/ItsShunya.yaml"))

    # Initialize SVG
    svg = SvgGenerator(width=560, height=650)

    y = 40
    x = 40

    line_ht = 18

    # Header prompt with multi-colored elements
    svg.create_colored_text(
        x, y,
        [
            ("┌─[",                         "accent1"),
            (f" {cfg.user.name.lower()}",   "prompt"),
            ("@",                           "accent2"),
            (f"{cfg.user.surname.lower()}", "accent3"),
            (" ]─[",                        "accent1"),
            (" ~/dev",                      "string"),
            (" ]",                          "accent1"),
        ]
    )
    y += line_ht

    svg.create_colored_text(
        x, y,
        [
            ("└─",              "accent1"),
            ("❯",               "warning"),
            (" ./profile.sh",   "command"),
        ]
    )
    y += line_ht

    svg.create_text_element(
        x, y,
        "────────────────────────────────────────────",
        "separator", None
    )

    ##### Banner (and optional logo)
    y += line_ht * 2

    # Uncomment to add ASCII logo on the left:
    # logo = LOGOS[DEFAULT_LOGO]  # or use a specific logo like LOGOS["terminal"]
    # svg.create_ascii_logo(x, y, logo, line_ht)
    # banner_x = 200  # Shift banner to the right to make room for logo
    # banner = BANNERS[DEFAULT_BANNER]
    # svg.create_multiple_tspan(banner_x, y, banner, "highlight")

    # Standard banner without logo:
    banner = BANNERS[DEFAULT_BANNER]
    banner = ["  " + line for line in banner] # Add indentation to banner
    svg.create_multiple_tspan(
        x, y, banner, "highlight")
    y += line_ht * (len(banner) + 1)

    ##### [ system ]
    svg.create_colored_text(
        x, y,
        [
            ("[",           "accent1"),
            (" system ",    "string"),
            ("]",           "accent1")
        ]
    )
    y += line_ht
    svg.create_colored_text(
        x, y,
        format.toDotLine("os", cfg.user.operative_system or "unknown")
    )
    y += line_ht
    svg.create_colored_text(
        x, y,
        format.toDotLine("uptime", time.human_uptime(cfg.user.birthday))
    )
    y += line_ht
    svg.create_colored_text(
        x, y,
        format.toDotLine("kernel", cfg.user.position or "unknown")
    )
    y += line_ht
    svg.create_colored_text(
        x, y,
        format.toDotLine("host", cfg.user.company or "unknown")
    )

    ##### [ dev ]
    y += line_ht * 2
    svg.create_colored_text(
        x, y,
        [
            ("[",       "accent1"),
            (" dev ",   "string"),
            ("]",       "accent1")])
    y += line_ht
    svg.create_colored_text(
        x, y,
        format.toDotLine("langs", " · ".join(cfg.languages.programming))
    )
    y += line_ht
    svg.create_colored_text(
        x, y,
        format.toDotLine("tooling", " · ".join(cfg.activities.software))
    )
    y += line_ht
    svg.create_colored_text(
        x, y,
        format.toDotLine("editor", cfg.user.ide or "unknown")
    )

    ##### [ github ]
    y += line_ht * 2
    svg.create_colored_text(
        x, y,
        [
            ("[", "accent1"),
            (" github ", "string"),
            ("]", "accent1")
            ]
    )
    y += line_ht
    svg.create_colored_text(
        x, y,
        format.toDotLine("repos", "15 (+25)")
    )
    y += line_ht
    svg.create_colored_text(
        x, y,
        format.toDotLine("commits", "2,527")
    )
    y += line_ht
    svg.create_colored_text(
        x, y,
        format.toDotLine("stars", "12")
    )

    ##### [ contact ]
    y += line_ht * 2
    svg.create_colored_text(
        x, y,
        [
            ("[", "accent1"),
            (" contact ", "string"),
            ("]", "accent1")
            ]
    )
    y += line_ht
    svg.create_colored_text(
        x, y,
        format.toDotLine("mail", cfg.contact.personal_mail or "-")
    )
    y += line_ht
    svg.create_colored_text(
        x, y,
        format.toDotLine("work", cfg.contact.work_mail or "-")
    )
    y += line_ht
    svg.create_colored_text(
        x, y,
        format.toDotLine("linkedin", cfg.contact.linkedin or "-")
    )
    y += line_ht
    svg.create_colored_text(
        x, y,
        format.toDotLine("discord", cfg.contact.discord or "-")
    )

    # Save SVG
    svg.save("output/profile.svg")


if __name__ == "__main__":
    main()
