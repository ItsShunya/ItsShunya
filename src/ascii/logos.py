"""ASCII logo definitions for profile generation.

This module contains various ASCII art logos representing different designs.

How to Create ASCII Logos
==========================

Manual Creation:
1. Use box-drawing characters (╭╮╰╯─│├┤┬┴┼)
2. Use block characters (█▀▄▌▐░▒▓)
3. Use geometric shapes (○●◆◇□■△▲)
4. Plan your design on graph paper first
5. Test in monospace font

Tools:
1. ASCII Art Paint (https://ascii-art-generator.org/)
2. Text Editor with good box-drawing support
3. Monodraw (macOS) - Professional ASCII art tool

Box-Drawing Characters Reference:
╭ ╮ ╰ ╯   Rounded corners
┌ ┐ └ ┘   Square corners
─ │       Lines
├ ┤ ┬ ┴   T-junctions
┼         Cross
╱ ╲       Diagonals

Block Characters:
█ Full block
▀ Upper half
▄ Lower half
▌ Left half
▐ Right half
░ Light shade
▒ Medium shade
▓ Dark shade

Tips:
- Keep logos under 30 lines tall
- Use consistent spacing
- Test rendering in target SVG/terminal
- Each logo line should be a tuple: (line_content, color_class)
"""

# Concentric circles logo - represents orbits/layers/system architecture
LOGO_CONCENTRIC_CIRCLES = [
    ("      ╭─────╮              ", "accent2"),
    ("    ╭─┤  │  ├─╮      ○    ", "accent2"),
    ("   ╭┤ │  │  │ ├╮          ", "accent3"),
    ("  ╭┤  ╰──●──╯  ├╮         ", "accent1"),
    ("   ╰┤ │  │  │ ├╯          ", "accent3"),
    ("    ╰─┤  │  ├─╯           ", "accent2"),
    (" ○    ╰─────╯             ", "accent2"),
]

# Collection of all logos
LOGOS = {
    "concentric_circles": LOGO_CONCENTRIC_CIRCLES,
}

# Default logo
DEFAULT_LOGO = "concentric_circles"
