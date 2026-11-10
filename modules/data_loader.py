import time

import pandas as pd
import requests


def download_csv(url: str, out_path: str, retries: int = 3) -> None:
    """Télécharge un CSV ; échoue explicitement si l'API renvoie une erreur."""
    last_error = None
    for attempt in range(retries):
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            if resp.content.lstrip().startswith(b"{"):  # erreur JSON de l'API
                raise ValueError(f"Réponse JSON inattendue : {resp.text[:200]}")
            with open(out_path, "wb") as f:
                f.write(resp.content)
            return
        except (requests.RequestException, ValueError) as e:
            last_error = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Téléchargement impossible : {url}") from last_error


def load_csv(path: str, skip: int = 3) -> pd.DataFrame:
    return pd.read_csv(path, skiprows=skip)
