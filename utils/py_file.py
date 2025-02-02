from abc import abstractmethod, ABCMeta
from typing import Union, List

_indentation_depth = 4


class PythonElement(metaclass=ABCMeta):

    @staticmethod
    def _render_indent(indentation: int) -> str:
        return " " * _indentation_depth * indentation

    @abstractmethod
    def render_content(self, indentation: int) -> [str]:
        """
        Renders the content of the C++ element into lines of code

        :return: the lines of code as strings
        """


class PythonContainer(metaclass=ABCMeta):
    _elements: list[PythonElement]

    def __init__(self):
        self._elements = []

    def add(self, elem: PythonElement):
        """
        Adds an element to the C++ file

        :param elem: Element to add
        :return: None
        """
        self._elements.append(elem)

    def _render_elements(self, indentation: int) -> [str]:
        lines = []
        for elem in self._elements:
            elem_lines = elem.render_content(indentation)
            elem_lines[len(elem_lines) - 1] = elem_lines[len(elem_lines) - 1]
            lines += elem_lines
        return lines


class PythonElementsImport(PythonElement):
    _package: str
    _elements: List[str]

    def __init__(self, package: str, elements: List[str]):
        self._package = package
        self._elements = elements

    def render_content(self, indentation: int) -> [str]:
        elem_list = ", ".join(sorted(self._elements))
        return [self._render_indent(indentation) + f"from {self._package} import {elem_list}"]


class PythonPackageImport(PythonElement):
    _package: str

    def __init__(self, package: str):
        self._package = package

    def render_content(self, indentation: int) -> [str]:
        return [self._render_indent(indentation) + f"import {self._package}"]


class PythonBlankLine(PythonElement):
    _blank_lines: int

    def __init__(self, blank_lines: int = 0):
        self._blank_lines = blank_lines

    def render_content(self, indentation: int) -> [str]:
        return ["\n" * self._blank_lines]


class PythonComment(PythonElement):
    _content: List[str]
    _docstr: bool

    def __init__(self, content: str, docstring: bool = False):
        self._content = content.split("\n")
        self._docstr = docstring

    def render_content(self, indentation: int) -> [str]:
        if self._docstr:
            if len(self._content) == 1:
                return [f'{self._render_indent(indentation)}"""{self._content[0]}"""']
            return ([self._render_indent(indentation) + '"""'] +
                    [self._render_indent(indentation) + x for x in self._content] +
                    [self._render_indent(indentation) + '"""'])
        return [self._render_indent(indentation) + f"# {x}" for x in self._content]


class PythonEnum(PythonElement):
    class _PythonEnumElement(PythonElement):
        _name: str
        _value: int
        _docstring: str

        def __init__(self, name: str, value: int, docstring: str = ""):
            self._name = name
            self._value = value
            self._docstring = docstring

        def render_content(self, indentation: int) -> str:
            buf_comment = ""
            if self._docstring:
                buf_comment = f"  # {self._docstring}"
            return f"{self._render_indent(indentation)}{self._name} = {str(self._value)}{buf_comment}"

    _name: str
    _docstring: str
    _items: List[_PythonEnumElement]

    def __init__(self, name: str, docstring: str):
        super().__init__()
        self._name = name
        self._docstring = docstring
        self._items = []

    def add_element(self, name: str, value: int, docstring: str = ""):
        self._items.append(self._PythonEnumElement(name, value, docstring))

    def render_content(self, indentation: int) -> [str]:
        return [""] + \
            [self._render_indent(indentation) + "class " + self._name + "(enum.IntEnum):"] + \
            PythonComment(self._docstring, docstring=True).render_content(indentation + 1) + \
            [x.render_content(indentation + 1) for x in self._items]


class PythonFile(PythonContainer):
    """Contains a C++ file for editing and saving"""

    def save(self, filename: str):
        """
        Saves the C++ file to the disk

        :param filename: Name of the file to add
        :return: None
        """
        lines = self._render_elements(0)
        with open(filename, "w") as file_p:
            out_lines = [x + "\n" for x in lines]
            file_p.writelines(out_lines)
