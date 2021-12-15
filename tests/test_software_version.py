import pytest

from utils.software_version import SoftwareVersion


def test_software_version_operators():
    with pytest.raises(ValueError):
        SoftwareVersion.from_string("2.4")
    with pytest.raises(ValueError):
        SoftwareVersion.from_string("2.4.3.5")

    assert SoftwareVersion.from_string("2.4.11") == SoftwareVersion(2, 4, 11)
    assert str(SoftwareVersion(1, 0, 8)) == "1.0.8"
    assert SoftwareVersion(1, 0, 8) == SoftwareVersion(1, 0, 8)
    assert SoftwareVersion(1, 0, 8) != SoftwareVersion(1, 0, 9)

    assert SoftwareVersion(1, 0, 8) < SoftwareVersion(1, 0, 9)
    assert SoftwareVersion(1, 0, 8) > SoftwareVersion(1, 0, 7)


def test_software_version_follows():
    assert SoftwareVersion(2, 3, 8).follows(SoftwareVersion(2, 3, 7))
    assert SoftwareVersion(2, 3, 0).follows(SoftwareVersion(2, 2, 7))
    assert SoftwareVersion(3, 0, 0).follows(SoftwareVersion(2, 3, 7))

    assert not SoftwareVersion(2, 3, 8).follows(SoftwareVersion(2, 3, 8))
    assert not SoftwareVersion(2, 3, 8).follows(SoftwareVersion(2, 3, 9))
    assert not SoftwareVersion(2, 3, 8).follows(SoftwareVersion(2, 2, 13))

    assert not SoftwareVersion(3, 0, 1).follows(SoftwareVersion(2, 3, 7))
    assert not SoftwareVersion(3, 1, 0).follows(SoftwareVersion(2, 3, 7))
    assert not SoftwareVersion(4, 0, 0).follows(SoftwareVersion(2, 3, 7))

