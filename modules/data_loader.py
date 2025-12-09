import pandas as pd
import requests

def download_csv(url: str, out_path: str) -> None:
    content = requests.get(url, timeout=30).content
    open(out_path,"wb").write(content)

def load_csv(path: str, skip: int = 3) -> pd.DataFrame:
    return pd.read_csv(path, skiprows=skip)