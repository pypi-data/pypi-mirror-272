import pytest


class FakeConsul:
    def __init__(self):
        self.__values = {}

    def set(self, key: str, value: str):
        self.__values[key] = value

    def get(self, key: str) -> tuple[bool, str | None]:
        return key in self.__values.keys(), self.__values.get(key)

    def clear(self):
        self.__values.clear()


consul = FakeConsul()


@pytest.fixture(scope='function')
def mock_consul(monkeypatch):
    monkeypatch.setattr('edgegap_consul.ConsulReader.get', consul.get)
    monkeypatch.setattr('edgegap_consul.ConsulReader.check', lambda _: True)

    try:
        yield consul
    finally:
        consul.clear()
