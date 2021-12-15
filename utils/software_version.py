"""Module for the software version class"""


class SoftwareVersion:
    """Class that represents a software version"""

    # Major version number
    major: int

    # Minor version number
    minor: int

    # Bugfix version number
    bugfix: int

    def __init__(self, major: int, minor: int, bugfix: int):
        self.major = major
        self.minor = minor
        self.bugfix = bugfix

    @classmethod
    def from_string(cls, version: str):
        data = [int(x) for x in version.split(".")]
        if len(data) != 3:
            raise ValueError(f"Cannot create SoftwareVersion from '{version}'")
        return SoftwareVersion(data[0], data[1], data[2])

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.bugfix}"

    def __gt__(self, other):
        return self.major > other.major or self.minor > other.minor or self.bugfix > other.bugfix

    def __lt__(self, other):
        return not self > other

    def __eq__(self, other):
        return self.major == other.major and self.minor == other.minor and self.bugfix == other.bugfix

    def __ne__(self, other):
        return not self == other

    def follows(self, other) -> bool:
        """
        Checks if this software version directly follows another one.

        :param other: Software version to compare with
        :return: True if this directly follows the other, False otherwise
        """
        if self.major != other.major:
            return self.major == other.major + 1 and self.minor == 0 and self.bugfix == 0
        elif self.minor != other.minor:
            return self.minor == other.minor + 1 and self.bugfix == 0
        elif self.bugfix != other.bugfix:
            return self.bugfix == other.bugfix + 1
        return False
