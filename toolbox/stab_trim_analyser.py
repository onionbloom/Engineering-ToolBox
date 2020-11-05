import numpy as np
import pandas as pd
from datetime import datetime as dt, date, timedelta
import re
import sys
import os
import errno
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class StabTrimAnalyser:
    '''
    isi di sini
    '''

    def __init__(self, file_path=None, dataframe_type=None, output_path=None):
        # if dataframe_type == None:
        #     raise NameError('Please specify the Dataframe Type')
        # if file_path == None:
        #     raise NameError('Please Specify the File Path')
        # if output_path == None:
        #     raise NameError('Please Specify the Output Path')

        self.category = 'stab_trim_problem'
        self.output_path = output_path

        # read DFDR Data CSV

        # self.dfdr_data = pd.read_csv(file_path, low_memory=False, index_col=0)

        dfdr_data = file_path
        self.dfdr_data = dfdr_data
        dfdr_data.index = dfdr_data.index.astype('int64')
        list_index = list(dfdr_data.index.values.tolist())
        first_index = list_index[0]
        self.first_index = first_index
        self.ac_reg = self.dfdr_data.loc[first_index, 'AC_REG']
        self.flight_no = self.dfdr_data.loc[first_index, 'FLIGHT_NO']

        # importing the Dataframe Cross Reference Database

        dataframedb_path = 'dataframe_db/param_crossref_{}.csv'.format(str.upper(dataframe_type))
        self.df_dataframedb = pd.read_csv(dataframedb_path)

    def extract_dfdr_data(self):
        dfdr_data = self.dfdr_data
        df_dataframedb = self.df_dataframedb
        category = self.category
        ac_reg = self.ac_reg
        flight_no = self.flight_no

        col_mandatory = ['DATETIME', \
                 'AC_REG', \
                 'FLIGHT_NO']

        col_cat = df_dataframedb.loc[df_dataframedb[category] == 'V', 'id_dataframe'].values.tolist()
        col_to_subset = col_mandatory + col_cat
        dfdr_data_sliced = dfdr_data[col_to_subset]

        # Trim Command Coding

        dfdr_data_sliced['TRIM_A_P_CD'] = 0
        dfdr_data_sliced['TRIM_MAN_CD'] = 0

        for index, row in dfdr_data_sliced.iterrows():
            if row['TRIMUP_A_P'] == 'TRIM':
                dfdr_data_sliced.loc[index, 'TRIM_A_P_CD'] = 1
            elif row['TRIMDOWN_A_P'] == 'TRIM':
                dfdr_data_sliced.loc[index, 'TRIM_A_P_CD'] = -1
            elif row['TRIMUP_MAN'] == 'TRIM':
                dfdr_data_sliced.loc[index, 'TRIM_MAN_CD'] = 1
            elif row['TRIMDOWN_MAN'] == 'TRIM':
                dfdr_data_sliced.loc[index, 'TRIM_MAN_CD'] = -1
        
        # Trim Simulation

        trim_speed_ap_flap_up = 0.09
        trim_speed_ap_flap_dwn = 0.27
        trim_speed_man_flap_up = 0.2
        trim_speed_man_flap_dwn = 0.4

        dfdr_data_sliced['FLAPTRANS_ALL'] = dfdr_data_sliced['FLAPTRANS_1'] & dfdr_data_sliced['FLAPTRANS_2'] & dfdr_data_sliced['FLAPTRANS_3'] & dfdr_data_sliced['FLAPTRANS_4']
        dfdr_data_sliced['FLAPEXT_ALL'] = dfdr_data_sliced['FLAPEXT_1'] & dfdr_data_sliced['FLAPEXT_2'] & dfdr_data_sliced['FLAPEXT_3'] & dfdr_data_sliced['FLAPEXT_4']

        dfdr_data_sliced['SIM_PITCHTRIMPOS'] = 0
        for index, row in dfdr_data_sliced.iterrows():
            if index == 1:
                dfdr_data_sliced.loc[index, 'SIM_PITCHTRIMPOS'] = dfdr_data_sliced.loc[index, 'PITCHTRIMPOS']
            elif row['TRIM_A_P_CD'] != 0 and row['FLAPEXT_ALL'] == True:
                dfdr_data_sliced.loc[index, 'SIM_PITCHTRIMPOS'] = dfdr_data_sliced.loc[index - 1, 'SIM_PITCHTRIMPOS'] + (row['TRIM_A_P_CD'] * trim_speed_ap_flap_dwn)
            elif row['TRIM_A_P_CD'] != 0 and row['FLAPEXT_ALL'] == False:
                dfdr_data_sliced.loc[index, 'SIM_PITCHTRIMPOS'] = dfdr_data_sliced.loc[index - 1, 'SIM_PITCHTRIMPOS'] + (row['TRIM_A_P_CD'] * trim_speed_ap_flap_up)
            elif row['TRIM_MAN_CD'] != 0 and row['FLAPEXT_ALL'] == True:
                dfdr_data_sliced.loc[index, 'SIM_PITCHTRIMPOS'] = dfdr_data_sliced.loc[index - 1, 'SIM_PITCHTRIMPOS'] + (row['TRIM_MAN_CD'] * trim_speed_man_flap_dwn)
            elif row['TRIM_MAN_CD'] != 0 and row['FLAPEXT_ALL'] == False:
                dfdr_data_sliced.loc[index, 'SIM_PITCHTRIMPOS'] = dfdr_data_sliced.loc[index - 1, 'SIM_PITCHTRIMPOS'] + (row['TRIM_MAN_CD'] * trim_speed_man_flap_up)
            else:
                dfdr_data_sliced.loc[index, 'SIM_PITCHTRIMPOS'] = dfdr_data_sliced.loc[index - 1, 'SIM_PITCHTRIMPOS']

        # OUTPUT

        output_path = self.output_path
        date_early = dfdr_data.loc[1, 'DATETIME']
        self.date_early = date_early
        output_folder_name = ac_reg + '_' + flight_no + '_' + date_early.strftime("%Y-%m-%d")
        output_path_added = output_path + '/' + output_folder_name + '/' + category.replace('_', ' ').title().replace(' ', '') + '/'

        file_name = 'dfdr_data_extracted.csv'
        output_path_complete = output_path_added + file_name

        self.dfdr_data_sliced = dfdr_data_sliced
        self.output_path_added = output_path_added

        if not os.path.exists(os.path.dirname(output_path_complete)):
            try:
                os.makedirs(os.path.dirname(output_path_complete))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        
        dfdr_data_sliced.to_csv(output_path_complete)
        return dfdr_data_sliced

    def plot_all(self, data=None, show_plot=True):
        fig, ax1 = plt.subplots(2, 1, sharex='all', figsize=[16, 9], dpi=166)

        ax1[0].set_ylabel('TRIM COMMAND', color = 'k')
        ax1[0].plot(data['DATETIME'], data['TRIM_A_P_CD'], color='#faf44b', label='TRIM COMMAND - A/P')
        ax1[0].plot(data['DATETIME'], data['TRIM_MAN_CD'], color='#ffb52b', label='TRIM COMMAND - MANUAL')
        ax1[0].legend(loc="lower left")

        ax2 = ax1[0].twinx()
        ax2.set_ylabel('PITCH TRIM POSITION', color = 'k')
        ax2.plot(data['DATETIME'], data['PITCHTRIMPOS'], color='k', label='ACTUAL')
        ax2.plot(data['DATETIME'], data['SIM_PITCHTRIMPOS'], color='r', label='SIMULATED')
        ax2.legend(loc="lower right")

        ax1[1].plot(data['DATETIME'], data['ALTITUDE'], color='k')
        ax1[1].set_xlabel('TIME')
        ax1[1].set_ylabel('ALTITUDE')

        fig_title = 'COMPARASION: ACTUAL VS SIMULATED PITCH TRIM POSN' + '\n' + self.ac_reg + ' ' + self.flight_no + ' ' + self.date_early.strftime("%Y-%m-%d")

        fig.suptitle(fig_title, fontsize=12)

        xformatter = mdates.DateFormatter('%H:%M')
        ax1[1].xaxis.set_major_formatter(xformatter)

        output_path_added = self.output_path_added
        file_name = 'figure_plot.png'
        output_path_complete = output_path_added + file_name

        if not os.path.exists(os.path.dirname(output_path_complete)):
            try:
                os.makedirs(os.path.dirname(output_path_complete))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        plt.savefig(output_path_complete)

        if show_plot == True:
            plt.show()
        
