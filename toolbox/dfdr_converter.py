import pandas as pd
import re
import numpy as np
import os
import errno
from datetime import date
from datetime import timedelta

class DfdrConverter:
    '''
    dfdr_converter
    This function will read and convert the DFDR Raw (.csv) file from specific Dataframe type to more uniform table.

    Inputs:
    file_path - File Path to the CSV file from DFDR Readout (Absolute Path)
    output_path - Folder Path to the OUTPUT of CSV file after cleaning and tidying process (Absolute Path)
    separator - Separator or Delimiter of the column in the .csv file. The default value of this input in comma ","
    dataframe_type - The type of dataframe used by the on the Aircraft from which the CSV file was obtained after DFDR readout 

    Methods:
    dfdr_data - CSV file which already cleaned and tidied up.

    Example Usage:
    filepath = "DFDR Data/PK-GFD_GA448.csv"
    separator = ","
    dataframe_type = "737-3B"
    output = dfdr_converter(filepath, separator, dataframe_type)
    '''

    def __init__(self, file_path=None, output_path=None, separator=',', dataframe_type=None):
        if file_path == None:
            raise NameError('Please Specify the File Path')
        if dataframe_type == None:
            raise NameError('Please specify the Dataframe Type')
        if separator not in [',', ':', '.', ';']:
            raise ValueError('Separator not acceptable. Only comma, colon, semicolon, and decimal can be accepted')
        if len(separator) > 1:
            raise ValueError('Too much value on the separator. Only one separator value can be accepted')

        self.file_path = file_path
        self.output_path = output_path
        self.separator = separator
        self.dataframe_type = dataframe_type

        # initializing Aircraft Registration and Flight Number

        file_path_splitted = self.file_path.split('/')
        self.file_name = file_path_splitted[-1]
        ac_reg_list = re.findall(r'PK-[A-Z]+', self.file_name)
        self.ac_reg = ac_reg_list[0]

        # importing DFDR Data from CSV
        
        self.dfdr_data = pd.read_csv(self.file_path, low_memory=False, index_col=0, sep=self.separator)

        # importing the Dataframe Cross Reference Database
        
        dataframedb_path = 'dataframe_db/param_crossref_{}.csv'.format(str.upper(self.dataframe_type))
        self.df_dataframedb = pd.read_csv(dataframedb_path)

    def dfdr_tidy(self):
        
        # dropping unused row in DFDR Data

        dfdr_data = self.dfdr_data
        dfdr_data = dfdr_data.drop(dfdr_data.index[0], axis=0)

        # renaming each column making the column name uniform and pandas friendly

        df_dataframedb = self.df_dataframedb
        dict_dataframedb = dict(zip(df_dataframedb['id_dfdr'], df_dataframedb['id_dataframe']))
        dfdr_data = dfdr_data.rename(columns=dict_dataframedb)

        # filling empty value on each column
        
        dfdr_data = dfdr_data.fillna(method='ffill').fillna(method='bfill')

        # creating a datetime

        ac_reg = self.ac_reg
        dfdr_data['YEAR'] = '20' + dfdr_data['YEAR']
        dfdr_data['DATETIME'] = ''

        list_index = list(dfdr_data.index.values.tolist())
        first_index = list_index[0]
        self.first_index = first_index

        if dfdr_data['MONTH'].dtypes != object:
            if np.isnan(dfdr_data.loc[1, 'MONTH']) == True:
                print('MONTH Column is empty')
                month_manual = input('Specify MONTH in number here: ')
                dfdr_data['MONTH'] = month_manual
            else:
                dfdr_data['MONTH'] = dfdr_data['MONTH']
        else:
            dfdr_data['MONTH'] = dfdr_data['MONTH']

        if dfdr_data['DAY'].dtypes != object:
            if np.isnan(dfdr_data.loc[1, 'DAY']) == True:
                print('DAY Column is empty')
                day_manual = input('Specify DAY in number here: ')
                dfdr_data['DAY'] = day_manual
            else:
                dfdr_data['DAY'] = dfdr_data['DAY']
        else:
            dfdr_data['DAY'] = dfdr_data['DAY']
        
        dfdr_data.loc[first_index, 'DATETIME'] = pd.to_datetime(dfdr_data.loc[first_index, 'YEAR']
                                                + '-' + dfdr_data.loc[first_index, 'MONTH']
                                                + '-' + dfdr_data.loc[first_index, 'DAY']
                                                + ' ' + dfdr_data.loc[first_index, 'GMT'])
        
        delta_datetime = timedelta(seconds=1)
        for index, row in dfdr_data.iterrows():
            if index == first_index:
                continue
            else:
                dfdr_data.loc[index, 'DATETIME'] = dfdr_data.loc[index - 1, 'DATETIME'] + delta_datetime
            
        dfdr_data['AC_REG'] = ac_reg

        regex_fltno = re.compile(r'G[A-Z]{1,2}\d{2,4}')
        FLTNUMBCHAR_extracted_list = list(set(dfdr_data['FLTNUMBCHAR'].dropna().tolist()))
        FLTNUMBCHAR_matched = list(filter(regex_fltno.match, FLTNUMBCHAR_extracted_list))
        flight_no = re.findall(regex_fltno, FLTNUMBCHAR_matched[0])
        dfdr_data['FLIGHT_NO'] = flight_no[0]

        # converting the column type of dfdr_data dataframe from object to numeric

        col_to_numeric = df_dataframedb.loc[df_dataframedb['d_type'] == 'numeric', 'id_dataframe'].values.tolist()
        col_header = list(dfdr_data.columns.values)
        col_to_numeric_crosscheck = []
        for col_name in col_to_numeric:
            if col_name in col_header:
                col_to_numeric_crosscheck.append(col_name)
            else:
                continue
        dfdr_data[col_to_numeric_crosscheck] = dfdr_data[col_to_numeric_crosscheck].apply(pd.to_numeric, errors='coerce')
        dfdr_data.index = dfdr_data.index.astype('int64')

        # output

        output_path = self.output_path
        date_early = dfdr_data.loc[1, 'DATETIME']
        output_folder_name = ac_reg + '_' + flight_no[0] + '_' + date_early.strftime("%Y-%m-%d")
        output_path_added = output_path + '/' + output_folder_name + '/' + 'DFDR_Converter' + '/'

        file_name = 'dfdr_data_tidy.csv'
        output_path_complete = output_path_added + file_name

        if not os.path.exists(os.path.dirname(output_path_complete)):
            try:
                os.makedirs(os.path.dirname(output_path_complete))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        dfdr_data.to_csv(output_path_complete)
        return dfdr_data


    
