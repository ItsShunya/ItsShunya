"""SVG generator module for creating SVG documents with text elements and styling."""

from style.themes import ColorScheme, Theme


class SvgGenerator:
    def __init__(
        self,
        width: int = 1000,
        height: int = 600,
        theme: ColorScheme = Theme.NORD,
    ) -> None:
        """
        Initialize the SVG generator with specified dimensions.

        Parameters
        ----------
        width : int, optional
            Width of the SVG canvas in pixels (default is 1000)
        height : int, optional
            Height of the SVG canvas in pixels (default is 600)
        theme : ColorScheme, optional
            Color scheme to use for styling (default is Theme.TOKYO_NIGHT)
        """
        self.width: int = width
        self.height: int = height
        self.theme: ColorScheme = theme
        self.content: list[str] = []
        self._init_svg()

    def _init_svg(self) -> None:
        """
        Initialize the SVG file with header and basic structure.

        Returns
        -------
        None
        """
        self._set_xml_header()
        self._create_svg_tag()
        self._create_style_tag()
        self._create_rect_tag()

    def _set_xml_header(self) -> None:
        """
        Set the XML header for the SVG document.

        Returns
        -------
        None
        """
        self.content.append('<?xml version="1.0" encoding="UTF-8"?>')

    def _create_svg_tag(self) -> None:
        """
        Create the SVG root tag with specified dimensions.

        Returns
        -------
        None
        """
        svg_tag = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}">'
        self.content.append(svg_tag)

    def _create_style_tag(self) -> None:
        """
        Create the style tag with CSS for styling elements.

        Returns
        -------
        None
        """
        t = self.theme
        style = f'''<style>
                .ascii {{
                    font-family: JetBrains Mono, monospace;
                    font-size: 14px;
                    fill: {t.ascii};
                    font-weight: normal;
                }}
                .key {{
                    font-family: JetBrains Mono, monospace;
                    font-size: 12px;
                    fill: {t.key};
                    font-weight: normal;
                }}
                .value {{
                    font-family: JetBrains Mono, monospace;
                    font-size: 12px;
                    fill: {t.value};
                    font-weight: normal;
                }}
                .cc {{
                    font-family: JetBrains Mono, monospace;
                    font-size: 12px;
                    fill: {t.cc};
                    font-weight: normal;
                }}
                .prompt {{
                    font-family: JetBrains Mono, monospace;
                    font-size: 14px;
                    fill: {t.prompt};
                    font-weight: normal;
                }}
                .command {{
                    font-family: JetBrains Mono, monospace;
                    font-size: 14px;
                    fill: {t.command};
                    font-weight: normal;
                }}
                .string {{
                    font-family: JetBrains Mono, monospace;
                    font-size: 14px;
                    fill: {t.string};
                    font-weight: normal;
                }}
                .comment {{
                    font-family: JetBrains Mono, monospace;
                    font-size: 14px;
                    fill: {t.comment};
                    font-style: normal;
                }}
                .error {{
                    font-family: JetBrains Mono, monospace;
                    font-size: 14px;
                    fill: {t.error};
                    font-weight: normal;
                }}
                .success {{
                    font-family: JetBrains Mono, monospace;
                    font-size: 14px;
                    fill: {t.success};
                }}
                .warning {{
                    font-family: JetBrains Mono, monospace;
                    font-size: 14px;
                    fill: {t.warning};
                    font-weight: normal;
                }}
                .highlight {{
                    font-family: JetBrains Mono, monospace;
                    font-size: 14px;
                    fill: {t.highlight};
                    font-weight: normal;
                }}
                .dim {{
                    font-family: JetBrains Mono, monospace;
                    font-size: 14px;
                    fill: {t.dim};
                }}
                .accent1 {{
                    font-family: JetBrains Mono, monospace;
                    font-size: 14px;
                    fill: {t.accent1};
                    font-weight: normal;
                }}
                .accent2 {{
                    font-family: JetBrains Mono, monospace;
                    font-size: 14px;
                    fill: {t.accent2};
                    font-weight: normal;
                }}
                .accent3 {{
                    font-family: JetBrains Mono, monospace;
                    font-size: 14px;
                    fill: {t.accent3};
                    font-weight: normal;
                }}
                .separator {{
                    font-family: JetBrains Mono, monospace;
                    font-size: 12px;
                    fill: {t.separator};
                }}
            </style>'''
        self.content.append(style)

    def _create_rect_tag(self) -> None:
        """
        Create a background rectangle covering the entire canvas.

        Returns
        -------
        None
        """
        self.content.append(f'<rect width="100%" height="100%" fill="{self.theme.background}"/>')

    def create_text_element(
        self,
        x: int | float,
        y: int | float,
        text: str,
        text_class: str = "cc",
        id: str | None = None
    ) -> str:
        """
        Create a text element with tspan for SVG rendering.

        Parameters
        ----------
        x : int or float
            X-coordinate position of the text
        y : int or float
            Y-coordinate position of the text
        text : str
            Text content to display
        text_class : str, optional
            CSS class for styling the text (default is "cc")
        id : str, optional
            Identificator to be re-used for the tspan.

        Returns
        -------
        str
            The generated text element as an SVG string
        """
        id_str = ' id="{id}" ' if id else ''
        text_element = (
            f'<text x="{x}" y="{y}" class="{text_class}"{id_str} xml:space="preserve">'
            f'<tspan>{text}</tspan>'
            f'</text>'
        )
        self.content.append(text_element)
        return text_element

    def create_colored_text(
        self,
        x: int | float,
        y: int | float,
        segments: list[tuple[str, str]],
    ) -> str:
        """
        Create a text element with multiple colored segments on the same line.

        Parameters
        ----------
        x : int or float
            X-coordinate position of the text
        y : int or float
            Y-coordinate position of the text
        segments : list[tuple[str, str]]
            List of (text, class_name) tuples for each colored segment

        Returns
        -------
        str
            The generated text element as an SVG string
        """
        text_element = f'<text x="{x}" y="{y}" xml:space="preserve">'

        for text, class_name in segments:
            text_element += f'<tspan class="{class_name}">{text}</tspan>'

        text_element += '</text>'
        self.content.append(text_element)
        return text_element

    def create_multiple_tspan(
        self,
        x: int | float,
        y: int | float,
        text_lines: list[str],
        text_class: str = "ascii",
        line_height: int = 18,
    ) -> str:
        """
        Create a text element with multiple tspan elements for multi-line text.

        Parameters
        ----------
        x : int or float
            X-coordinate position of the text
        y : int or float
            Y-coordinate position of the text
        text_lines : list of str
            List of text lines to display
        text_class : str, optional
            CSS class for styling the text (default is "ascii")
        line_height : int, optional
            Vertical spacing between lines in pixels (default is 18)

        Returns
        -------
        str
            The generated text element with multiple tspan as an SVG string
        """
        text_element = f'<text x="{x}" y="{y}" class="{text_class}" xml:space="preserve">'

        for i, line in enumerate(text_lines):
            dy = 0 if i == 0 else line_height
            text_element += f'<tspan x="{x}" dy="{dy}">{line}</tspan>\n'

        text_element += '</text>'
        self.content.append(text_element)
        return text_element

    def create_ascii_logo(
        self,
        x: int | float,
        y: int | float,
        logo_lines: list[tuple[str, str]],
        line_height: int = 18,
    ) -> None:
        """
        Create an ASCII art logo with individual color classes per line.

        Parameters
        ----------
        x : int or float
            X-coordinate position of the logo
        y : int or float
            Y-coordinate position of the logo
        logo_lines : list of tuple[str, str]
            List of (line_content, color_class) tuples for each line
        line_height : int, optional
            Vertical spacing between lines in pixels (default is 18)

        Returns
        -------
        None
        """
        for i, (line, color_class) in enumerate(logo_lines):
            self.create_text_element(x, y + (i * line_height), line, color_class)

    def save(
        self,
        filename: str = "output.svg",
    ) -> None:
        """
        Save the SVG content to a file.

        Parameters
        ----------
        filename : str, optional
            Output filename for the SVG file (default is "output.svg")

        Returns
        -------
        None

        Raises
        ------
        IOError
            If there is an error writing to the file
        """
        with open(filename, 'w') as f:
            f.write('\n'.join(self.content))
            f.write('\n</svg>')
