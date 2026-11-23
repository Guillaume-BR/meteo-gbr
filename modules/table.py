import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from PIL import Image

from modules.formatters import add_units, format_dates, normalize_daily, rename_columns
from modules.icons import image_code


def build_table(
    df_day: pd.DataFrame, df_hour: pd.DataFrame, dates_attendues: list
) -> Figure:
    """Construit la figure du tableau météo à partir des CSV Open-Meteo lus bruts."""
    df_hour = df_hour.rename(columns={"windspeed_10m (km/h)": "vent"})

    # une ligne par jour attendu, colonnes toujours présentes, NaN -> "-"
    df_day = normalize_daily(rename_columns(df_day), dates_attendues)

    # valeur de la pluie pour l'affichage des gouttes
    pluie = df_day["pluie"].tolist()

    # ajout des unités puis transposition
    df_day = add_units(df_day).T

    # calcul du vent moyen et remplacement de la valeur dans df_day
    for i in range(len(dates_attendues)):
        subset = df_hour.loc[24 * i : 24 * (i + 1) - 1]
        value = round(subset["vent"].mean(), 1)
        df_day.iloc[5, i] = "-" if pd.isna(value) else str(value) + " km/h"

    # création du tableau contenant les informations voulues
    fig = plt.figure(figsize=(14, 10), dpi=60)
    ax = plt.subplot()

    ncols = df_day.shape[1]
    nrows = df_day.shape[0] - 1

    ax.set_xlim(0, ncols + 1)
    ax.set_ylim(0, nrows)
    ax.set_axis_off()

    columns = df_day.iloc[0].tolist()

    # création des dates (nom du jour/numéro/mois)
    df_day = format_dates(df_day)

    # nom des colonnes
    for i in range(ncols):
        ax.annotate(
            xy=(i + 1, nrows - 0.7),
            text=df_day.iloc[0, i],
            ha="center",
            va="bottom",
            weight="bold",
            fontsize=15,
        )

    for j, column in enumerate(columns):
        ax.annotate(
            xy=(j + 1, nrows - 2),
            text=df_day.iloc[2, j],
            ha="center",
            va="center",
            weight="bold",
            fontsize=12,
            bbox=dict(boxstyle="round4", pad=0.8, fc="indianred"),
        )

    for j, column in enumerate(columns):
        ax.annotate(
            xy=(j + 1, nrows - 3),
            text=df_day.iloc[3, j],
            ha="center",
            va="center",
            weight="bold",
            fontsize=12,
            bbox=dict(boxstyle="round4", pad=0.8, fc="lightblue"),
        )

    # ajout du reste des valeurs dans le tableau
    for i in range(4, nrows):
        for j, column in enumerate(columns):
            ax.annotate(
                xy=(j + 1, nrows - i),
                text=df_day.iloc[i, j],
                ha="center",
                weight="bold",
                fontsize=12,
                va="center",
            )

    # création des lignes de séparations
    ax.plot([0.5, 4.5], [nrows, nrows], lw=6, color="black", marker="", zorder=4)
    ax.plot([0.5, 4.5], [0.5, 0.5], lw=6, color="black", marker="", zorder=4)
    for x in range(1, nrows - 1):
        ax.plot(
            [0.5, 4.5], [x + 0.5, x + 0.5], lw=1.15, color="gray", ls=":", zorder=3, marker=""
        )

    # transformation en différents types de coordonnées
    DC_to_FC = ax.transData.transform
    FC_to_NFC = fig.transFigure.inverted().transform

    # coordonnées des données -> coordonnées normalisées de la figure
    def DC_to_NFC(x):
        return FC_to_NFC(DC_to_FC(x))

    # ajout des images du temps
    ax_point_1 = DC_to_NFC([0.25, 0.25])
    ax_point_2 = DC_to_NFC([0.75, 0.75])
    ax_width = abs(ax_point_1[0] - ax_point_2[0]) * 2
    ax_height = abs(ax_point_1[1] - ax_point_2[1]) * 2

    for i in range(ncols):
        ax_coords = DC_to_NFC([i + 0.5, 4.4])
        ico_ax = fig.add_axes([ax_coords[0], ax_coords[1], ax_width, ax_height])
        image_code(df_day.iloc[1, i], ico_ax)

    # ajout des gouttes d'eau
    gt_point_1 = DC_to_NFC([0.25, 0.25])
    gt_point_2 = DC_to_NFC([0.5, 0.5])
    gt_width = abs(gt_point_1[0] - gt_point_2[0])
    gt_height = abs(gt_point_1[1] - gt_point_2[1])
    for i in range(ncols):
        ax_coords = DC_to_NFC([i + 0.55, 1.9])
        if isinstance(pluie[i], float) and pluie[i] >= 0:
            goutte_ax = fig.add_axes([ax_coords[0], ax_coords[1], gt_width, gt_height])
            image = Image.open("./data/goutte.png")
            goutte_ax.axis("off")
            goutte_ax.imshow(image)

    # ajout des directions du vent
    v_point_1 = DC_to_NFC([0.25, 0.25])
    v_point_2 = DC_to_NFC([0.4, 0.4])
    v_width = abs(v_point_1[0] - v_point_2[0])
    v_height = abs(v_point_1[1] - v_point_2[1])
    for i in range(ncols):
        if isinstance(df_day.iloc[6, i], float) and df_day.iloc[6, i] >= 0:
            ax_coords = DC_to_NFC([i + 0.55, 0.9])
            vent_ax = fig.add_axes([ax_coords[0], ax_coords[1], v_width, v_height])
            vent = Image.open("./data/vent.png")
            vent = vent.rotate(-df_day.iloc[6, i])
            vent_ax.axis("off")
            vent_ax.imshow(vent)

    return fig
