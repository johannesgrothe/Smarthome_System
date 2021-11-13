"""Module for the markdown file writer"""
from abc import abstractmethod, ABCMeta
from typing import Optional


class MarkdownElementError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MarkdownElement(metaclass=ABCMeta):
    """Superclass for all markdown elements"""

    def __init__(self):
        pass

    @abstractmethod
    def render_contend(self) -> list[str]:
        """
        Renders the element into writable markdown file lines

        :return: A list of all lines rendered from the element
        """


class MarkdownTable(MarkdownElement):
    _header: list[str]
    _lines: list[list[str]]

    def __init__(self, header: list[str]):
        super().__init__()
        self._header = header
        self._lines = []

    @staticmethod
    def _max_str_length(data: list[str]) -> int:
        return max([len(x) for x in data])

    @staticmethod
    def _format_str(data: str, length: int) -> str:
        return data + " " * (length - len(data))

    @classmethod
    def _format_line(cls, data: list[str], max_length) -> str:
        return " | ".join([cls._format_str(x, max_length) for x in data]).strip()

    def _get_max_elem_length(self) -> int:
        line_lengths = [self._max_str_length(x)
                        for x
                        in self._lines]
        line_lengths.append(self._max_str_length(self._header))
        return max(line_lengths)

    def add_line(self, line: list[str]):
        if len(line) != len(self._header):
            raise MarkdownElementError(f"Length of passed list ({len(line)}) "
                                       f"does not match length of header ({len(self._header)})")
        self._lines.append(line)

    def render_contend(self) -> list[str]:
        lines = []
        max_len = self._get_max_elem_length()

        lines.append(self._format_line(self._header, max_len))
        lines.append(self._format_line(["-" * max_len for _ in self._header], max_len))
        for line in self._lines:
            lines.append(self._format_line(line, max_len))
        return lines


class MarkdownHeader(MarkdownElement):
    _text: str
    _level: int

    def __init__(self, text: str, level: int):
        super().__init__()
        self._text = text
        self._level = level

    def render_contend(self) -> list[str]:
        return [f"{'#' * (self._level + 1)} {self._text}"]


class MarkdownText(MarkdownElement):
    _text: str

    def __init__(self, text: str):
        super().__init__()
        self._text = text

    def render_contend(self) -> list[str]:
        return [self._text]


class MarkdownDivider(MarkdownElement):
    """A horizontal line"""

    def __init__(self):
        super().__init__()

    def render_contend(self) -> list[str]:
        return ["-----"]


class MarkdownCode(MarkdownElement):
    """Code-block for the markdown file"""
    _code: str
    _code_block: bool
    _language: Optional[str]

    def __init__(self, code_lines: str, block: bool = True, language: Optional[str] = None):
        super().__init__()
        self._code = code_lines
        self._code_block = block
        self._language = language

    def render_contend(self) -> list[str]:
        borders = "`"
        if self._code_block:
            borders = "```"
        out_str = borders
        if self._language:
            out_str += self._language
        out_str += "\n"
        out_str += self._code
        out_str += "\n"
        out_str += borders
        return [out_str]


class MarkdownList(MarkdownElement):
    """Contains a markdown list"""
    _lines: list[str]

    def __init__(self):
        super().__init__()
        self._lines = []

    def add_line(self, text: str):
        """
        Adds an entry to the markdown list

        :param text: Entry to add
        :return: None
        """
        self._lines.append(text)

    def render_contend(self) -> list[str]:
        out_data = [f"- {x}" for x in self._lines]
        return out_data


class MarkdownFile:
    """Contains a markdown file for editing and saving"""
    _elements: list[MarkdownElement]

    def __init__(self):
        self._elements = []

    def add(self, elem: MarkdownElement):
        """
        Adds a element to the markdown file

        :param elem: Element to add
        :return: None
        """
        self._elements.append(elem)

    def save(self, filename: str):
        """
        Saves the markdown file to the disk

        :param filename: Name of the file to add
        :return: None
        """
        lines = []
        for elem in self._elements:
            elem_lines = elem.render_contend()
            elem_lines[len(elem_lines) - 1] = elem_lines[len(elem_lines) - 1] + "\n"
            lines += elem_lines
        with open(filename, "w") as file_p:
            out_lines = [x + "\n" for x in lines]
            file_p.writelines(out_lines)
