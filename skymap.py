import pandas as pd
import matplotlib.pyplot as plt
import process_catalog
import constellation
import tools

#TODO
#grosseur des étoiles en fonction du champ + obj ciel profond + epaisseur constellations

# Variables to adjust before generation

#global information on map
constellations_to_draw = 'And|Aqr|Aql|Ari|Aur|Boo|Cam|CnC|Cvn|CMa|CMi|Cap|Cas|Cep|Cet|Com|CrB|Crv|Crt|Cyg|Del|Dra|Gem|Her|Hya|Lac|Leo|LMi|Lep|Lib|Lyn|Lyr|Mon|Oph|Ori|Peg|Per|Psc|Pup|Sge|Sgr|Sco|Sct|Ser|Tau|Tri|UMa|UMi|Vir|Vul'
ra_min = 0
ra_max= 24
dec_min = -40
dec_max= 90

#central point of view and egde of field view
noBound = False #if there is no bound, ignore other paramters for view below
central_ra=11
central_dec=13
fieldViewWidth=45
fieldViewHeigth=30


#other global parameters
drawBoundLimit = False
showCoord = True
processCatalog = False
mapTitle=''
maxMagnitude = 4.5



if(processCatalog):
    process_catalog.process_star_catalog(constellations_to_draw)

# get stars in df, and reduced stars to draw visible stars
df_star_full = pd.read_csv('stars.csv', sep=';')
df_star = process_catalog.get_df_visible_stars(df_star_full, maxMagnitude)

#init map
ax = tools.initFigure(central_longitude=central_ra, central_latitude=90,ra_min=ra_min, ra_max=ra_max, dec_min=dec_min, dec_max=dec_max, showC=showCoord, title=mapTitle)
tools.computeFigureDeg(ax, central_ra)
tools.computeEdges(ax,fieldViewWidth=fieldViewWidth,fieldViewHeigth=fieldViewHeigth, central_ra=central_ra, central_dec=central_dec)
tools.initBound(ax=ax, isNoBound=noBound, drawBoundLimit=drawBoundLimit)



#draw figures
constellation.draw_constellation(df_star_full,constellations_to_draw)
tools.drawStars(ax,df_star)
tools.drawRADecLines(ax, central_ra)
ra, dec = tools.getCoordDeepSkyObject('M65')
tools.drawTelrad(ax, ra=ra, dec=dec)
tools.drawDeepSkyObject(ax,'M65', 'galaxie')
tools.drawLegend(ax)
tools.drawPOIRect(ax,11,10,15,10)
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




    