import json
import urllib.request
from PIL import Image


with open("./data/ic.json", "r") as f:
    df_ic = json.load(f)


# fonction pour insérer les images
def image_code(code, ax):
    try:
        code_int = int(float(code))
        url = df_ic[str(code_int)]["day"]["image"]
        image = Image.open(urllib.request.urlopen(url, timeout=30))
    except (ValueError, KeyError, OSError):
        # code manquant/inconnu ou icône injoignable : image par défaut
        image = Image.open("./data/default.png")
    ax.imshow(image)
    ax.axis("off")
    return ax
