import os
import pooch
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import urllib
import json


df_ic = pd.read_json("ic.json", orient = 'index')
df_ic = df_ic.drop(['night'], axis=1)
df_ic.to_json(r'~/mameteo/test/icone.json')
with open('icone.json','r') as f:
    d = json.loads(f.read(),)
df_icone = pd.json_normalize(d )
pd.json_normalize