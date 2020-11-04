import pandas as pd
import matplotlib.pyplot as plt
import process_catalog
import asterism
import tools

# -------Variables to adjust before generation-------------

#global information on map for nothern hemisphere
constellations_to_draw = 'And|Aqr|Aql|Ari|Aur|Boo|Cam|CnC|Cvn|CMa|CMi|Cap|Cas|Cep|Cet|Com|CrB|Crv|Crt|Cyg|Del|Dra|Gem|Her|Hya|Lac|Leo|LMi|Lep|Lib|Lyn|Lyr|Mon|Oph|Ori|Peg|Per|Psc|Pup|Sge|Sgr|Sco|Sct|Ser|Tau|Tri|UMa|UMi|Vir|Vul'
ra_min = 0
ra_max= 24
dec_min = -40
dec_max= 90

#central point of view and egde of field view
noBound = False #if there is no bound, ignore other paramters for view below
central_ra=12
central_dec=40
fieldViewWidth=50
fieldViewHeight=45

#other global parameters
drawBoundLimit = False
showCoord = True
processCatalog = False
mapTitle=''
fileName = 'map'
maxMagnitude = 6
# ---------------------------------------------------


if(processCatalog):
    process_catalog.process_star_catalog(constellations_to_draw)

# get stars in df, and reduced stars to draw visible stars
df_star_full = pd.read_csv('stars.csv', sep=';')
df_star = process_catalog.get_df_visible_stars(df_star_full, maxMagnitude)

#init map
ax = tools.initFigure(central_longitude=central_ra, central_latitude=90,ra_min=ra_min, ra_max=ra_max, dec_min=dec_min, dec_max=dec_max, showC=showCoord, title=mapTitle, maxMagnitude=maxMagnitude)
tools.computeFigureDeg(ax, central_ra)
tools.computeEdges(ax,fieldViewWidth=fieldViewWidth,fieldViewHeigth=fieldViewHeight, central_ra=central_ra, central_dec=central_dec)
tools.initBound(ax=ax, isNoBound=noBound, drawBoundLimit=drawBoundLimit)



#draw figures - constellations, stars, ra and dec lines
asterism.draw_constellation(df_star_full,constellations_to_draw)
tools.drawStars(ax,df_star)
tools.drawRADecLines(ax, central_ra)

#draw figures specific - uncomment examples

#Examples for ephemerides
#tools.drawEphemerides(obj_id='1003699', obj_type='designation', color='#E2F566', start='2020-11-02', stop='2020-11-25', step='1d', showDate=True, dateDisplayFreq=5,textPadding=[1.5,0],ax=ax)
#tools.drawEphemerides(obj_id='499', obj_type='majorbody', color='#F26A46', start='2020-07-01', stop='2021-02-01', step='7d', showDate=True, dateDisplayFreq=5, textPadding=[0,-1] ,ax=ax)


#Exemples for deep sky objects
#tools.drawDeepSkyObject(ax,'M63', 'galaxie')
#tools.drawDeepSkyObject(ax,'M53', 'amas globulaire')
#tools.drawDeepSkyObject(ax,'M97', 'nébuleuse')
#ra, dec = tools.getCoordDeepSkyObject('M97')
#tools.drawTelrad(ax, ra=ra, dec=dec)
#tools.drawLegend(ax)

#others exemples
#asterism.draw_asterism(df_star_full,[113852,113993,114186,114365,114104,113790,113498,113316,112998])
#tools.drawPOIRect(ax,11,10,15,10)

#finalize figure and save it
tools.cropAndRevserseImage(ax)
plt.savefig(fileName + '.png', format='png', dpi=300, pad_inches=0)
plt.show()

    