import datetime
import requests
import pandas as pd
import matplotlib.pylab as plt

# Obtenir la date d'aujourd'hui
aujourd_hui = datetime.date.today()

# Date cinq jours plus tard
J_plus_4 = aujourd_hui + datetime.timedelta(days=4)

#mon url pour obtenir le jeu de données
url_db = "https://api.open-meteo.com/v1/meteofrance?latitude=43.6109&longitude=3.8763&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max&timezone=GMT&start_date=2023-10-24&end_date=2023-10-28&format=csv"

#telecharger jeu de données
db = requests.get(url_db)

#on enregistre et écrase le précédent fichier
open("./test/db.csv", "wb").write(db.content)

#transformation db en dataframe
df = pd.read_csv("./test/db.csv")
df.head()

##suppression colonnes inutiles
#df = df.drop(['timezone', 'timezone_abbreviation'], axis=1)
#df = df.drop([0],axis=0)
#
##modification nom colonne et suppression ligne index 1
#df.columns = ["time","temperature_2m","precipitation","wind_speed_10m"]
#df = df.drop(1)
#df = df.reset_index(drop=True)













# %%
