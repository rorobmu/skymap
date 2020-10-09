import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import process_catalog
import constellation
import tools
"""
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.coordinates import get_body_barycentric, get_body, get_moon
t = Time("2020-10-09 15:39", scale="utc")
loc = EarthLocation.from_geodetic(lat=45.73, lon=4.9181) 
solar_system_ephemeris.set('de432s')
mars = get_body('mars', t, loc) 
   """ 

#TODO
#test ephemride (ex:mars, messier)

# Variables to set up how to draw
constellations_to_draw = 'And|Aqr|Aql|Ari|Aur|Boo|Cam|CnC|Cvn|CMa|CMi|Cap|Cas|Cep|Cet|Com|CrB|Crv|Crt|Cyg|Del|Dra|Gem|Her|Hya|Lac|Leo|LMi|Lep|Lib|Lyn|Lyr|Mon|Oph|Ori|Peg|Per|Psc|Pup|Sge|Sgr|Sco|Sct|Ser|Tau|Tri|UMa|UMi|Vir|Vul'
processCatalog = False
ra_min = 0
ra_max= 24
dec_min = -40
dec_max= 90

central_longitude_ra=11
central_latitude_dec=90
noBound = False
drawBoundLimit = False
showCoord = True

ra_down_left=13.5
dec_down_left=-15
ra_up_right=7
dec_up_right=60


if(processCatalog):
    process_catalog.process_star_catalog(constellations_to_draw)

# get stars in df, and reduced stars to draw visible stars
df_star_full = pd.read_csv('stars.csv', sep=';')
df_star = process_catalog.get_df_visible_stars(df_star_full)

#init
ax = tools.initFigure(central_longitude=central_longitude_ra, central_latitude=central_latitude_dec,ra_min=ra_min, ra_max=ra_max, dec_min=dec_min, dec_max=dec_max, showC=showCoord)
tools.initBound(ax=ax, ra_up_right=ra_up_right, dec_up_right=dec_up_right, ra_down_left=ra_down_left, dec_down_left=dec_down_left, isNoBound=noBound, drawBoundLimit=drawBoundLimit)

#draw figures
constellation.draw_constellation(df_star_full,constellations_to_draw)
tools.drawStars(ax,df_star)
tools.drawRADecLines(ax)

tools.cropAndRevserseImage(ax)

plt.show()
#plt.savefig('test.png', format='png', dpi=150)

