"""Smoke test: Client imports cleanly and is instantiable."""


def test_client_imports_cleanly():
    from mlbapi.client import Client
    assert Client is not None


def test_client_instantiates():
    from mlbapi.client import Client
    c = Client()
    assert c is not None
