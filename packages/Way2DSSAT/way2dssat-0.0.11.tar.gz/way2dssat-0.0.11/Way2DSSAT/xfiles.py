"""Function to create DSSAT X file from a template X file.

input
-----
path: path to the template file
    Example template 
    https://github.com/ManavjotSingh97/Way2DSSAT/blob/main/Seasonl/KSMR6301.SNX

init_cond:
    dictinary of initial key as depth and value as SDUL  
    for example dict = 'GSS2733104': {5: 0.2, 15: 0.2, 30: 0.2, 60: 0.2, 
                                                100: 0.338, 200: 0.308} 
site_name:
    string of site name less than 120 char

station:
    string of max 8 character eg: UFGA8201 or ABCD(default)

soil:
    soil name, (not the .SOL file name) for eg: GSS2733103(default)
crop:
    two character for eg: SB(default)

cultivar:
    full cultivar name, for eg: NE0006 NECPHA4 2014 (default)

planting_date:
    planting date in format yydoy , for eg: 24145

Returns
-------
    xfile .SNX in cwd

Example
-------
    path = 'C:path/to/the/template'
    init_cond = {5: 0.2, 15: 0.2, 30: 0.2, 60: 0.2, 100: 0.338, 200: 0.308}
    Xfile()

    """

def Xfile(path,init_cond,site_name = '-99',station = 'ABCD',soil = 'GSS2733103',
          crop = 'SB',cultivar = 'NE0006 NECPHA4 2014',planting_date = '24145'):
    """Function to create DSSAT X file from a template X file.

    Parameters
    ----------

    path: path to the template file.
        Example template 
        https://github.com/ManavjotSingh97/Way2DSSAT/blob/main/Seasonl/KSMR6301.SNX

    init_cond:
        dictinary of initial key as depth and value as SDUL.  
        for example dict = 'GSS2733104': {5: 0.2, 15: 0.2, 30: 0.2, 60: 0.2} 

    site_name:
        string of site name less than 120 char.

    station:
        string of max 8 character eg: UFGA8201 or ABCD(default).

    soil:
        soil name, (not the .SOL file name) for eg: GSS2733103(default).

    crop:
        two character for eg: SB(default).

    cultivar:
        full cultivar name, for eg: NE0006 NECPHA4 2014 (default).

    planting_date:
        planting date in format yydoy , for eg: 24145.

    Output
    -------
        Writes xfile of format .SNX in cwd.
    """
    #Variables that can be changed

    #geting the year part from planting_date variable
    yy=planting_date[0:2]
    crop = crop.upper()
    
    #Checking error in input
    if len(site_name) >120:
        return 'error, site name greater than max length 120'
    if len(station) >8:
        return 'error, station name greater than max length 8, input e.g: UFGA8201'
    if len(soil) >10:
        return 'error, soil name greater than max length 10, input eg:IBSB910015'
    if len(crop) !=2:
        return 'error, crop code out of bound, input eg: SB'
    # #No check for cultivar 
    if len(planting_date)!=5:
        return 'error, planting date out of bound' 


    counter=0
    linenum=[]
    with open(path, 'r') as input_file:
        for line in input_file:
            counter+=1

            #getting line numbers where we need to change the variables

            if '@SITE' in line:
                s=counter
                linenum.append(s+1)            
            if '*CULTIVARS' in line:
                cult=counter
                linenum.append(cult+2)
            if'*FIELDS' in line:
                fields=counter
                linenum.append(fields+2)
            if '*INITIAL CONDITIONS' in line:
                init = counter
                linenum.append(init+2)
                linenum.append(init+4)
            if '*PLANTING' in line:
                plnt=counter
                linenum.append(plnt+2)
            if 'SIMULATION CONTROLS' in line:
                sim = counter
                linenum.append(sim+2)


    counter2=0            

    with open(path, 'r') as input_file, open(f'{station[0:4]}{yy}01.SNX', 'w') as output_file:
        # iterating through lines in inputfile
        for line in input_file:
            counter2 += 1

            #if the line number equals the element in listnum change the line

            if counter2 in linenum:

                #changed site name
                if counter2 == linenum[0]:
                    changed_line = f'{site_name} \n'
                    output_file.write(changed_line)

                #changed crop and cultivar name
                if counter2 == linenum[1]:
                    changed_line = f' 1 {crop} {cultivar}\n'
                    output_file.write(changed_line)

                #changed weather station and soil type
                if counter2 == linenum[2]:
                    changed_line = f' 1 UFGA0001 {station:8}   -99     0 DR000     0     0 00000 -99    180  {soil} -99\n'
                    output_file.write(changed_line)    

                #changed intial conditions collection date assumed same as planting date
                if counter2 == linenum[3]:
                    changed_line = f' 1   -99 {planting_date}   -99   -99     1     1   -99   -99   -99   -99   -99   -99 -99\n'
                    output_file.write(changed_line)

                #changed soil conditions
                if counter2 == linenum[4]:
                 #   next(input_file)
                    # #loop through soil prop from dictionary given by previous code
                    for key,values in init_cond.items():
                        changed_line = f' 1{key:>6}{values:>6}    .1     1\n'
                        output_file.write(changed_line)
                    output_file.write('\n')

                #changed planting date
                if counter2== linenum[5]:
                    changed_line = f' 1 {planting_date}   -99    50   -99     S     R    30    90   2.5   -99   -99   -99   -99   -99                        -99\n'
                    output_file.write(changed_line)

                #changing simulation control
                if counter2 == linenum[6]:
                    changed_line = f' 1 GE             10     1     S {planting_date}  2150 DEFAULT SEASONAL CONTROL\n'
                    output_file.write(changed_line)

            #removing existing information if any in the template file
            elif counter2>linenum[4] and counter2<plnt:
                output_file.write('')

            else:
                output_file.write(line)