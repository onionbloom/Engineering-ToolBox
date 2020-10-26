import pandas as pd
import re
import numpy as np
import os
import errno
from datetime import date
from datetime import timedelta

from toolbox import app


class DfdrConvert:

    def __init__(self, raw_dfdr_csv, filename):
        self.raw_dfdr_df = pd.read_csv(raw_dfdr_csv)
        self.raw_dfdr_csv = filename

    def dfdr_tidy(self):
        dfdr_data = self.raw_dfdr_df

        # drop unused row
        dfdr_data = dfdr_data.drop(dfdr_data.index[0], axis=0)

        # add AC Reg, Date, and Flight No columns
        regex_AC_REG = re.findall(r'G[A-Z]+', self.raw_dfdr_csv)
        regex_Date = re.findall(r'\d{6,8}', self.raw_dfdr_csv)
        regex_FlightNo = re.findall(r'GIA\d{2,4}', self.raw_dfdr_csv)
        dfdr_data['AC_Reg'] = 'PK-'+regex_AC_REG[0]
        dfdr_data['Date'] = regex_Date[0]
        dfdr_data['Date'] = pd.to_datetime(dfdr_data['Date'], format='%y%m%d')
        dfdr_data['GMT'] = pd.to_datetime(
            dfdr_data['GMT'], format='%H:%M:%S').dt.time
        dfdr_data['FlightNo'] = regex_FlightNo[-1]

        # select parameter columns
        columns = ['AC_Reg', 'FlightNo', 'Date', 'GMT', 'Air/Ground', 'Altitude', 'Airspeed', 'Flap Handle-Pos', 'Flap Posn-L', 'Flap Posn-R',
                   'FlapSkew 1 Pos', 'FlapSkew 2 Pos', 'FlapSkew 3 Pos', 'FlapSkew 4 Pos', 'FlapSkew 5 Pos', 'FlapSkew 6 Pos', 'FlapSkew 7 Pos',
                   'FlapSkew 8 Pos']
        dfdr_data = dfdr_data[columns]

        # fix columns name
        col_name = ['AC_Reg', 'FlightNo', 'Date', 'Time', 'Air/Ground', 'Altitude', 'Airspeed', 'Flap_Handle_Pos', 'TE_Flap_Pos_LT',
                    'TE_Flap_Pos_RT', 'TE_Flap_Skew_Pos_1', 'TE_Flap_Skew_Pos_2', 'TE_Flap_Skew_Pos_3', 'TE_Flap_Skew_Pos_4',
                    'TE_Flap_Skew_Pos_5', 'TE_Flap_Skew_Pos_6', 'TE_Flap_Skew_Pos_7', 'TE_Flap_Skew_Pos_8']
        dfdr_data.columns = col_name

        # missing values handling
        col_na = ['TE_Flap_Pos_LT', 'TE_Flap_Pos_RT', 'TE_Flap_Skew_Pos_1', 'TE_Flap_Skew_Pos_2', 'TE_Flap_Skew_Pos_3', 'TE_Flap_Skew_Pos_4',
                  'TE_Flap_Skew_Pos_5', 'TE_Flap_Skew_Pos_6', 'TE_Flap_Skew_Pos_7', 'TE_Flap_Skew_Pos_8']
        dfdr_data[col_na] = dfdr_data[col_na].fillna(
            method='ffill').fillna(method='bfill')

        # fix dfdr_data types
        col_int = []
        col_float = ['Altitude', 'Airspeed', 'Flap_Handle_Pos', 'TE_Flap_Pos_LT', 'TE_Flap_Pos_RT', 'TE_Flap_Skew_Pos_1', 'TE_Flap_Skew_Pos_2',
                     'TE_Flap_Skew_Pos_3', 'TE_Flap_Skew_Pos_4', 'TE_Flap_Skew_Pos_5', 'TE_Flap_Skew_Pos_6', 'TE_Flap_Skew_Pos_7',
                     'TE_Flap_Skew_Pos_8']

        dfdr_data[col_int] = dfdr_data[col_int].astype('int')
        dfdr_data[col_float] = dfdr_data[col_float].astype('float')

        # convert back to csv
        csv_clean = app.config['UPLOAD_FOLDER']+'{registration}_{date}_{flight_no}_cleaned.csv'.format(registration=dfdr_data.loc[1, 'AC_REG'], date=dfdr_data['Date'][0],
                                                                                                       flight_no=dfdr_data['FlightNo'][0])

        dfdr_data.to_csv(csv_clean, index=False)
