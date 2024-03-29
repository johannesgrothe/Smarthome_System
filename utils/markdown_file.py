"""Module for the markdown file writer"""
from abc import abstractmethod, ABCMeta, ABC
from typing import Optional, Union


class MarkdownElementError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MarkdownElement(metaclass=ABCMeta):
    """Superclass for all markdown elements"""

    def __init__(self):
        pass

    @abstractmethod
    def render_content(self) -> list[str]:
        """
        Renders the element into writable markdown file lines

        :return: A list of all lines rendered from the element
        """


class MarkdownHeader(MarkdownElement):
    _text: str
    _level: int

    def __init__(self, text: str, level: int):
        super().__init__()
        self._text = text
        self._level = level

    def render_content(self) -> list[str]:
        return [f"{'#' * (self._level + 1)} {self._text}"]


class MarkdownText(MarkdownElement):
    _text: str

    def __init__(self, text: str):
        super().__init__()
        self._text = text

    def render_content(self) -> list[str]:
        return [self._text]


class MarkdownDivider(MarkdownElement):
    """A horizontal line"""

    def __init__(self):
        super().__init__()

    def render_content(self) -> list[str]:
        return ["-----"]


class MarkdownLink(MarkdownElement, ABC):
    """Link to an internal or external resource"""
    _text: str
    _target: str
    _prefix_text: str

    def __init__(self, text: str, target: str, prefix_text: Optional[str] = None):
        super().__init__()
        self._text = text
        self._target = target
        if not prefix_text:
            self._prefix_text = ""
        else:
            self._prefix_text = prefix_text


class MarkdownInternalLinkGithub(MarkdownLink):
    """A link to an internal target on github"""

    def __init__(self, text: str, target: str, prefix_text: Optional[str] = None):
        # GitHub allows for internal links to other headlines
        buf_target = target.lower().strip().replace(".", "").replace(" ", "-")
        super().__init__(text, buf_target, prefix_text)

    def render_content(self) -> list[str]:
        return [f"{self._prefix_text}[{self._text}](#{self._target})"]


class MarkdownHyperLink(MarkdownLink):
    """A link to an external resource"""

    def __init__(self, text: str, target: str, prefix_text: Optional[str] = None):
        super().__init__(text, target, prefix_text)

    def render_content(self) -> list[str]:
        return [f"{self._prefix_text}[{self._text}]({self._target})"]


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

    def render_content(self) -> list[str]:
        borders = "`"
        if self._code_block:
            borders = "```"
        out_str = borders
        if self._language and self._code_block:
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

    # def add_line(self, text: str):
    def add_line(self, line: Union[str, MarkdownText, MarkdownLink]):
        """
        Adds an entry to the markdown list

        :param line: Entry to add
        :return: None
        """
        if isinstance(line, str):
            self._lines.append(line)
        else:
            self._lines.append(" ".join(line.render_content()))

    def render_content(self) -> list[str]:
        out_data = [f"- {x}" for x in self._lines]
        return out_data


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

    @staticmethod
    def _format_table_element(elem: Union[int, str, MarkdownText, MarkdownLink]) -> str:
        if isinstance(elem, str):
            return elem
        elif isinstance(elem, MarkdownElement):
            return " ".join(elem.render_content())
        else:
            return str(elem)

    @classmethod
    def _format_line(cls, data: list[str], lengths: list[int]) -> str:
        return "|" + "|".join([" " + cls._format_str(x, l) for x, l in zip(data, lengths)]) + "|"

    def _get_max_column_length(self, index: int):
        column_elems = [self._header[index]] + [x[index] for x in self._lines]
        elem_lengths = [len(x) for x in column_elems]
        return max(elem_lengths)

    def add_line(self, line: list[Union[int, str, MarkdownText, MarkdownLink]]):
        if len(line) != len(self._header):
            raise MarkdownElementError(f"Length of passed list ({len(line)}) "
                                       f"does not match length of header ({len(self._header)})")
        self._lines.append([self._format_table_element(x) for x in line])

    def render_content(self) -> list[str]:
        column_lengths = [self._get_max_column_length(x) + 1 for x in range(len(self._header))]

        lines = [self._format_line(self._header, column_lengths),
                 self._format_line(["-" * l for l in column_lengths], column_lengths).replace(" -", "--")]

        for line in self._lines:
            lines.append(self._format_line(line, column_lengths))
        return lines


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
            elem_lines = elem.render_content()
            elem_lines[len(elem_lines) - 1] = elem_lines[len(elem_lines) - 1] + "\n"
            lines += elem_lines
        with open(filename, "w") as file_p:
            out_lines = [x + "\n" for x in lines]
            file_p.writelines(out_lines)
