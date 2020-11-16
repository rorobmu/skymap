import pandas as pd


def process_star_catalog(constellations):
   
    df_hyg = pd.read_csv('hygdata_v3.csv', sep=',')
    #df_stars = df_hyg[df_hyg['bf'].str.contains(constellations, case=False, regex=True).fillna(False)]
    
    df_stars = df_hyg[df_hyg['mag']<=14]
    df_stars = df_stars[df_stars['dec']>=-55]
    #remove sun
    df_stars = df_stars[df_stars['proper']!='Sol']
    df_stars.to_csv('stars.csv', sep=';', index=False)


def get_df_visible_stars(df_full, mag):
    df_visible_stars = df_full[df_full['mag']<=mag]
    df_visible_stars = df_visible_stars[df_visible_stars['dec']>=-40]
    return df_visible_stars

