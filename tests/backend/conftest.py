import pytest
from ipykernel.comm import Comm
from ipywidgets import Widget

from ipychart import Chart


class MockComm(Comm):
    """A mock Comm object.

    Can be used to inspect calls to Comm's open/send/close methods.
    """

    comm_id = "a-b-c-d"
    kernel = "Truthy"

    def __init__(self, *args, **kwargs):
        self.log_open = []
        self.log_send = []
        self.log_close = []
        super().__init__(*args, **kwargs)

    def open(self, *args, **kwargs):
        self.log_open.append((args, kwargs))

    def send(self, *args, **kwargs):
        self.log_send.append((args, kwargs))

    def close(self, *args, **kwargs):
        self.log_close.append((args, kwargs))


_widget_attrs = {}
undefined = object()


@pytest.fixture
def mock_comm():
    _widget_attrs["_comm_default"] = getattr(
        Widget, "_comm_default", undefined
    )
    Widget._comm_default = lambda self: MockComm()
    _widget_attrs["_repr_mimebundle_"] = Widget._repr_mimebundle_

    def raise_not_implemented(*args, **kwargs):
        raise NotImplementedError()

    Widget._ipython_display_ = raise_not_implemented

    yield MockComm()

    for attr, value in _widget_attrs.items():
        if value is undefined:
            delattr(Widget, attr)
        else:
            setattr(Widget, attr, value)


@pytest.fixture
def sample_chart():
    """Fixture to create a sample chart for testing."""
    data = {"labels": ["A", "B", "C"], "datasets": [{"data": [1, 2, 3]}]}
    options = {"title": {"display": True, "text": "Sample Chart"}}
    return Chart(data=data, kind="bar", options=options)
