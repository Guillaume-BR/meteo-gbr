import datetime

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from modules import table

DATES = [datetime.date(2026, 11, 23) + datetime.timedelta(days=k) for k in range(4)]


@pytest.fixture(autouse=True)
def no_network_no_figures(monkeypatch):
    # image_code télécharge les icônes : inutile (et lent) dans les tests
    monkeypatch.setattr(table, "image_code", lambda *_, **__: None)
    yield
    plt.close("all")


@pytest.fixture
def daily() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "time": [str(d) for d in DATES],
            "weathercode (wmo code)": [0, 3, 61, 95],
            "temperature_2m_max (°C)": [20.5, 18.0, 15.5, 12.0],
            "temperature_2m_min (°C)": [10.0, 9.5, 8.0, 5.5],
            "precipitation_sum (mm)": [0.0, 0.5, 4.0, 12.5],
            "windspeed_10m_max (km/h)": [25.0, 30.0, 35.0, 40.0],
            "winddirection_10m_dominant (°)": [90.0, 180.0, 270.0, 0.0],
        }
    )


@pytest.fixture
def hourly() -> pd.DataFrame:
    return pd.DataFrame({"time": range(96), "windspeed_10m (km/h)": [10.0] * 96})


def annotations(fig) -> list[str]:
    return [t.get_text() for t in fig.axes[0].texts]


def test_build_table_content(daily, hourly):
    fig = table.build_table(daily, hourly, DATES)

    assert annotations(fig) == [
        *["lun\n23\nnov", "mar\n24\nnov", "mer\n25\nnov", "jeu\n26\nnov"],
        *["20.5 °C", "18.0 °C", "15.5 °C", "12.0 °C"],
        *["10.0 °C", "9.5 °C", "8.0 °C", "5.5 °C"],
        *["0.0 mm", "0.5 mm", "4.0 mm", "12.5 mm"],
        *["10.0 km/h"] * 4,
    ]
    # 1 axe du tableau + 4 icônes + 4 gouttes + 4 flèches de vent
    assert len(fig.axes) == 13


def test_build_table_does_not_modify_inputs(daily, hourly):
    daily_before, hourly_before = daily.copy(), hourly.copy()

    table.build_table(daily, hourly, DATES)

    pd.testing.assert_frame_equal(daily, daily_before)
    pd.testing.assert_frame_equal(hourly, hourly_before)


def test_build_table_with_missing_days_and_variable(daily, hourly):
    """L'API peut omettre des jours ou une variable : le tableau reste affiché."""
    incomplete = daily.drop(columns="precipitation_sum (mm)").iloc[:2]

    fig = table.build_table(incomplete, hourly.iloc[:48], DATES)

    texts = annotations(fig)
    # une donnée manquante s'affiche "-" seul, sans unité
    assert texts[4:8] == ["20.5 °C", "18.0 °C", "-", "-"]  # tmax
    assert texts[8:12] == ["10.0 °C", "9.5 °C", "-", "-"]  # tmin
    assert texts[12:16] == ["-"] * 4  # pluie : variable absente
    # vent : pas de données horaires pour les 2 derniers jours
    assert texts[16:] == ["10.0 km/h", "10.0 km/h", "-", "-"]
    # 1 axe du tableau + 4 icônes + 0 goutte (pluie absente) + 2 flèches de vent
    assert len(fig.axes) == 7
