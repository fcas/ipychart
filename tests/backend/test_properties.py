import pytest

from ipychart.utils.exceptions import (
    InvalidChartDataError,
    InvalidChartKindError,
)


@pytest.mark.parametrize("invalid_kind", ["foo", 123, None])
def test_kind_setter_with_invalid_value(sample_chart, invalid_kind):
    with pytest.raises(InvalidChartKindError):
        sample_chart.kind = invalid_kind


@pytest.mark.parametrize(
    "invalid_data",
    [
        {"a": 1, "b": 2},
        {"datasets": "not a list"},
        {"datasets": [{"data": None}]},
    ],
)
def test_data_setter_with_invalid_value(sample_chart, invalid_data):
    with pytest.raises(InvalidChartDataError):
        sample_chart.data = invalid_data


def test_options_setter(sample_chart):
    sample_chart.options = {"title": {"display": True, "text": "Test Chart"}}
    assert sample_chart.options["title"]["text"] == "Test Chart"


def test_colorscheme_setter(sample_chart):
    sample_chart.colorscheme = "tableau.Tableau20"
    assert sample_chart.colorscheme == "tableau.Tableau20"


def test_zoom_setter(sample_chart):
    sample_chart.zoom = False
    assert sample_chart.zoom is False
