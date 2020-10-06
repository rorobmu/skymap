import pandas as pd
import numpy as np


#00365A


def process_star_catalog(constellations):
    colwidths = [4,10,11,6,6,4,1,1,1,5,2,9,2,2,4,1,2,2,2,2,2,4,1,2,2,2,6,6,5,
                 1,1,5,1,5,1,5,1,20,1,6,6,1,5,4,4,2,3,1,4,6,4,2,1]
    colnames = ['HR_number', 'Name', 'DM', 'HD', 'SAO', 'FK5','IRflag','r_IRflag', 'Multiple', 'ADS'
                , 'ADScomp', 'VarID', 'RAh1900', 'RAm1900', 'RAs1900', 'DE-1900', 'DEd1900', 'DEm1900', 'DEs1900'
                ,'RAh','RAm', 'RAs', 'DE-', 'DEd', 'DEm', 'DEs', 'GLON', 'GLAT', 'Vmag', 'n_Vmag', 'u_Vmag', 'B-V', 'u_B-V'
                , 'U-B', 'u_U-B', 'R-I', 'n_R-I', 'SpType', 'n_SpType', 'pmRA', 'pmDE', 'n_Parallax', 'Parallax', 'RadVel'
                , 'n_RadVel', 'l_RotVel', 'RotVel', 'u_RotVel', 'Dmag', 'Sep', 'MultID', 'MultCnt', 'NoteFlag']
    
    df = pd.read_fwf('catalog.dat', widths=colwidths, names=colnames)
    df_name_notna = df['Name'].notna()
    df_stars = df[df['Name'].str.contains('UMa').fillna(False)]
    df_stars = df_stars[df_stars['Vmag']<=6.5]
    df_stars['RA'] = df_stars['RAh'] + df_stars['RAm']/60 + df_stars['RAs']/3600
    df_stars['Dec'] = df_stars['DEd'] + df_stars['DEm']/60 + df_stars['DEs']/3600
    df_stars['Dec'] = df_stars['DE-'] + df_stars['Dec'].astype(str)
    df_stars['Dec'] = df_stars['Dec'].astype(float)
    
    df_hyg = pd.read_csv('hygdata_v3.csv', sep=',')
    df_stars = df_hyg[df_hyg['bf'].str.contains(constellations, case=False, regex=True).fillna(False)]
    df_stars = df_stars[df_stars['mag']<=6.5]
    df_stars.to_csv('stars.csv', sep=';', index=False)



