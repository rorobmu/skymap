import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import process_catalog
import constellation
import tools



#TODO
#test ephemride (ex:mars, messier)

# Variables to set up how to draw
constellations_to_draw = 'And|Aqr|Aql|Ari|Aur|Boo|Cam|CnC|Cvn|CMa|CMi|Cap|Cas|Cep|Cet|Com|CrB|Crv|Crt|Cyg|Del|Dra|Gem|Her|Hya|Lac|Leo|LMi|Lep|Lib|Lyn|Lyr|Mon|Oph|Ori|Peg|Per|Psc|Pup|Sge|Sgr|Sco|Sct|Ser|Tau|Tri|UMa|UMi|Vir|Vul'
processCatalog = False
ra_min = 0
ra_max= 24
dec_min = -40
dec_max= 90

central_longitude_ra=1
central_latitude_dec=90
noBound = True
drawBoundLimit = False
showCoord = True

ra_down_left=2.5
dec_down_left=-10
ra_up_right=23.5
dec_up_right=20


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



#tools.drawEphemerides(ax=ax, obj_id='499', start='2020-07-01', stop='2021-02-01', step='7d', color='#F26A46')


"""
tools.drawDeepSkyObject(ax,'M65')
tools.drawDeepSkyObject(ax,'M66')
tools.drawDeepSkyObject(ax,'M63')
tools.drawDeepSkyObject(ax,'M51')
tools.drawDeepSkyObject(ax,'M94')
tools.drawDeepSkyObject(ax,'M64')
tools.drawDeepSkyObject(ax,'M53')
tools.drawDeepSkyObject(ax,'M59')
tools.drawDeepSkyObject(ax,'M60')
tools.drawDeepSkyObject(ax,'M95')
tools.drawDeepSkyObject(ax,'M91')
tools.drawDeepSkyObject(ax,'M105')
tools.drawDeepSkyObject(ax,'M81')
tools.drawDeepSkyObject(ax,'M82')
tools.drawDeepSkyObject(ax,'M108')
tools.drawDeepSkyObject(ax,'M109')
"""
tools.cropAndRevserseImage(ax)


plt.savefig('mars_retrogradation2.png', format='png', dpi=300, pad_inches=0)
plt.show()




    