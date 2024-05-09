"""
Creates .WTH file from weather data file 

Input
-----
path: path to csv

the csv must contain following columns
- 'SRAD','Tmax','Tmin','Rain','timedate' 
- 'timedate' in format = '%m/%d/%Y'/%Y'

stname(optional)

    name of the station
    first 4 alphabets will be used as output file name

latitude

    of format = 123.456 

longitude

    of format = +-123.456
elevation

Output
------
    weather file stored as ABCD.WTH
"""
def WTH(path,stname = 'ABCd',latitude= 34.583,longitude= -103.200,elevation= 1348):
    """Creates .WTH file from weather data file. 

    Parameters
    ----------
    path: string path to csv.
        the csv must contain following columns
        - 'SRAD','Tmax','Tmin','Rain','timedate' 
        - 'timedate' in format = '%m/%d/%Y'

    stname(optional): string
        name of the station first 4 alphabets will be 
        used as output file name.

    latitude : float.
        of format = 123.456 .
        
    longitude : float
        of format = +-123.456 .

    elevation : float.
    
    Output
    ------
    writes .WTH file to cwd as f'{stname[0:4]}{yy}01.WTH'  for eg: ABCD2301.WTH.
    
    Returns
    -------
    weather file stored as f'{stname[0:4]}{yy}01.WTH'  for eg: ABCD2301.WTH.
    
    String : name of weather station
    """
    #Import Modules 
    import pandas
    df = pandas.read_csv(path)
    
    # Converting  the date column into desired format 
    
    df['timedate'] = pandas.to_datetime(df['TS'], format = '%m/%d/%Y')
    
    #Calculating the mean matrix for TAV and AMP contribution
    mean_mtx=df.loc[:365,['Tmax','Tmin']].groupby(df['timedate'].dt.month).mean()
    
    mean_mtx['mean']=mean_mtx[['Tmax','Tmin']].mean(axis=1)
    
    AMP = round(mean_mtx['mean'].mean(),1)
    TAV = round((mean_mtx['mean'].max()-mean_mtx['mean'].min())/2,1)
    
    # MODEL input format for date is YYdoy 
    # converting into YYdoy
    # Basic arithmetic operation  = (2023 - 2000)*1000 + 123 which gives 23123 (YYDOY)
    
    DATE=[]
    
    for i in range(len(df)):
        DATE.append(str(df['timedate'].dt.year[i])[-2:]+f"{df['timedate'].dt.dayofyear[i]:03}")    
    
        #saving the DATE in the dataframe at required place   
    df.insert(0,'DATE',DATE)
    
    
    yy=str(df['timedate'].dt.year[0])[-2:] #saving string for file name
    
    # rounding off to the desired input
    df[['SRAD','Tmax','Tmin','Rain']] = round(df[['SRAD','Tmax','Tmin','Rain']],1)
    df['DATE'] = df['DATE'].astype(str)
    
    #droping extra coulmns 
    
    df.drop(columns = ['TS','timedate'], inplace = True)
    df=df.reset_index(drop = True)
    ## Name of weather station 
    # This need to be entered in capital and four character length
    
    #station name
    station = stname.upper() # making sure entered station is in upper case
    
    
    #  headers : : weather file
    
    line1 =f'*WEATHER DATA : {station}\n'
    
    line2 = "\n" # blank line as per the format of .WTH files of DSSAT
    
    #line3 = ['@','INSI','LAT','LONG','ELEV','TAV','AMP','REFHT','WNDHT'] # list variables in this line
    
    line3 = '@ INSI      LAT     LONG  ELEV   TAV   AMP REFHT WNDHT\n'
    
    #line4 = [station,latitude,longitude, elevation,TAV,AMP, 11.2, -99.0, -99.0]
    
    line4 = f'  {station}{latitude:>9}{longitude:>9}  1348{TAV:>6}{AMP:>6} -99.0 -99.0\n'
    
    #line5 = ['@DATE','SRAD','TMAX','TMIN','RAIN','DEWP','WIND','PAR','EVAP','RHUM']
    
    line5 = '@DATE  SRAD  TMAX  TMIN  RAIN\n'
    
    # creating function to write weateher data in fixed format
    
    def data(v):
        data_value = f'{v[0]:>5}{v[1]:>6}{v[2]:>6}{v[3]:>6}{v[4]:>6}\n'
        return data_value
    # Initialize empty string
    wth = ''
    
    # Append additional lines
    wth += line1
    wth += line2
    wth += line3
    wth += line4
    wth += line5
    
    for k,row in df.iterrows():
        wth += data(row.values)
    
    # Write to a .WTH file
    
    with open(f'{station[0:4]}{yy}01.WTH', 'w') as file:
        file.write(wth)
    return f'{station[0:4]}{yy}01.WTH'  