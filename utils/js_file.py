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

    def __init__(self, name: str):
        self._name = name

    def render_content(self, indentation: int) -> [str]:
        return [self._render_indent(indentation) + f"import {self._name} from \"react\";"]


class JSBlankLine(JSElement):
    _blank_lines: int

    def __init__(self, blank_lines: int = 0):
        self._blank_lines = blank_lines

    def render_content(self, indentation: int) -> [str]:
        return ["\n" * self._blank_lines]


class JSVariable(JSElement):
    _type: str
    _name: str
    _value: Union[int, str]
    _docstring: str

    def __init__(self, var_type: str, name: str, value: Union[int, str], docstr: str = ""):
        self._type = var_type
        self._name = name
        self._value = value
        self._docstring = docstr

    def render_content(self, indentation: int) -> [str]:
        docstr_buf = "" if not self._docstring else f"  // {self._docstring}"
        value_buf = str(self._value) if isinstance(self._value, int) else f"\"{self._value}\""
        type_prefix = self._type
        type_suffix = ""
        if type_prefix.endswith("[]"):
            type_prefix = type_prefix[:-2].strip()
            type_suffix = "[] "

        return [self._render_indent(indentation) +
                f"{type_prefix} {self._name} {type_suffix}= {value_buf};{docstr_buf}"]


class JSComment(JSElement):
    _content: str

    def __init__(self, content: str):
        self._content = content

    def render_content(self, indentation: int) -> [str]:
        parts = self._content.split("\n")
        return [self._render_indent(indentation) + f"// {x}" for x in parts]


class JSConstantsClass(JSElement, JSContainer):
    _name: str
    _docstring: str

    def __init__(self, name: str, docstring: str):
        super().__init__()
        self._name = name
        self._docstring = docstring

    def render_content(self, indentation: int) -> [str]:
        return [""] + \
               JSComment(self._docstring).render_content(indentation) + \
               [self._render_indent(indentation) + "export default class " + self._name + " {"] + \
               self._render_elements(indentation + 1) + \
               [self._render_indent(indentation) + "}"]


class JSFile(JSContainer):
    """Contains a JS file for editing and saving"""

    def save(self, filename: str):
        """
        Saves the JS file to the disk

        :param filename: Name of the file to add
        :return: None
        """
        lines = self._render_elements(0)
        with open(filename, "w") as file_p:
            out_lines = [x + "\n" for x in lines]
            file_p.writelines(out_lines)
