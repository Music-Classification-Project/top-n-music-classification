import pytest
from backend.model_interface.flask_app.__init__ import create_app

"""
Provides Flask app/test-client fixtures for dummy and non-dummy service modes
"""
@pytest.fixture
def app_dummy():
    app = create_app({"TESTING": True, "USE_DUMMY_SERVICE": True})
    yield app


@pytest.fixture
def client_dummy(app_dummy):
    return app_dummy.test_client()


@pytest.fixture
def app_nodummy():
    app = create_app({"TESTING": True, "USE_DUMMY_SERVICE": False})
    yield app


@pytest.fixture
def client_nodummy(app_nodummy):
    return app_nodummy.test_client()

