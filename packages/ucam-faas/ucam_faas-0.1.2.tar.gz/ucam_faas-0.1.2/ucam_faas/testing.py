from . import _initialize_ucam_faas_app

try:
    from pytest import fixture

    @fixture
    def event_app_client():
        def _event_app_client(target, source=None):
            test_app = _initialize_ucam_faas_app(target, source, True)
            return test_app.test_client()

        return _event_app_client

except ImportError:
    pass
