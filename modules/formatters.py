import pandas as pd

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {
        "weathercode (wmo code)": "code",
        "temperature_2m_max (°C)": "tmax",
        "temperature_2m_min (°C)": "tmin",
        "precipitation_sum (mm)": "pluie",
        "windspeed_10m_max (km/h)": "vent",
        "winddirection_10m_dominant (°)" : "direction"
    }
    return df.rename(columns=mapping,inplace=True)

def add_units(df: pd.DataFrame) -> pd.DataFrame:
    units = {"tmax":"°C","tmin":"°C","pluie":"mm","vent":"km/h"}
    for col,unit in units.items():
        df[col] = df[col].astype(str)+f" {unit}"
    return df

def format_dates(df: pd.DataFrame) -> pd.DataFrame:
    jours=["lun","mar","mer","jeu","ven","sam","dim"]
    mois=["janv","fév","mars","avr","mai","juin","juil","août",
          "sept","oct","nov","déc"]

    for i in range(df.shape[1]):
        d = pd.to_datetime(df.iloc[0,i])
        df.iloc[0,i] = f"{jours[d.weekday()]}\n{d.day}\n{mois[d.month-1]}"
    return df