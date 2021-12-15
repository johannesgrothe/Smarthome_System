from lib.system_identifier import SystemIdentifier


class TestIdentifier(SystemIdentifier):
    zero = 0
    one = 1
    two = 2


def test_system_identifier():
    assert TestIdentifier.get_attributes() == ["zero", "one", "two"]
    assert TestIdentifier.from_int(1) == TestIdentifier.one
    assert TestIdentifier.from_string("one") == TestIdentifier.one
    assert TestIdentifier.one.to_string() == "one"
    assert TestIdentifier.one.to_int() == 1
