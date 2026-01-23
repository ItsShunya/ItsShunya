"""ASCII banner definitions for profile generation.

This module contains various ASCII art banners that can be used in the profile.

How to Generate ASCII Banners
==============================

Online Tools:
1. Patorjk's Text to ASCII Art Generator (RECOMMENDED)
   URL: https://patorjk.com/software/taag/
   - Select font (e.g., "ANSI Shadow", "Big", "Standard", "Slant")
   - Enter your text
   - Copy the generated ASCII art

2. FIGlet (Command Line Tool)
   Install: sudo apt-get install figlet
   Usage: figlet -f <font> "YourText"
   Example: figlet -f banner "SHUNYA"

3. ASCII Art Generator
   URL: https://www.ascii-art-generator.org/

Popular Fonts for Programming:
- ANSI Shadow (used below for SHUNYA)
- Slant
- Big
- Standard
- Graffiti
- Doom
- Banner3
- Block

Tips:
- Use monospace-friendly fonts
- Test in terminal with monospace font before adding
- Keep banners under 80 characters wide for better compatibility
- Use box-drawing characters for borders and logos
"""

# ANSI Shadow font - used in the profile
SHUNYA_ANSI_SHADOW = [
    "███████╗██╗  ██╗██╗   ██╗███╗   ██╗██╗   ██╗ █████╗ ",
    "██╔════╝██║  ██║██║   ██║████╗  ██║╚██╗ ██╔╝██╔══██╗",
    "███████╗███████║██║   ██║██╔██╗ ██║ ╚████╔╝ ███████║",
    "╚════██║██╔══██║██║   ██║██║╚██╗██║  ╚██╔╝  ██╔══██║",
    "███████║██║  ██║╚██████╔╝██║ ╚████║   ██║   ██║  ██║",
    "╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝",
]

# Collection of all banners
BANNERS = {
    "ansi_shadow": SHUNYA_ANSI_SHADOW,
}

# Default banner
DEFAULT_BANNER = "ansi_shadow"
