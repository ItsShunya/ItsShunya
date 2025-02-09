class SvgGenerator:
    def __init__(self, width=1000, height=600):
        self.width = width
        self.height = height
        self.content = []
        self._init_svg()

    def _init_svg(self):
        """Initialize the SVG file with header and basic structure"""
        self._set_xml_header()
        self._create_svg_tag()
        self._create_style_tag()
        self._create_rect_tag()

    def _set_xml_header(self):
        """Set the XML header"""
        self.content.append('<?xml version="1.0" encoding="UTF-8"?>')

    def _create_svg_tag(self):
        """Create the SVG root tag"""
        svg_tag = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}">'
        self.content.append(svg_tag)

    def _create_style_tag(self):
        """Create the style tag with CSS"""
        style = '''
            <style>
                .ascii {
                    font-family: monospace;
                    font-size: 14px;
                    fill: #ffffff;
                }
                .key {
                    font-family: Arial, sans-serif;
                    font-size: 12px;
                    fill: #b3b3b3;
                }
                .value {
                    font-family: Arial, sans-serif;
                    font-size: 12px;
                    fill: #ffffff;
                }
                .cc {
                    fill: #333333;
                }
            </style>
        '''
        self.content.append(style.strip())

    def _create_rect_tag(self):
        """Create a background rectangle"""
        rect_tag = '<rect width="100%" height="100%" fill="#1a1a1a"/>'
        self.content.append(rect_tag)

    def create_text_element(self, x, y, text, text_class="ascii"):
        """Create a text element with tspan"""
        text_element = f'<text x="{x}" y="{y}" class="{text_class}">'
        text_element += f'<tspan>{text}</tspan>'
        text_element += '</text>'
        self.content.append(text_element)
        return text_element

    def create_multiple_tspan(self, x, y, text_lines, text_class="ascii"):
        """Create a text element with multiple tspan elements"""
        text_element = f'<text x="{x}" y="{y}" class="{text_class}">'
        for line in text_lines:
            text_element += f'<tspan>{line}</tspan>'
        text_element += '</text>'
        self.content.append(text_element)
        return text_element

    def save(self, filename="output.svg"):
        """Save the SVG content to a file"""
        with open(filename, 'w') as f:
            f.write('\n'.join(self.content))
            f.write('</svg>')
