import pytest

from saulve.errors import MissingAttribute, WrongAttributeType
from saulve.import_module import import_instance


def test_module_must_have_attribute() -> None:
    with pytest.raises(MissingAttribute) as exc_info:
        import_instance('tests.import_module.test_module', 'nothing', str)

    exc_msg = str(exc_info.value)
    assert "test_module does not have a 'nothing' attribute" in exc_msg


def test_module_attribute_must_be_instance_of() -> None:
    with pytest.raises(WrongAttributeType) as exc_info:
        import_instance('tests.import_module.test_module', 'not_a_string', str)

    exc_msg = str(exc_info.value)
    assert "test_module.not_a_string is not a str instance" in exc_msg


def test_import_module_attribute() -> None:
    imported = import_instance(
        'tests.import_module.test_module',
        'a_string',
        str)

    assert imported == 'a string'
