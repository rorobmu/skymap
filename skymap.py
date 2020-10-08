import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import process_catalog
import constellation
import tools

#TODO
#nettoyer code ajout comment + variables plus claires
#créer fonction "isinbound" pour savoir si on dessine l'objet ou voir si utilisation xlim/ylim
#réécrire coordonnées dans image à taille limité
#test ephemride (ex:mars)

constellations_to_draw = 'And|Aqr|Aql|Ari|Aur|Boo|Cam|CnC|Cvn|CMa|CMi|Cap|Cas|Cep|Cet|Com|CrB|Crv|Crt|Cyg|Del|Dra|Gem|Her|Hya|Lac|Leo|LMi|Lep|Lib|Lyn|Lyr|Mon|Oph|Ori|Peg|Per|Psc|Pup|Sge|Sgr|Sco|Sct|Ser|Tau|Tri|UMa|UMi|Vir|Vul'


#process_catalog.process_star_catalog(constellations)

df_star_full = pd.read_csv('stars.csv', sep=';')
df_star = process_catalog.get_df_visible_stars(df_star_full)

min_ra = 0
max_ra = 24
min_dec = -40
max_dec = 90

ax = tools.initFigure(ra_min=0, ra_max=24, central_latitude=90)
constellation.draw_constellation(df_star_full,constellations_to_draw)
tools.initBound(ax=ax, ra_up_left=5, dec_up_left=-10, ra_down_right=15, dec_down_right=-20, isNoBound=False)

#draw stars
for index, row in df_star.iterrows():
    star_x, star_y = ax.projection.transform_point(row['ra']*360/24, row['dec'],src_crs=ccrs.Geodetic())
    if(tools.isInBound( star_x, star_y)):
        ax.scatter(star_x,star_y,s=(4.5-row['mag'])*7, color='white', lw=0, edgecolor='none', zorder=10)    
    #ax.text(row['RA']*360/24, row['Dec'],row['Name'], ha='left', va='center', 
    #            transform=ccrs.Geodetic(), fontsize=10,color='white')


ra_large = np.arange(min_ra*360/24.0, (max_ra*360/24.0)+1, 1*360/24)
ra_delim = np.arange(min_ra*360/24, max_ra*360/24.00, 0.1)

dec_large = np.arange(min_dec, max_dec + 1, 10)
dec_delim = np.arange(min_dec, max_dec + 0.01, 0.1)


# boucle pour dessiner la grille "à la main"
for dec in dec_large: 
    #utiliser delim2 pour tronquer
    ra_delim2 = []
    for delim in ra_delim : 
        at_x, at_y = ax.projection.transform_point(delim, dec,src_crs=ccrs.Geodetic())
        if(tools.isInBound(at_x, at_y)):
            ra_delim2.append(delim)
    
    ax.plot(ra_delim2, [dec]*len(ra_delim2), transform=ccrs.Geodetic(), 
            color='cyan', lw=1, alpha=.1, clip_on=True)
    #ax.text((max_ra*360/24)+.2, dec,str(dec) + '°', ha='right', va='center',transform=ccrs.Geodetic(), fontsize=15,color='white')
    
for ra in ra_large:   
    #utiliser delim2 pour tronquer
    dec_delim2 = []
    for delim in dec_delim : 
        at_x, at_y = ax.projection.transform_point(ra, delim,src_crs=ccrs.Geodetic())
        if(tools.isInBound(at_x, at_y)):
            dec_delim2.append(delim)
            
    ax.plot([ra]*len(dec_delim2), dec_delim2, transform=ccrs.Geodetic(), 
            color='cyan', lw=1, alpha=.1, clip_on=True)
    #ax.text(ra, min_dec-1,str(int(ra/360*24)) + 'h', ha='center', va='top',transform=ccrs.Geodetic(), fontsize=15,color='white')
    
#dessine la grille automatiquement
#ax.gridlines(color='red', ylocs=np.arange(20, 81, 10), xlocs=np.arange(7*360/24.0, 15*360/24.0, 1*360/24))#, draw_labels=True)  
#ax.tissot(facecolor='green', alpha=.8, lats=np.arange(20, 81, 10), lons=np.arange(7*360/24.0, 15*360/24.0, 1*360/24))    


tools.cropAndRevserseImage(ax)


plt.show()
#plt.savefig('test.png', format='png', dpi=150)

