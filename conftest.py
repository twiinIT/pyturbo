def pytest_addoption(parser):
    parser.addoption(
        "--class-name",
        action="store",
        default=None,
        help="Run tests only for classes with this exact name",
    )