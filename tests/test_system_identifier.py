from utils.system_identifier import IntSystemIdentifier, StringSystemIdentifier


class TestIntIdentifier(IntSystemIdentifier):
    zero = 0
    one = 1
    two = 2


class TestStringIdentifier(StringSystemIdentifier):
    zero = "_"
    one = "_blub"
    two = "_blub_blub"


def test_system_identifier_int():
    assert TestIntIdentifier.get_attributes() == ["zero", "one", "two"]
    assert TestIntIdentifier.from_int(1) == TestIntIdentifier.one
    assert TestIntIdentifier.from_string("one") == TestIntIdentifier.one
    assert TestIntIdentifier.one.to_string() == "one"
    assert TestIntIdentifier.one.to_int() == 1


def test_system_identifier_string():
    assert TestStringIdentifier.get_attributes() == ["zero", "one", "two"]
    assert TestStringIdentifier.from_string("one") == TestStringIdentifier.one
    assert TestStringIdentifier.one.to_string() == "one"
