# import pytest
#
#
# def pytest_addoption(parser):
#     parser.addoption(
#         "--repeat-regression",
#         action="store",
#         default=1,
#         type=int,
#         help="Number of times to repeat the entire test suite."
#     )
#
#
# @pytest.hookimpl(tryfirst=True)
# def pytest_collection_modifyitems(session, config, items):
#     repeat_count = config.getoption("--repeat-regression")
#     session.repeat_count = repeat_count
#
#
# @pytest.hookimpl(tryfirst=True)
# def pytest_runtestloop(session):
#     items = list(session.items)
#     for i in range(session.repeat_count):
#         print(f"\nIteration {i + 1}/{session.repeat_count}")
#         for item in items:
#             item.config.hook.pytest_runtest_protocol(item=item, nextitem=None)
#     return True


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


@pytest.hookimpl(tryfirst=True)
def pytest_runtestloop(session):
    repeat_count = session.repeat_count
    items = list(session.items)

    if repeat_count > 1:
        for i in range(repeat_count):
            print(f"\nIteration {i + 1}/{repeat_count}")
            for item in items:
                item.config.hook.pytest_runtest_protocol(item=item, nextitem=None)
        return True
    else:
        for item in items:
            item.config.hook.pytest_runtest_protocol(item=item, nextitem=None)
        return True
