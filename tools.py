import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
import numpy as np
from astroquery.jplhorizons import Horizons
import datetime
from astropy.coordinates import SkyCoord

def initFigure(central_longitude, central_latitude, ra_min, ra_max, dec_min, dec_max,showC, title, maxMagnitude):
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
    global background_color
    global deepSky_dict
    global maxMag
    
    maxMag=maxMagnitude
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
    if(title!=''):
        plt.title(title, fontsize=25, fontweight='medium', color='white', va='top')

    deepSky_dict = {
        "galaxie": ['$\u2585$',0],
        "amas globulaire":  ['$\u2042$',0],#u25A3
        "nébuleuse": ['$\u25B2$',0],
        }

    return ax

def initBound(ax, isNoBound,drawBoundLimit):
    global noBound
    
    noBound=isNoBound
    
    if(drawBoundLimit):
        #draw square for bound
        ax.plot([point_downleft[0], point_upleft[0]], [point_downleft[1], point_upleft[1]], color='red', lw=8, clip_on=True)
        ax.plot([point_upleft[0], point_upright[0]], [point_upleft[1], point_upright[1]], color='red', lw=8, clip_on=True)
        ax.plot([point_upright[0], point_downright[0]], [point_upright[1], point_downright[1]], color='red', lw=8, clip_on=True)
        ax.plot([point_downright[0], point_downleft[0]], [point_downright[1], point_downleft[1]], color='red', lw=8, clip_on=True)

def isInBound(x, y):
    if(noBound):
        return True
    #the figure is not reversed on x yet, so we must invert the test for x
    if(x>point_downleft[0] and x<point_upright[0] and y>point_downleft[1] and y<point_upright[1]):
        return True
    return False



def cropAndRevserseImage(ax):
    if(noBound):
        ax.set_xlim(ax.get_xlim()[::-1])
        ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[1])
    else:
        ax.set_xlim(point_upright[0],point_downleft[0])
        ax.set_ylim(point_downleft[1], point_upright[1])
    
        
        
def drawRADecLines(ax,central_ra):
    # draw declinaison lines
    for dec in dec_step: 
        ra_delim = []
        ra_delim_coord = []
        for delim in ra_line : 
            at_x, at_y = ax.projection.transform_point(delim, dec,src_crs=ccrs.Geodetic())
            if(isInBound(at_x, at_y)):
                ra_delim.append(delim)
                ra_delim_coord.append((at_x, at_y))
        
        ax.plot(ra_line, [dec]*len(ra_line), transform=ccrs.Geodetic(),color='cyan', lw=1, alpha=.2, clip_on=True)

        if(showCoord):
            if(noBound==False and len(ra_delim)>0):
                #text_x, text_y = ax.projection.transform_point(min(ra_delim)+0.1, dec,src_crs=ccrs.Geodetic())
                text_x, text_y = max(ra_delim_coord)
                if(text_y < point_upright[1] and text_y > point_downleft[1] and text_x > point_upright[0]- 20000):
                    ax.text(text_x, text_y,str(dec) + '°', ha='left', va='center', fontsize=30,color='white')
            elif(noBound==True):
                text_x, text_y = ax.projection.transform_point(central_ra*360/24.0, dec,src_crs=ccrs.Geodetic())
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
                if(text_x > point_downleft[0] and text_x < point_upright[0] and text_y < point_downleft[0] + 10000 and int(ra/360*24)<24):
                    ax.text(text_x, text_y,str(int(ra/360*24)) + 'h', ha='center', va='bottom', fontsize=30,color='white')
            elif(noBound==True and int(ra/360*24)<24):
                text_x, text_y = ax.projection.transform_point(ra, min_dec-1,src_crs=ccrs.Geodetic())
                ax.text(text_x, text_y,str(int(ra/360*24)) + 'h', ha='center', va='center', fontsize=15,color='white')
        
    #dessine la grille automatiquement
    #ax.gridlines(color='red', ylocs=np.arange(-50, 91, 10), xlocs=np.arange(0*360/24.0, 24*360/24.0, 1*360/24), draw_labels=True)  
    #ax.tissot(facecolor='green', alpha=.8, lats=np.arange(-40, 81, 10), lons=np.arange(0*360/24.0, 24*360/24.0, 1*360/24))    



def getCoordDeepSkyObject(obj_name):
    target = SkyCoord.from_name(obj_name)  
    return target.ra.deg, target.dec.deg

def computeFigureDeg(ax, central_longitude_ra):
    global figureDecPixel
    x, y = ax.projection.transform_point(central_longitude_ra*360/24, 90,src_crs=ccrs.Geodetic())
    x2, y2 = ax.projection.transform_point(central_longitude_ra*360/24, 89,src_crs=ccrs.Geodetic())

    figureDecPixel = y-y2
    
def computeEdges(ax, fieldViewWidth, fieldViewHeigth, central_ra, central_dec):
    #central point of view
    x, y = ax.projection.transform_point(central_ra*360/24, central_dec,src_crs=ccrs.Geodetic())
    
    global point_downleft
    global point_upleft
    global point_upright
    global point_downright
    
    point_downleft = [x-((fieldViewWidth/2.0)*figureDecPixel), y-((fieldViewHeigth/2.0)*figureDecPixel)]
    point_upleft = [x-((fieldViewWidth/2.0)*figureDecPixel), y+((fieldViewHeigth/2.0)*figureDecPixel)]
    point_upright = [x+((fieldViewWidth/2.0)*figureDecPixel), y+((fieldViewHeigth/2.0)*figureDecPixel)]
    point_downright = [x+((fieldViewWidth/2.0)*figureDecPixel), y-((fieldViewHeigth/2.0)*figureDecPixel)]
    
def drawStars(ax, df_star):
    #draw stars
    sizeFactor=8
    for index, row in df_star.iterrows():
        star_x, star_y = ax.projection.transform_point(row['ra']*360/24, row['dec'],src_crs=ccrs.Geodetic())
        if(isInBound( star_x, star_y)):
            ax.scatter(star_x,star_y,s=(maxMag-row['mag'])*sizeFactor, color='white', lw=0, edgecolor='none', zorder=10)    
            #ax.text(star_x,star_y, row['hip'], ha='left', va='center', fontsize=10,color='white')

def drawTelrad(ax, ra, dec):
    x, y = ax.projection.transform_point(ra, dec,src_crs=ccrs.Geodetic())
    circle = plt.Circle((x, y), 0.25*figureDecPixel, fill=False, color='red', linewidth=1, zorder=20)
    ax.add_artist(circle)
    circle = plt.Circle((x, y), 1*figureDecPixel, fill=False, color='red', linewidth=1, zorder=20)
    ax.add_artist(circle)
    circle = plt.Circle((x, y), 2*figureDecPixel, fill=False, color='red', linewidth=1, zorder=20)
    ax.add_artist(circle)
    
def drawPOIRect(ax, ra, dec, width, height):
    
    x, y = ax.projection.transform_point(ra*360/24, dec,src_crs=ccrs.Geodetic())
    
    point_downleft = [x-((width/2.0)*figureDecPixel), y-((height/2.0)*figureDecPixel)]
    point_upleft = [x-((width/2.0)*figureDecPixel), y+((height/2.0)*figureDecPixel)]
    point_upright = [x+((width/2.0)*figureDecPixel), y+((height/2.0)*figureDecPixel)]
    point_downright = [x+((width/2.0)*figureDecPixel), y-((height/2.0)*figureDecPixel)]
    
    ax.plot([point_downleft[0], point_upleft[0]], [point_downleft[1], point_upleft[1]], color='red', lw=2, clip_on=True)
    ax.plot([point_upleft[0], point_upright[0]], [point_upleft[1], point_upright[1]], color='red', lw=2, clip_on=True)
    ax.plot([point_upright[0], point_downright[0]], [point_upright[1], point_downright[1]], color='red', lw=2, clip_on=True)
    ax.plot([point_downright[0], point_downleft[0]], [point_downright[1], point_downleft[1]], color='red', lw=2, clip_on=True)

def drawLegend(ax):
    legend_elements = []
    for obj in deepSky_dict:
        if(deepSky_dict[obj][1]==1):
            legend_elements.append(Line2D([], [], marker=deepSky_dict[obj][0], color=background_color, label=obj,
                          markerfacecolor='w', markersize=25))

    l= plt.legend(handles=legend_elements, numpoints=1,loc='lower right', fontsize='20', facecolor=background_color,
               handler_map={tuple: HandlerTuple(ndivide=None)}, framealpha=1)
    for text in l.get_texts():
        text.set_color('w')
        
    """legend multiple
    p1, = plt.plot([1, 2.5, 3], 'k-d',markersize=15,markerfacecolor='w', color=background_color)
    p2, = plt.plot([3, 2, 1], marker='$\u2638$', markersize=25,markerfacecolor='w', color=background_color)
    #226D2
    l= plt.legend([(p1, p2)], ['Galaxie'], numpoints=1,loc='lower left', fontsize='30', facecolor=background_color,
               handler_map={tuple: HandlerTuple(ndivide=None)})
    """

            
def drawEphemerides(ax, obj_id, obj_type, start, stop, step, color, showDate, dateDisplayFreq, textPadding):
    #Bron
    loc = {'lon': 4.920591,
       'lat': 45.732450,
       'elevation': 0.2}

    obj = Horizons(id=obj_id, id_type=obj_type,location=loc, epochs={'start':start, 'stop':stop,'step':step})
    eph = obj.ephemerides()
    
    for i in range(0,len(eph)):
        x_text, y_text = ax.projection.transform_point(eph[i]['RA']-textPadding[0], eph[i]['DEC']+textPadding[1],src_crs=ccrs.Geodetic())
        x, y = ax.projection.transform_point(eph[i]['RA'], eph[i]['DEC'],src_crs=ccrs.Geodetic())
        ax.scatter(x,y,s=50, color=color, lw=0, edgecolor='none', zorder=15, marker='$\u25C6$' )
        if(showDate):
            if(i%dateDisplayFreq == 0 or i == 0):
                formatted_date = datetime.datetime.strptime(eph[i]['datetime_str'], '%Y-%b-%d %H:%M').strftime('%d/%m')
                ax.text(x_text,y_text,formatted_date, ha='center', va='center', fontsize=15,color='white',zorder=16)
            
            
def drawDeepSkyObject(ax, obj_name, object_type):

    target = SkyCoord.from_name(obj_name)  
    x, y = ax.projection.transform_point(target.ra.deg, target.dec.deg,src_crs=ccrs.Geodetic())
    
    ax.scatter(x,y, marker=deepSky_dict[object_type][0], color='white',zorder=16, s=250)
    ax.text(x,y-200000,obj_name, ha='center', va='center', fontsize=18,color='white',zorder=16, fontweight='normal')

    deepSky_dict[object_type][1]=1
    
    #circle = plt.Circle((x, y), 150000, fill=False, color='white', linewidth=1, zorder=20)
    #ax.add_artist(circle)
        