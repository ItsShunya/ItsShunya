"""Theme configuration module for SVG color schemes."""

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class ColorScheme:
    """
    Color scheme definition for SVG styling.

    Attributes
    ----------
    background : str
        Background color
    ascii : str
        Default text color
    key : str
        Key/label color
    value : str
        Value color
    cc : str
        Secondary/muted color
    prompt : str
        Shell prompt color
    command : str
        Command color
    string : str
        String/argument color
    comment : str
        Comment color
    error : str
        Error message color
    success : str
        Success message color
    warning : str
        Warning message color
    highlight : str
        Highlight color
    dim : str
        Dimmed text color
    """

    background: str
    ascii: str
    key: str
    value: str
    cc: str
    prompt: str
    command: str
    string: str
    comment: str
    error: str
    success: str
    warning: str
    highlight: str
    dim: str


class Theme:
    """Predefined color themes for terminal-style SVG output."""

    TOKYO_NIGHT: ClassVar[ColorScheme] = ColorScheme(
        background="#1a1b26",
        ascii="#c0caf5",
        key="#7aa2f7",
        value="#bb9af7",
        cc="#565f89",
        prompt="#7dcfff",
        command="#9ece6a",
        string="#e0af68",
        comment="#565f89",
        error="#f7768e",
        success="#9ece6a",
        warning="#ff9e64",
        highlight="#ff007c",
        dim="#414868",
    )

    DRACULA: ClassVar[ColorScheme] = ColorScheme(
        background="#282a36",
        ascii="#f8f8f2",
        key="#8be9fd",
        value="#bd93f9",
        cc="#6272a4",
        prompt="#50fa7b",
        command="#50fa7b",
        string="#f1fa8c",
        comment="#6272a4",
        error="#ff5555",
        success="#50fa7b",
        warning="#ffb86c",
        highlight="#ff79c6",
        dim="#44475a",
    )

    NORD: ClassVar[ColorScheme] = ColorScheme(
        background="#2e3440",
        ascii="#eceff4",
        key="#88c0d0",
        value="#b48ead",
        cc="#4c566a",
        prompt="#8fbcbb",
        command="#a3be8c",
        string="#ebcb8b",
        comment="#4c566a",
        error="#bf616a",
        success="#a3be8c",
        warning="#d08770",
        highlight="#b48ead",
        dim="#3b4252",
    )

    GRUVBOX_DARK: ClassVar[ColorScheme] = ColorScheme(
        background="#282828",
        ascii="#ebdbb2",
        key="#83a598",
        value="#d3869b",
        cc="#665c54",
        prompt="#8ec07c",
        command="#b8bb26",
        string="#fabd2f",
        comment="#928374",
        error="#fb4934",
        success="#b8bb26",
        warning="#fe8019",
        highlight="#d3869b",
        dim="#504945",
    )

    MONOKAI: ClassVar[ColorScheme] = ColorScheme(
        background="#272822",
        ascii="#f8f8f2",
        key="#66d9ef",
        value="#ae81ff",
        cc="#75715e",
        prompt="#a6e22e",
        command="#a6e22e",
        string="#e6db74",
        comment="#75715e",
        error="#f92672",
        success="#a6e22e",
        warning="#fd971f",
        highlight="#f92672",
        dim="#49483e",
    )

    CATPPUCCIN_MOCHA: ClassVar[ColorScheme] = ColorScheme(
        background="#1e1e2e",
        ascii="#cdd6f4",
        key="#89b4fa",
        value="#cba6f7",
        cc="#6c7086",
        prompt="#94e2d5",
        command="#a6e3a1",
        string="#f9e2af",
        comment="#6c7086",
        error="#f38ba8",
        success="#a6e3a1",
        warning="#fab387",
        highlight="#f5c2e7",
        dim="#45475a",
    )
