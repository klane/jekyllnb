def pytest_configure(config):
    config.addinivalue_line("markers", "unix: mark test to run only on Unix systems")
