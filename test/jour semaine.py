import datetime


# Obtenez la date actuelle
aujourdhui = datetime.datetime.now()



# Obtenez le nom du jour de la semaine, le jour du mois et le nom du mois
jour_semaine = noms_jours[aujourdhui.weekday()]
jour_mois = aujourdhui.day
mois = noms_mois[aujourdhui.month]

# Créez la chaîne de date au format souhaité
date_formattee = f"{jour_semaine} {jour_mois} {mois}"

# Affichez la date formatée
print(date_formattee)