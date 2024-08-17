import os
from unittest.mock import MagicMock, mock_open, patch

import pytest

from ipychart import Chart


@pytest.fixture
def sample_chart():
    data = {"labels": ["A", "B", "C"], "datasets": [{"data": [1, 2, 3]}]}
    options = {"title": {"display": True, "text": "Sample Chart"}}
    return Chart(data=data, kind="bar", options=options)


def test_get_html_template(sample_chart):
    html = sample_chart.get_html_template()

    assert "<script src=" in html
    assert "application/vnd.jupyter.widget-state+json" in html
    assert "application/vnd.jupyter.widget-view+json" in html


def test_get_python_template(sample_chart):
    python_code = sample_chart.get_python_template()

    assert "data =" in python_code
    assert "options =" in python_code
    assert "Chart(data=data, kind='bar', options=options" in python_code


def test_to_image_invalid_directory(sample_chart):
    with pytest.raises(FileNotFoundError):
        sample_chart.to_image("/non/existent/path/test.png")


def test_to_image_directory_as_path(sample_chart, tmpdir):
    with pytest.raises(ValueError):
        sample_chart.to_image(tmpdir)


def test_to_html(sample_chart, tmpdir):
    temp_file = tmpdir.join("test.html")
    sample_chart.to_html(str(temp_file))
    assert os.path.exists(temp_file)
    assert os.path.getsize(temp_file) > 0
