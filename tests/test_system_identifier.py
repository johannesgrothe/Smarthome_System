from utils.system_identifier import IntSystemIdentifier, StringSystemIdentifier


class BufIntIdentifier(IntSystemIdentifier):
    zero = 0
    one = 1
    two = 2


class BufStringIdentifier(StringSystemIdentifier):
    zero = "_"
    one = "_blub"
    two = "_blub_blub"


def test_system_identifier_int():
    assert BufIntIdentifier.get_attributes() == ["zero", "one", "two"]
    assert BufIntIdentifier.from_int(1) == BufIntIdentifier.one
    assert BufIntIdentifier.from_string("one") == BufIntIdentifier.one
    assert BufIntIdentifier.one.to_string() == "one"
    assert BufIntIdentifier.one.to_int() == 1


def test_system_identifier_string():
    assert BufStringIdentifier.get_attributes() == ["zero", "one", "two"]
    assert BufStringIdentifier.from_string("one") == BufStringIdentifier.one
    assert BufStringIdentifier.one.to_string() == "one"
