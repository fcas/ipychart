import pytest

from ipychart import Chart
from ipychart.utils.exceptions import (
    InvalidChartDataError,
    InvalidChartKindError,
)


@pytest.fixture
def chart():
    return Chart(data={"datasets": [{"data": [1, 2, 3]}]}, kind="bar")


@pytest.mark.parametrize("invalid_kind", ["foo", 123, None])
def test_kind_setter_with_invalid_value(chart, invalid_kind):
    with pytest.raises(InvalidChartKindError):
        chart.kind = invalid_kind


@pytest.mark.parametrize(
    "invalid_data",
    [
        {"a": 1, "b": 2},
        {"datasets": "not a list"},
        {"datasets": [{"data": None}]},
    ],
)
def test_data_setter_with_invalid_value(chart, invalid_data):
    with pytest.raises(InvalidChartDataError):
        chart.data = invalid_data


def test_options_setter(chart):
    chart.options = {"title": {"display": True, "text": "Test Chart"}}
    assert chart.options["title"]["text"] == "Test Chart"


def test_colorscheme_setter(chart):
    chart.colorscheme = "tableau.Tableau20"
    assert chart.colorscheme == "tableau.Tableau20"


def test_zoom_setter(chart):
    chart.zoom = False
    assert chart.zoom is False
