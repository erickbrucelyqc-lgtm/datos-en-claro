import io
from pathlib import Path

import pytest
from erick_dashboard import prepare_data
from streamlit.testing.v1 import AppTest


def test_csv_validation_and_nonfinite_amounts():
    text = "date,category,amount\n2026-01-01,Software,5\nbad,Software,3\n2026-01-02, ,9\n2026-01-03,Datos,inf\n"
    clean, rejected = prepare_data(io.StringIO(text))
    assert clean["amount"].sum() == 5
    assert rejected == 3
    with pytest.raises(ValueError):
        prepare_data(io.StringIO("foo,bar\n1,2"))
    with pytest.raises(ValueError):
        prepare_data(io.StringIO("date,category,amount\n"))


def test_dashboard_metrics_and_filter():
    app = AppTest.from_file(str(Path(__file__).with_name("erick_dashboard.py"))).run(
        timeout=30
    )
    assert not app.exception
    assert app.metric[0].value == "$11,750.00"
    assert app.metric[1].value == "10"
    app.sidebar.multiselect[0].set_value(["Software"]).run()
    assert not app.exception
    assert app.metric[0].value == "$4,450.00"
    app.sidebar.multiselect[0].set_value([]).run()
    assert not app.exception
    assert len(app.info) == 1
