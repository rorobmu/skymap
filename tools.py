import cartopy.crs as ccrs
import matplotlib.pyplot as plt


corner_lim_up_left_x=0
corner_lim_up_left_y=0
corner_lim_down_right_x=0
corner_lim_down_right_y=0
noBound=False

def initFigure(ra_min, ra_max, central_latitude):
    #draw figures
    figsize = (40, 20)
    background_color = '#00365A'
    
    plt.figure(figsize=figsize)
    ax = plt.axes(projection=ccrs.AzimuthalEquidistant(
        central_longitude=((ra_min+ra_max)/2)*360/24.0, central_latitude=central_latitude))
    ax.background_patch.set_facecolor(background_color)
    return ax

def initBound(ax, ra_up_left, dec_up_left, ra_down_right, dec_down_right, isNoBound):
    global corner_lim_up_left_x
    global corner_lim_up_left_y
    global corner_lim_down_right_x
    global corner_lim_down_right_y
    global noBound
    
    noBound=isNoBound
    
    corner_lim_up_left_x, corner_lim_up_left_y =  ax.projection.transform_point(ra_up_left*360/24, dec_up_left,src_crs=ccrs.Geodetic())
    ax.scatter(corner_lim_up_left_x,corner_lim_up_left_y,
                color='green', lw=10, alpha=1, clip_on=True)
    
    
    corner_lim_down_right_x, corner_lim_down_right_y = ax.projection.transform_point(ra_down_right*360/24, dec_down_right,src_crs=ccrs.Geodetic())
    ax.scatter(corner_lim_down_right_x,corner_lim_down_right_y,
                color='red', lw=10, alpha=1, clip_on=True)

def isInBound(x, y):
    if(noBound):
        return True
    if(x>corner_lim_up_left_x and x<corner_lim_down_right_x 
           and y<corner_lim_up_left_y and y>corner_lim_down_right_y):
        return True
    return False



def cropAndRevserseImage(ax):
    if(noBound):
        ax.set_xlim(ax.get_xlim()[::-1])
        ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[1])
    else:
        ax.set_xlim(corner_lim_down_right_x, corner_lim_up_left_x)
        ax.set_ylim(corner_lim_down_right_y, corner_lim_up_left_y)