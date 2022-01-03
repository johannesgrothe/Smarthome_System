from abc import abstractmethod, ABCMeta
from typing import Union

_indentation_depth = 4


class JSElement(metaclass=ABCMeta):

    @staticmethod
    def _render_indent(indentation: int) -> str:
        return " " * _indentation_depth * indentation

    @abstractmethod
    def render_content(self, indentation: int) -> [str]:
        """
        Renders the content of the JS element into lines of code

        :return: the lines of code as strings
        """


class JSContainer(metaclass=ABCMeta):
    _elements: list[JSElement]

    def __init__(self):
        self._elements = []

    def add(self, elem: JSElement):
        """
        Adds an element to the JS file

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


class JSImport(JSElement):
    _name: str
    _in_package: bool

    def __init__(self, name: str, in_package: bool):
        self._name = name
        self._in_package = in_package

    def render_content(self, indentation: int) -> [str]:
        include_buf = f"\"{self._name}\"" if self._in_package else f"<{self._name}>"
        return [self._render_indent(indentation) + f"#include {include_buf}"]

