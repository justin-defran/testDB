# Created by Gurudev Dutt <gdutt@pitt.edu> on 2020-07-28
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from pathlib import Path
import functools, logging, random, subprocess
import os, inspect, datetime
import psycopg2 as pg2
import numpy as np
from decorators import decorator_insert
from decorators import decorator_extract

def generate_name():
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    now = (datetime.datetime.now()).strftime("%H-%M-%S")
    name = str(today) + '-' + str(now)

    return name


def list_to_np(inlist):

    out = np.zeros(len(inlist))

    for i in range(0,len(inlist)):
        out[i] = float(inlist[i])

    return out

class Data:
    def __init__(self):
        pass

class SQL_qpulse:
    """
    This class interacts with the SQL DB , uploads to the DB, creates tables
    in the DB, and extracts information from the DB.
    This is written based on the Query/Content model, in this model we have
    special functions for each type of data file that return a customized
    query and params to be uploaded. This is decorated with the appropriate
    decorator that establishes the connection to the DB, performs the functions,
    and closes the connection.

    The class specific for quantum pulse experiments.
    """

    TABLE_NAME = 'qpulse'

    def __init__(self):
        self.data_id = generate_name()

    @decorator_insert
    def insert(self, params1, params):

        """
                This function is used to upload log data into the SQL DB.
                :param: Takes class params and set of params to be inserted.
                :type: list
                :rtype: string,list
                :return: returns a query string and a list of contents.
        """

        query = 'INSERT INTO ' + TABLE_NAME + '(data_id,raw_data0,raw_data1,sample,count_time,reset_time,avg,threshold,AOM_delay,microwave_delay,type' \
                ',start,stepsize,steps,PTS,SRS,avgCount,x_arr,time_stamp) ' \
                'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP)'
        content = (self.data_id,params1[0],params1[1],(params[0])[0],(params[0])[1],(params[0])[2],(params[0])[3],
                   (params[0])[4],(params[0])[5],(params[0])[6],(params[1])['type'],int((params[1])['start']),
                   int((params[1])['stepsize']),int((params[1])['steps']),(str((params[2])['PTS']) )
                    ,(str((params[2])['SRS'])),params[3],params[4])
        return (query,content)

    @decorator_extract
    def extract(self, data_id=None, key=None, sample=None, count_time=None, reset_time=None,
                         avg=None, threshold=None, AOM_delay=None, microwave_delay=None,
                         type=None, start=None, stepsize=None, steps=None, avgCount=None,
                         PTS=None, SRS=None):

        """
                This function is used to extract data from the SQL DB.
                :param: Takes inputs of what you want to search.
                :type: string,list
                :rtype: list
                :return: returns data object.
                |
        """

        if (data_id != None):
            name = data_id + '%'
        else:
            name = None
        content = []
        input = [name, key, sample, count_time, reset_time, avg, threshold, AOM_delay, microwave_delay, type,
                 start, stepsize, steps, avgCount, PTS, SRS]

        input_strings = [" data_id LIKE %s", " and key = %s", " and sample = %s", " and count_time = %s",
                         " and reset_time = %s", " and avg = %s", " and threshold = %s",
                         " and AOM_delay = %s", " and microwave_delay = %s", " and type = %s",
                         " and start = %s", " and stepsize = %s", " and steps = %s", " and avgCount = %s",
                         " and PTS = %s", " and SRS = %s"]
        query = 'SELECT * FROM qpulse WHERE'
        val = True
        for i, j in enumerate(input):

            if (j != None):
                if (input[0] == None and val == True):
                    query = query + input_strings[i][4:]
                    content.append(j)
                    val = False
                    continue
                content.append(j)
                query = query + input_strings[i]

        return (query, content)


    def format(self, raw):
        '''
        Raw is the output of the psycopg2 query, a list of lists of lists etc...
        '''
        data = Data()

        data.key = [row[0] for row in raw]
        data.data_id = [row[1] for row in raw]
        data.rawdata0 = [list_to_np(row[2]) for row in raw]
        data.rawdata1 = [list_to_np(row[3]) for row in raw]
        data.sample = [row[4] for row in raw]
        data.count_time = [row[5] for row in raw]
        data.reset_time = [row[6] for row in raw]
        data.avg = [row[7] for row in raw]
        data.threshold = [row[8] for row in raw]
        data.aom_delay = [row[9] for row in raw]
        data.mw_delay = [row[10] for row in raw]
        data.type = [row[11] for row in raw]
        data.start = [row[12] for row in raw]
        data.stepsize = [row[13] for row in raw]
        data.steps = [row[14] for row in raw]
        data.PTS = [row[15] for row in raw]
        data.SRS = [row[16] for row in raw]
        data.avgCount = [float(row[17]) for row in raw]
        data.x_arr = [row[18] for row in raw]
        data.time_stamp = [row[19] for row in raw]

        return data

    def load(self, **kwargs):
        '''
        Access the data here. Note that extract is defined to have a decorator. After completing the extract method and
        the decorator function, the result is passed through format for final adjustments.

        Kwargs are the searchable parameters.
        '''
        return self.format(self.extract(**kwargs))

    def backup(self):
        folder = str(datetime.datetime.today().strftime("%Y-%m-%d"))
        onedrivepath = "/Users/bmesi/Desktop/Onedrive/OneDrive - University of Pittsburgh/Duttlab/QuantumPulse/"+folder
        filepath = '"'+onedrivepath + "/backup.sql"+'"'
        if not(os.path.exists(onedrivepath)):
            os.makedirs(onedrivepath)

        try:
            subprocess.run('pg_dump -U postgres quantumpulse > ' + filepath,shell = True)
        except:
            print("Terminal Error")

if __name__ == '__main__':

    SQL = SQL_qpulse()
    a = SQL.load(sample=50000)
    print(a.rawdata0)
