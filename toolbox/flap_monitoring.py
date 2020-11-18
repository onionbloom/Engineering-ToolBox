import numpy as np
import pandas as pd
from datetime import datetime as dt, date, timedelta
import re
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class FlapDataExtractor:
    '''
    isi di sini
    '''

    def __init__(self, all_param_csv, output_path, dataframe_type='737-3B'):
        # if dataframe_type == None:
        #     raise NameError('Please specify the Dataframe Type')
        # if file_path == None:
        #     raise NameError('Please Specify the File Path')
        # if output_path == None:
        #     raise NameError('Please Specify the Output Path')

        self.category = 'flap_monitoring'
        self.output_path = output_path

        # read DFDR Data CSV

        self.dfdr_data = pd.read_csv(all_param_csv, low_memory=False, index_col=0)
        self.ac_reg = self.dfdr_data.loc[1, 'AC_REG']
        self.flight_no = self.dfdr_data.loc[1, 'FLIGHT_NO']

        # importing the Dataframe Cross Reference Database

        dataframedb_path = './toolbox/data/dataframe_db/param_crossref_{}.csv'.format(str.upper(dataframe_type))
        self.df_dataframedb = pd.read_csv(dataframedb_path)

    def extract_flap_skew(self):

        col_mandatory = ['DATETIME', \
                 'AC_REG', \
                 'FLIGHT_NO']

        col_cat = self.df_dataframedb.loc[self.df_dataframedb[self.category] == 'V', 'id_dataframe'].values.tolist()
        col_to_subset = col_mandatory + col_cat
        dfdr_data_sliced = self.dfdr_data[col_to_subset]

        dfdr_data_sliced['FLAPTRANS_ALL'] = dfdr_data_sliced['FLAPEXT_1'] & dfdr_data_sliced['FLAPEXT_2'] & dfdr_data_sliced['FLAPEXT_3'] & dfdr_data_sliced['FLAPEXT_4']
        dfdr_data_sliced['FLAPTRANS_IND'] = dfdr_data_sliced['FLAPEXT_1'] | dfdr_data_sliced['FLAPEXT_2'] | dfdr_data_sliced['FLAPEXT_3'] | dfdr_data_sliced['FLAPEXT_4']
        dfdr_data_sliced['FLAPTRANS_DISC'] = dfdr_data_sliced['FLAPTRANS_ALL'] ^ dfdr_data_sliced['FLAPTRANS_IND']

        dfdr_data_sliced['DELTA_FLAPPOS'] = (dfdr_data_sliced['TE_FLAPPSE_L'] - dfdr_data_sliced['TE_FLAPPSE_R']).abs()
        dfdr_data_sliced['DELTA_FLAPSYN'] = (dfdr_data_sliced['TE_FLAPPSE_L_SYNCRHO'] - dfdr_data_sliced['TE_FLAPPSE_R_SYNCHRO']).abs()

        dfdr_data_sliced['TE_FLPSK1TO8_VAL'] = (dfdr_data_sliced['TE_FLAPSKW_1'] - dfdr_data_sliced['TE_FLAPSKW_8']).abs()
        dfdr_data_sliced['TE_FLPSK2TO7_VAL'] = (dfdr_data_sliced['TE_FLAPSKW_2'] - dfdr_data_sliced['TE_FLAPSKW_7']).abs()
        dfdr_data_sliced['TE_FLPSK3TO6_VAL'] = (dfdr_data_sliced['TE_FLAPSKW_3'] - dfdr_data_sliced['TE_FLAPSKW_6']).abs()
        dfdr_data_sliced['TE_FLPSK4TO5_VAL'] = (dfdr_data_sliced['TE_FLAPSKW_4'] - dfdr_data_sliced['TE_FLAPSKW_5']).abs()

        self.dfdr_data_sliced = dfdr_data_sliced

        output_path = self.output_path
        date_early = self.dfdr_data.loc[1, 'DATETIME']
        output_name = 'extract' + '_' + self.category.replace('_', ' ').title().replace(' ', '') + '_' + self.ac_reg + '_' + self.flight_no + '_' + date_early.strftime("%Y-%m-%d") + '.csv'
        output_path_complete = output_path + '/' + output_name
        dfdr_data_sliced.to_csv(output_path_complete)
        return dfdr_data_sliced

        
