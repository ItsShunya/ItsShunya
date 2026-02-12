"""Main entry point for generating the riced shell SVG profile."""

from pathlib import Path

#from ascii.logos import LOGOS, DEFAULT_LOGO
from ascii.banner import BANNERS, DEFAULT_BANNER
from config.config import ConfigParser
from svg.svg_generator import SvgGenerator
from graphql.github import *
from utils import format, time, timer

# Constants
LINE_HEIGHT = 18
SECTION_SPACING = LINE_HEIGHT * 2
START_X = 40
START_Y = 40

def fetch_github_stats(
    cfg: ConfigParser
) -> dict:
    """Fetch all GitHub statistics and return as a dictionary."""
    github_queries = {
        'commits':      (commit_counter, 7),
        'stars':        (graph_repos_stars, 'stars', ['OWNER']),
        'repos':        (graph_repos_stars, 'repos', ['OWNER']),
        'contrib':      (graph_repos_stars, 'repos', ['OWNER', 'COLLABORATOR', 'ORGANIZATION_MEMBER']),
        'followers':    (follower_getter, cfg.user.username),
    }

    github_data = {}
    total_time = 0

    for key, args in github_queries.items():
        func, *params = args
        github_data[key], query_time = timer.perf_counter(func, *params)
        total_time += query_time

    print(f"Total Github GraphQL query time: {total_time:.4f} s")
    return github_data


def add_info_line(
    svg: SvgGenerator,
    x: int,
    y: int,
    label: str,
    value: str
) -> int:
    """Add a single info line and return new y position."""
    svg.create_colored_text(x, y, format.toDotLine(label, value))
    return y + LINE_HEIGHT


def add_section_header(
    svg: SvgGenerator,
    x: int,
    y: int,
    title: str
) -> int:
    """Add a section header and return new y position."""
    svg.create_colored_text(x, y, [
        ("[", "accent1"),
        (f" {title} ", "string"),
        ("]", "accent1")
    ])
    return y + LINE_HEIGHT


def create_profile_header(
    svg: SvgGenerator,
    x: int,
    y: int,
    cfg: ConfigParser
) -> int:
    """Create the shell prompt header."""
    svg.create_colored_text(x, y, [
        ("┌─[", "accent1"),
        (f" {cfg.user.name.lower()}", "prompt"),
        ("@", "accent2"),
        (f"{cfg.user.surname.lower()}", "accent3"),
        (" ]─[", "accent1"),
        (" ~/dev", "string"),
        (" ]", "accent1"),
    ])
    y += LINE_HEIGHT

    svg.create_colored_text(x, y, [
        ("└─", "accent1"),
        ("❯", "warning"),
        (" ./profile.sh", "command"),
    ])
    y += LINE_HEIGHT

    svg.create_text_element(
        x, y,
        "─────────────────────────────────────────────────────────────────",
        "separator", None
    )
    return y + LINE_HEIGHT


def create_banner(
    svg: SvgGenerator,
    x: int,
    y: int
) -> int:
    """Create the ASCII banner and return new y position."""
    y += LINE_HEIGHT

    # Uncomment to add ASCII logo on the left:
    # logo = LOGOS[DEFAULT_LOGO]  # or use a specific logo like LOGOS["terminal"]
    # svg.create_ascii_logo(x, y, logo, LINE_HEIGHT)
    # banner_x = 200  # Shift banner to the right to make room for logo
    # banner = BANNERS[DEFAULT_BANNER]
    # svg.create_multiple_tspan(banner_x, y, banner, "highlight")

    # Standard banner without logo:
    banner = BANNERS[DEFAULT_BANNER]
    banner = ["  " + line for line in banner]  # Add indentation to banner
    svg.create_multiple_tspan(x, y, banner, "highlight")

    return y + LINE_HEIGHT * (len(banner) + 1)


def build_sections_data(
    cfg: ConfigParser,
    github_data: dict
) -> dict:
    """Build the data structure for all profile sections."""
    return {
        "system": [
            ("os", cfg.user.operative_system or "unknown"),
            ("uptime", time.human_uptime(cfg.user.birthday)),
            ("kernel", cfg.user.position or "unknown"),
            ("host", cfg.user.company or "unknown"),
        ],
        "dev": [
            ("langs", " · ".join(cfg.languages.programming)),
            ("tooling", " · ".join(cfg.activities.software)),
            ("editor", cfg.user.ide or "unknown"),
        ],
        "github": [
            ("repos", f"{github_data['repos']} (+{github_data['contrib']})"),
            ("commits", f"{github_data['commits']}"),
            ("stars", f"{github_data['stars']}"),
            ("followers", f"{github_data['followers']}"),
        ],
        "contact": [
            ("mail", cfg.contact.personal_mail or "-"),
            ("web", cfg.contact.web or "-"),
            ("work", cfg.contact.work_mail or "-"),
            ("linkedin", cfg.contact.linkedin or "-"),
        ],
    }


def render_sections(
    svg: SvgGenerator,
    x: int,
    y: int,
    sections: tuple
) -> int:
    """Render all profile sections and return final y position."""
    for section_name, items in sections.items():
        y += LINE_HEIGHT  # spacing between sections
        y = add_section_header(svg, x, y, section_name)
        for label, value in items:
            y = add_info_line(svg, x, y, label, value)

    return y


def main() -> None:
    """
    Generate the riced shell SVG profile.
    """
    # Load configuration
    cfg = ConfigParser.from_yaml_file(Path("config/ItsShunya.yaml"))

    # Fetch GitHub stats
    github_data = fetch_github_stats(cfg)

    # Initialize SVG
    svg = SvgGenerator(width=560, height=700)

    # Build the profile
    y = START_Y
    y = create_profile_header(svg, START_X, y, cfg)
    y = create_banner(svg, START_X, y)

    sections = build_sections_data(cfg, github_data)
    y = render_sections(svg, START_X, y, sections)

    # Save SVG
    svg.save("output/profile.svg")


if __name__ == "__main__":
    main()
