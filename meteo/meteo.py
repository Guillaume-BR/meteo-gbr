import datetime
import os
import pooch
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import urllib

#Date d'aujourd'hui
aujourd_hui = datetime.date.today()

# Date cinq jours plus tard
J_plus_4 = aujourd_hui + datetime.timedelta(days=4)

# télécharger le jeu de données

url_db = "https://api.open-meteo.com/v1/meteofrance?latitude=43.6109&longitude=3.8763&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max&timezone=GMT&start_date={0}&end_date={1}&format=csv".format(aujourd_hui,J_plus_4)

path_target = "./data/db.csv"
path, fname = os.path.split(path_target)
pooch.retrieve(url_db, path=path, fname=fname, known_hash=None) 

# transformation db en dataframe
df = pd.read_csv(path_target, skiprows=3, index_col=None,)

df.rename(columns={"weathercode (wmo code)" : "code" , "temperature_2m_max (°C)":"tmax" , "temperature_2m_min (°C)":"tmin" , "precipitation_sum (mm)" : "pluie" , "windspeed_10m_max (km/h)" : "vent"}, inplace = True)

df['tmax'] = df['tmax'].astype(str) + ' °C'
df['tmin'] = df['tmin'].astype(str) + ' °C'
df['pluie'] = df['pluie'].astype(str) + ' mm'
df['vent'] = df['vent'].astype(str) + ' km/h'

# Créez une liste de noms de jours de la semaine et de noms de mois
noms_jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
noms_mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


#Création du tableau contenant les informations voulues
fig = plt.figure(figsize=(10,10), dpi=300)
ax = plt.subplot()

ncols = 5
nrows = df.shape[1]

ax.set_xlim(0, ncols + 1)
ax.set_ylim(0, nrows)
ax.set_axis_off()

positions = [1.5, 2.5, 3.5, 4.5, 5.5]

columns = df['time'].tolist()

# Add table's main text
for i in range(1,nrows):
    for j, column in enumerate(columns):
        ha = 'center'
        ax.annotate(
            xy = (positions[j], nrows - i),
            text = df.iloc[j,i],
            ha = ha,
            va = 'center'
        )

# création des dates (nom du jour/numéro/mois)
dates = [] 
for i in range(5):
    jour = datetime.date.today() + datetime.timedelta(days=i)
    jour_semaine = noms_jours[jour.weekday()]
    numero_mois = jour.day
    mois = noms_mois[jour.month]
    jour = f"{jour_semaine}\n{numero_mois}\n{mois}"
    dates.append(jour)

#nom des colonnes
for index, c in enumerate(dates):
        ha = 'center'
        ax.annotate(
            xy=(positions[index], nrows-0.5),
            text=dates[index],
            ha=ha,
            va='bottom',
            weight='bold'
        )
#nom des lignes
lignes = []

plt.savefig(
    'meteo.svg',
    dpi=300,
    transparent=True
)
