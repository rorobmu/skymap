import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


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
                color='cyan', lw=3, alpha=.4, clip_on=True)


