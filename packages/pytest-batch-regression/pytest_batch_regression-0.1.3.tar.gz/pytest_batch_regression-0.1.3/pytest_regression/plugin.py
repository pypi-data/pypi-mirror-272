import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--repeat-regression",
        action="store",
        default=1,
        type=int,
        help="Number of times to repeat the entire test suite."
    )


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(session, config, items):
    repeat_count = config.getoption("--repeat-regression")
    session.repeat_count = repeat_count


# pytest_regression/plugin.py

@pytest.hookimpl(tryfirst=True)
def pytest_runtestloop(session):
    original_items = list(session.items)
    for i in range(session.repeat_count):
        print(f"\nIteration {i + 1}/{session.repeat_count}")
        session.config.hook.pytest_sessionstart(session=session)
        session.items = list(original_items)
        session.config.hook.pytest_collection_modifyitems(session=session, config=session.config, items=session.items)
        exitstatus = session.config.hook.pytest_runtestloop(session=session)
        session.config.hook.pytest_sessionfinish(session=session, exitstatus=exitstatus)
    return True

