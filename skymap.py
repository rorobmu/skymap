import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import process_catalog
import constellation

#TODO
#tester avec toutes les constellations hemisphere nord
#nettoyer code ajout comment + variables plus claires
#créer fonction "isinbound" pour savoir si on dessine l'objet ou voir si utilisation xlim/ylim
#réécrire coordonnées dans image à taille limité
#test ephemride (ex:mars)

constellations = 'UMa|Boo|UMi|And|Oph|Cas|Peg|Cet|Ori|Aqr|Tri|Per'
process_catalog.process_star_catalog(constellations)
df_uma = pd.read_csv('stars.csv', sep=';')

min_ra = 0
max_ra = 24
min_dec = -40
max_dec = 90

#draw figures
figsize = (40, 20)
background_color = '#00365A'

fig = plt.figure(figsize=figsize)
ax = plt.axes(projection=ccrs.AzimuthalEquidistant(
    central_longitude=((min_ra+max_ra)/2)*360/24.0, central_latitude=90))
ax.background_patch.set_facecolor(background_color)


constellation.draw_constellation(df_uma,constellations)

corner_lim_up_left_x, corner_lim_up_left_y =  ax.projection.transform_point(5*360/24, -10,src_crs=ccrs.Geodetic())
ax.scatter(corner_lim_up_left_x,corner_lim_up_left_y,
            color='green', lw=10, alpha=1, clip_on=True)


corner_lim_down_right_x, corner_lim_down_right_y = ax.projection.transform_point(15*360/24, -20,src_crs=ccrs.Geodetic())
ax.scatter(corner_lim_down_right_x,corner_lim_down_right_y,
            color='red', lw=10, alpha=1, clip_on=True)

for index, row in df_uma.iterrows():
    star_x, star_y = ax.projection.transform_point(row['ra']*360/24, row['dec'],src_crs=ccrs.Geodetic())
    #if(star_x>corner_lim_up_left_x and star_x<corner_lim_down_right_x 
     #      and star_y<corner_lim_up_left_y and star_y>corner_lim_down_right_y):
    ax.scatter(star_x,star_y,s=(4.5-row['mag'])*7, color='white', lw=0, edgecolor='none', zorder=10)    
    #ax.text(row['RA']*360/24, row['Dec'],row['Name'], ha='left', va='center', 
    #            transform=ccrs.Geodetic(), fontsize=10,color='white')
#ax.set_xlim(ax.get_xlim()[::-1])
#ax.set_ylim(ax.get_ylim()[::-1])


ra_large = np.arange(min_ra*360/24.0, (max_ra*360/24.0)+1, 1*360/24)
ra_delim = np.arange(min_ra*360/24, max_ra*360/24.00, 0.1)

dec_large = np.arange(min_dec, max_dec + 1, 10)
dec_delim = np.arange(min_dec, max_dec + 0.01, 0.1)

#ax.text(11*360/24, 20,         'test1', ha='left', va='center',transform=ccrs.Geodetic(), fontsize=10,color='white')
#ax.text(14*360/24, 30, 'test2', ha='left', va='center',transform=ccrs.Geodetic(), fontsize=10,color='white')

# boucle pour dessiner la grille "à la main"
for dec in dec_large: 
    #utiliser delim2 pour tronquer
    ra_delim2 = []
    for delim in ra_delim : 
        at_x, at_y = ax.projection.transform_point(delim, dec,src_crs=ccrs.Geodetic())
        if(at_x>corner_lim_up_left_x and at_x<corner_lim_down_right_x 
           and at_y<corner_lim_up_left_y and at_y>corner_lim_down_right_y):
            ra_delim2.append(delim)
    
    ax.plot(ra_delim, [dec]*len(ra_delim), transform=ccrs.Geodetic(), 
            color='cyan', lw=1, alpha=.1, clip_on=True)
    ax.text((max_ra*360/24)+.2, dec,str(dec) + '°', ha='right', va='center',transform=ccrs.Geodetic(), fontsize=15,color='white')
    
for ra in ra_large:   
    #utiliser delim2 pour tronquer
    dec_delim2 = []
    for delim in dec_delim : 
        at_x, at_y = ax.projection.transform_point(ra, delim,src_crs=ccrs.Geodetic())
        if(at_x>corner_lim_up_left_x and at_x<corner_lim_down_right_x 
           and at_y<corner_lim_up_left_y and at_y>corner_lim_down_right_y):
            dec_delim2.append(delim)
            
    ax.plot([ra]*len(dec_delim), dec_delim, transform=ccrs.Geodetic(), 
            color='cyan', lw=1, alpha=.1, clip_on=True)
    ax.text(ra, min_dec-1,str(int(ra/360*24)) + 'h', ha='center', va='top',transform=ccrs.Geodetic(), fontsize=15,color='white')
    
#point1 = [13.79*360/24.0,49.31]
#point2 = [13.39*360/24.0,54.9]
#x_values = [point1[0], point2[0]]
#y_values = [point1[1], point2[1]]
#plt.plot(x_values, y_values, transform=ccrs.Geodetic(), 
#            color='red', lw=3, alpha=1, clip_on=True)




#dessine la grille automatiquement
#ax.gridlines(color='red', ylocs=np.arange(20, 81, 10), xlocs=np.arange(7*360/24.0, 15*360/24.0, 1*360/24))#, draw_labels=True)  
#ax.tissot(facecolor='green', alpha=.8, lats=np.arange(20, 81, 10), lons=np.arange(7*360/24.0, 15*360/24.0, 1*360/24))    


ax.set_xlim(ax.get_xlim()[::-1])
ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[1])
#ax.set_xlim(corner_lim_down_right_x, corner_lim_up_left_x)
#ax.set_ylim(corner_lim_down_right_y, corner_lim_up_left_y)


plt.show()
#plt.savefig('test.png', format='png', dpi=150)

