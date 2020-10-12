import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
from astroquery.jplhorizons import Horizons
import datetime
from astropy.coordinates import SkyCoord

def initFigure(central_longitude, central_latitude, ra_min, ra_max, dec_min, dec_max,showC):
    # init ra/dec
    global min_ra
    global max_ra
    global min_dec
    global max_dec
    global ra_step
    global ra_line
    global dec_step
    global dec_line
    global showCoord
    
    showCoord=showC
    
    min_ra = ra_min
    max_ra = ra_max
    min_dec = dec_min
    max_dec = dec_max
    
    ra_step = np.arange(min_ra*360/24.0, (max_ra*360/24.0)+1, 1*360/24)
    ra_line = np.arange(min_ra*360/24, max_ra*360/24.00, 0.1)
    dec_step = np.arange(min_dec, max_dec + 1, 10)
    dec_line = np.arange(min_dec, max_dec + 0.01, 0.1)
    
    #draw figures
    figsize = (30, 15)
    background_color = '#00365A'    
    fig = plt.figure(figsize=figsize)
    fig.patch.set_facecolor('#00365A')       
    ax = plt.axes(projection=ccrs.AzimuthalEquidistant(
        central_longitude=central_longitude*360/24.0, central_latitude=central_latitude))
    ax.background_patch.set_facecolor(background_color)
    ax.patch.set_edgecolor(background_color)
    ax.outline_patch.set_edgecolor('white')
    plt.title('Carte du ciel - hémisphère nord', fontsize=25, fontweight='medium', color='white', va='top')
    


    return ax

def initBound(ax, ra_up_right, dec_up_right, ra_down_left, dec_down_left, isNoBound,drawBoundLimit):
    global corner_lim_up_right_x
    global corner_lim_up_right_y
    global corner_lim_down_left_x
    global corner_lim_down_left_y
    global noBound
    
    noBound=isNoBound
    debug = False
    
    corner_lim_up_right_x, corner_lim_up_right_y =  ax.projection.transform_point(ra_up_right*360/24, dec_up_right,src_crs=ccrs.Geodetic())
    corner_lim_down_left_x,  corner_lim_down_left_y = ax.projection.transform_point(ra_down_left*360/24, dec_down_left,src_crs=ccrs.Geodetic())
    
    #debug : scatter limit point 
    if(debug):
        ax.scatter(corner_lim_up_right_x,corner_lim_up_right_y, color='green', lw=10, alpha=1, clip_on=True)
        ax.scatter(corner_lim_down_left_x,corner_lim_down_left_y, color='red', lw=10, alpha=1, clip_on=True)
    if(drawBoundLimit):
        #draw square for bound
        x_values  = [corner_lim_down_left_x, corner_lim_down_left_x]
        y_values  = [corner_lim_down_left_y, corner_lim_up_right_y]
        ax.plot(x_values, y_values,color='red', lw=2, alpha=1, clip_on=True )
        
        x_values  = [corner_lim_up_right_x, corner_lim_up_right_x]
        y_values  = [corner_lim_down_left_y, corner_lim_up_right_y]
        ax.plot(x_values, y_values,color='red', lw=2, alpha=1, clip_on=True )
        
        x_values  = [corner_lim_down_left_x, corner_lim_up_right_x]
        y_values  = [corner_lim_down_left_y, corner_lim_down_left_y]
        ax.plot(x_values, y_values,color='red', lw=2, alpha=1, clip_on=True )
        
        x_values  = [corner_lim_down_left_x, corner_lim_up_right_x]
        y_values  = [corner_lim_up_right_y, corner_lim_up_right_y]
        ax.plot(x_values, y_values,color='red', lw=2, alpha=1, clip_on=True )


def isInBound(x, y):
    if(noBound):
        return True
    #the figure is not reversed on x yet, so we must invert the test for x
    if(x>corner_lim_up_right_x and x<corner_lim_down_left_x 
           and y<corner_lim_up_right_y and y>corner_lim_down_left_y):
        return True
    return False



def cropAndRevserseImage(ax):
    if(noBound):
        ax.set_xlim(ax.get_xlim()[::-1])
        ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[1])
    else:
        ax.set_xlim(corner_lim_down_left_x, corner_lim_up_right_x)
        ax.set_ylim(corner_lim_down_left_y, corner_lim_up_right_y)
    
        
        
def drawRADecLines(ax):
    # draw declinaison lines
    for dec in dec_step: 
        ra_delim = []
        ra_text = ra_line[0]
        for delim in ra_line : 
            at_x, at_y = ax.projection.transform_point(delim, dec,src_crs=ccrs.Geodetic())
            if(isInBound(at_x, at_y)):
                ra_delim.append(delim)
                
                if(delim > ra_text and delim - ra_text < 1):
                    ra_text = delim
        
        
        #if(len(ra_delim)>0):
        ax.plot(ra_line, [dec]*len(ra_line), transform=ccrs.Geodetic(),color='cyan', lw=1, alpha=.2, clip_on=True)

        if(showCoord):
            if(noBound==False and len(ra_delim)>0):
                ra_text=max(ra_delim)
                text_x, text_y = ax.projection.transform_point(ra_text+0.1, dec,src_crs=ccrs.Geodetic())
                if(text_y < corner_lim_up_right_y):
                    ax.text(corner_lim_down_left_x - 10000, text_y,str(dec) + '°', ha='left', va='center', fontsize=30,color='white')
            elif(noBound==True):
                text_x, text_y = ax.projection.transform_point(5*360/24.0, dec,src_crs=ccrs.Geodetic())
                ax.text(text_x, text_y,str(dec) + '°', ha='left', va='center', fontsize=15,color='white')
                
    # draw ra lines    
    for ra in ra_step:   
        dec_delim = []
        for delim in dec_line : 
            at_x, at_y = ax.projection.transform_point(ra, delim,src_crs=ccrs.Geodetic())
            if(isInBound(at_x, at_y)):
                dec_delim.append(delim)
                
        ax.plot([ra]*len(dec_delim), dec_delim, transform=ccrs.Geodetic(), 
                color='cyan', lw=1, alpha=.2, clip_on=True)
        
        if(showCoord):
            if(noBound==False and len(dec_delim)>0):
                text_x, text_y = ax.projection.transform_point(ra, min(dec_delim)-0.1,src_crs=ccrs.Geodetic())
                if(text_x < corner_lim_down_left_x and text_x > corner_lim_up_right_x and int(ra/360*24)<24):
                    ax.text(text_x, corner_lim_down_left_y,str(int(ra/360*24)) + 'h', ha='center', va='bottom', fontsize=30,color='white')
            elif(noBound==True and int(ra/360*24)<24):
                text_x, text_y = ax.projection.transform_point(ra, min_dec-1,src_crs=ccrs.Geodetic())
                ax.text(text_x, text_y,str(int(ra/360*24)) + 'h', ha='center', va='center', fontsize=15,color='white')
        
    #dessine la grille automatiquement
    #ax.gridlines(color='red', ylocs=np.arange(-50, 91, 10), xlocs=np.arange(0*360/24.0, 24*360/24.0, 1*360/24), draw_labels=True)  
    #ax.tissot(facecolor='green', alpha=.8, lats=np.arange(-40, 81, 10), lons=np.arange(0*360/24.0, 24*360/24.0, 1*360/24))    

def drawStars(ax, df_star):
    #draw stars
    for index, row in df_star.iterrows():
        star_x, star_y = ax.projection.transform_point(row['ra']*360/24, row['dec'],src_crs=ccrs.Geodetic())
        if(isInBound( star_x, star_y)):
            ax.scatter(star_x,star_y,s=(6.5-row['mag'])*5, color='white', lw=0, edgecolor='none', zorder=10)    
        #ax.text(row['RA']*360/24, row['Dec'],row['Name'], ha='left', va='center', 
        #            transform=ccrs.Geodetic(), fontsize=10,color='white')


def drawEphemerides(ax, obj_id, start, stop, step, color):
    #Bron
    loc = {'lon': 4.920591,
       'lat': 45.732450,
       'elevation': 0.2}

    obj = Horizons(id=obj_id, id_type='majorbody',location=loc, epochs={'start':start, 'stop':stop,'step':step})
    eph = obj.ephemerides()
    
    for i in range(0,len(eph)):
        x, y = ax.projection.transform_point(eph[i]['RA'], eph[i]['DEC'],src_crs=ccrs.Geodetic())
        ax.scatter(x,y,s=110, color=color, lw=0, edgecolor='none', zorder=15)
        if(i%5 == 0 or i == 0):
            formatted_date = datetime.datetime.strptime(eph[i]['datetime_str'], '%Y-%b-%d %H:%M').strftime('%d/%m')
            ax.text(x,y-40000,formatted_date, ha='center', va='top', fontsize=20,color='white',zorder=16)
            
def drawDeepSkyObject(ax, obj_name):

    target = SkyCoord.from_name(obj_name)  
    x, y = ax.projection.transform_point(target.ra.deg, target.dec.deg,src_crs=ccrs.Geodetic())
    ax.text(x,y,obj_name, ha='center', va='center', fontsize=10,color='white',zorder=16, fontweight='bold')
    circle = plt.Circle((x, y), 150000, fill=False, color='white', linewidth=1, zorder=20)
    ax.add_artist(circle)
