import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import tools

def draw_constellation(df, const_name):
    df_const = pd.read_csv('constellationship.fab', header=None)
    df_const['constellation'] = df_const[0].str.split().str.get(0)
    df_const['num_pairs'] = df_const[0].str.split().str.get(1)
    df_const['star_hip'] = df_const[0].str.split().str[2:]
    df_const.drop(0, axis=1, inplace=True)
    df_const['star_hip'].tolist()
    df_const = df_const[df_const['constellation'].str.contains(const_name, case=False, regex=True)]

    star_list =[int(y) for x in df_const['star_hip'].tolist() for y in x]
    for i in range(0,len(star_list),2):
        star_from = df[df['hip']==star_list[i]]
        star_to = df[df['hip']==star_list[i+1]]
        star_from_coord = [float(star_from['ra'])*360/24.0,float(star_from['dec'])]
        star_to_coord = [float(star_to['ra'])*360/24.0,float(star_to['dec'])]
        x_values = [star_from_coord[0], star_to_coord[0]]
        y_values = [star_from_coord[1], star_to_coord[1]]
        plt.plot(x_values, y_values, transform=ccrs.Geodetic(), 
                color='cyan', lw=1.2, alpha=.4, clip_on=True)


def draw_asterism(df, hip_list):


    for i in range(0,len(hip_list)-1,1):
        star_from = df[df['hip']==hip_list[i]]
        star_to = df[df['hip']==hip_list[i+1]]
        star_from_coord = [float(star_from['ra'])*360/24.0,float(star_from['dec'])]
        star_to_coord = [float(star_to['ra'])*360/24.0,float(star_to['dec'])]
        x_values = [star_from_coord[0], star_to_coord[0]]
        y_values = [star_from_coord[1], star_to_coord[1]]
        plt.plot(x_values, y_values, transform=ccrs.Geodetic(), 
                color='yellow', lw=1.2, alpha=.4, clip_on=True)


def init_asterism(name,largeView):
    if(name=="Lucky7"):
        if largeView:
            return 1,60,4,55,40,1,10
        else :
            return 23.1,61,8.5,7.5,7.5,1/6,2
        
    if(name=="GolfClub"):
        if largeView:
            return 2,45,4,55,40,1,10
        else :
            return 2,39,8.5,7.5,7.5,1/6,2
        
    if(name=="HomePlate"):
        if largeView:
            return 0.16,40,4,55,40,1,10
        else :
            return 0.16,40,8.5,7.5,7.5,1/6,2

def draw_Lucky7(ax, df, largeView):
    if(largeView):
        tools.drawPOIRect(ax,23.1,61,7.5,7.5)
    else :
        draw_asterism(df,[113852,113993,114186,114365,114104,113790,113498,113316,112998])
        draw_asterism(df,[115590,115218,114904,115245,115590])
        draw_asterism(df,[115245, 115267,115141,115023])
        
def draw_GolfClub(ax, df, largeView):
    if(largeView):
        tools.drawPOIRect(ax,2,39,7.5,7.5)
    else :
        draw_asterism(df,[8606,8734,8805,8930,9021,9001,8930])

def draw_HomePlate(ax, df, largeView):
    if(largeView):
        tools.drawPOIRect(ax,0,40,7.5,7.5)
    else :
        draw_asterism(df,[626,508,525,737,714,626])
        draw_asterism(df,[714,508])
