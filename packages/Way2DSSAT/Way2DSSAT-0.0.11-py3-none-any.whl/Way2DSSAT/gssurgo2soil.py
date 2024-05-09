"""Converts gSSURGO format into DSSAT .SOL format.
    
Arguments

path -- string
path to your .csv file containing the data from gSSURGO. Must have the following columns(and other related depths)
WC15Bar_DCP_0to5
WC3rdbar_DCP_0to5
Clay_DCP_0to5
Silt_DCP_0to5
pHwater_DCP_0to5
CEC_DCP_0to5
Db3rdbar_DCP_0to5
Ksat_DCP_0to5
OrgMatter_DCP_0to5
MUKEY_DCP_0to5          

Return --

SG.SOL file in cwd

a py dictionary of format
dictionary = {MUKEY :{depth:SH2O}}

a list of all the Mukeys

Example --

path = 'Username/pathtothecsv'
A,B = ssurgo2soil(path)          
"""

def SOL(path):
    """Converts gSSURGO format into DSSAT .SOL format.

    Parameters
    ----------
    path : string
        path to your .csv file containing the data from gSSURGO. Must have the following columns(and other related depths)
            - WC15Bar_DCP_0to5
            - WC3rdbar_DCP_0to5
            - Clay_DCP_0to5
            - Silt_DCP_0to5
            - pHwater_DCP_0to5
            - CEC_DCP_0to5
            - Db3rdbar_DCP_0to5
            - Ksat_DCP_0to5
            - OrgMatter_DCP_0to5
            - MUKEY_DCP_0to5          

    Output
    ------
    Creates a SG.SOL file in cwd.
    
    Returns
    -------
    A : Dictionary of format.
        A = {MUKEY :{depth:SH2O}}.

    B : List of all the Mukeys.

    Example
    -------
    path = 'Username/pathtothecsv'.
    
    A,B = ssurgo2soil(path)
    """
    import pandas
    import math
    #Reading csv  
    df_soil = pandas.read_csv(path)
    #Returns list of columns not required with specific keyword
    # data from ssurgo contains columns suchas pct_Silt** which aren't required
    # Removing those columns form the dataframe
    # These have column name are duplicate of the required soil properties with additional pct in 
    # the name. Thus posing difficulty in calling the column name with keyword
    columns_not_req = list(df_soil.columns.array[list(df_soil.columns.str.contains('pct'))])
    #
    # copying the orignal dataframe
    df=df_soil
    #
    # droping the columns not required
    df= df.drop(columns=columns_not_req)
    #
    #Getting the column name for each parameter 
    SLLL_columns = list(df.columns.array[list(df.columns.str.contains('WC15Bar'))])
    SDUL_columns = list(df.columns.array[list(df.columns.str.contains('WC3rdbar'))])
    SLCL_columns = list(df.columns.array[list(df.columns.str.contains('Clay'))])
    SLSI_columns = list(df.columns.array[list(df.columns.str.contains('Silt'))])
    SLHW_columns = list(df.columns.array[list(df.columns.str.contains('pHwater'))])
    SCEC_columns = list(df.columns.array[list(df.columns.str.contains('CEC'))])
    SBDM_columns = list(df.columns.array[list(df.columns.str.contains('Db3rdbar'))])
    SSKS_columns = list(df.columns.array[list(df.columns.str.contains('Ksat_'))])
    SLOC_columns = list(df.columns.array[list(df.columns.str.contains('OrgMatter'))])
    Mukey_columns = list(df.columns.array[list(df.columns.str.contains('MUKEY'))])
    #
    # CODING LINES IN .SOL FILE FORMAT
    Mukey=0
    line1 = "*Soils: Created by py2Sol library\n"
    line2="\n"
    #CL is the texture which needed to be specified later in the soil profile
    #200 is the maximum depth of soil
    # seriesname can have spaces upto this length "but ca"
    #
    line4='@SITE        COUNTRY          LAT     LONG SCS FAMILY\n'  
    #
    # Input for latitude longitude is given here and 
    line5 = ' Havlock     USA                40      96 Havlock series\n'
    line6 = '@ SCOM  SALB  SLU1  SLDR  SLRO  SLNF  SLPF  SMHB  SMPX  SMKE\n'
    #
    #seventh line includes::
    #SCOM -    colour of soil (BN for brown)
    #SALB -    albedo (here 0.13 for brown)
    #SLDR -    Drainage rate, fraction day-1
    #SLRO -    Runoff curve no
    #SLNF -    Mineralization factor, 0 to 1 scale(default 1)
    #SLPF -    Soil fertility factor, 0 to 1 scale(default 1)
    #SMHB -    pH in buffer determination method, code(default IB001)               
    #SMKE -    Potassium determination method, code (Default IB001)                  
    #SMPX -    Phosphorus determination code(Default IB001)
    #
    #
    line7 = '    BN   .13     6    .6    61     1     1 IB001 IB001 IB001\n'
    #
    #
    #Header for the data to be stored in the file
    line8 = "@  SLB  SLMH  SLLL  SDUL  SSAT  SRGF  SSKS  SBDM  SLOC  SLCL  SLSI  SLCF  SLNI  SLHW  SLHB  SCEC  SADC\n"
    #
    #8th line includes
    # SBL     Depth, base of layer, cm                                            
    # SLMH     Master horizon 
    # SLLL     Lower limit of plant extractable soil water, cm3 cm-3 
    # SDUL     Drained upper limit, cm3 cm-3                                      
    # SSAT     Upper limit, saturated, cm3 cm-3                      
    # SRGF     Root growth factor, soil only, 0.0 to 1.0             
    # SSKS     Sat. hydraulic conductivity, macropore, cm h-1        
    # SBDM     Bulk density, moist, g cm-3                                         
    # SLOC     Organic carbon, %                                     
    # SLCL     Clay (<0.002 mm), %                                                  
    # SLSI     Silt (0.05 to 0.002 mm), %                            
    # SLCF     Coarse fraction (>2 mm), %                                           
    # SLNI     Total nitrogen, %                                     
    # SLHW     pH in water                                                          
    # SLHB     pH in buffer                                                         
    # SCEC     Cation exchange capacity, cmol kg-1                                 
    # SADC     Anion adsorption coefficient (reduced nitrate flow), cm3 
    # Writing lines to the text documents
    #
    #Initialize empty string
    Soil=''
    # 
    SH20 = {}
    soil_for_X={}
    MU_key=[]
    #
    for j in range(0,len(df)):
        Mukey = df[Mukey_columns].loc[j,Mukey_columns[0]]
        MU_key.append(Mukey)
        # Appending teh empty string
        Soil+=line1
        Soil+=line2
        Soil+=f'*GSS{Mukey:07}  SSURGO      CL         200 seriesname can have spaces upto this length but ca\n'
        Soil+=line4
        Soil+=line5
        Soil+=line6
        Soil+=line7
        Soil+=line8
    
        #adding the data to the file 
    
        SLCF = '-99'
        SLMH = '-99'
        SRGF = 1
        SLNI = '-99'
        SLHB= '-99'
        SADC = '-99'
    
        for i in range(0,len(SLCL_columns)):
            SLB =int(SLCL_columns[i].split('to')[1]) #DEPTH
    
            SLLL=round(df[SLLL_columns].loc[j,SLLL_columns[i]]/100,3) 
            SDUL=round(df[SDUL_columns].loc[j,SDUL_columns[i]]/100,3)
            SLCL=round(df[SLCL_columns].loc[j,SLCL_columns[i]],1)
            SLSI=round(df[SLSI_columns].loc[j,SLSI_columns[i]],1)
            SSAT= round(0.3332 + (-0.000725)*(SLSI)+0.12768*math.log10(SLCL) , 3) #from DSSAT mannual
            SLHW=round(df[SLHW_columns].loc[j,SLHW_columns[i]],3)
            SCEC=round(df[SCEC_columns].loc[j,SCEC_columns[i]],3)
            SBDM= round(df[SBDM_columns].loc[j,SBDM_columns[i]],3)
            SSKS=round(df[SSKS_columns].loc[j,SSKS_columns[i]]*0.36,2) #from micrometer /second to cm /hour
            SLOC=round(df[SLOC_columns].loc[j,SLOC_columns[i]],3)
            Soil+= f'{SLB:>6}{SLMH:>6}{SLLL:>6}{SDUL:>6}{SSAT:>6}{SRGF:>6}{SSKS:>6}{SBDM:>6}{SLOC:>6}{SLCL:>6}{SLSI:>6}{SLCF:>6}{SLNI:>6}{SLHW:>6}{SLHB:>6}{SCEC:>6}{SADC:>6}\n'
            SH20[SLB] = SDUL
        Soil+='\n'
        soil_for_X[f'GSS{Mukey}']=SH20
    # Write to a .SOL file
    with open(f'GS.SOL', 'w') as file:
        file.write(Soil)
    return soil_for_X,MU_key