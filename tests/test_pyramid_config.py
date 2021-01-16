from typing import Dict

from filestorage import store, pyramid_config, StorageContainer


class MockPyramidRegistry:
    # No need to require Pyramid as a testing library - only need two objects.
    def __init__(self, settings):
        self.settings = settings


class MockPyramidConfig:
    # No need to require Pyramid as a testing library - only need two objects.

    def __init__(self, settings: Dict):
        self._settings = settings
        self.registry = MockPyramidRegistry(settings)
        self._request_methods: Dict = {}

    def get_settings(self):
        return self._settings

    def add_request_method(
        self, callable=None, name=None, property=False, reify=False
    ):
        self._request_methods[name] = callable

    def get_request_prop(self, name):
        return self._request_methods[name]()


def test_pyramid_includeme():
    settings = {
        'store.use_global': 'false',
        'store.handler': 'DummyHandler',
        'store.handler.base_url': 'http://foo.bar',
    }
    config = MockPyramidConfig(settings)
    pyramid_config.includeme(config)

    pyramid_store = config.get_request_prop('store')
    assert store is not pyramid_store
    assert isinstance(pyramid_store, StorageContainer)
    assert pyramid_store.base_url == 'http://foo.bar'


def test_pyramid_different_prop_name():
    settings = {
        'store.use_global': 'false',
        'store.name': 'my_store',
        'store.handler': 'DummyHandler',
        'store.handler.base_url': 'http://foo.bar',
    }
    config = MockPyramidConfig(settings)
    pyramid_config.includeme(config)

    pyramid_store = config.get_request_prop('my_store')
    assert store is not pyramid_store
    assert isinstance(pyramid_store, StorageContainer)
    assert pyramid_store.base_url == 'http://foo.bar'


def test_pyramid_no_config():
    settings = {}

    config = MockPyramidConfig(settings)
    pyramid_config.includeme(config)

    pyramid_store = config.get_request_prop('store')
    assert store is pyramid_store
    assert pyramid_store.finalized is False
