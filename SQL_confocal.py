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
from utils import get_bin, write_bin
from SQL_abstract import SQL_abstract

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


class SQL_confocal(SQL_abstract):
    """
    This class interacts with the SQL DB , uploads to the DB, creates tables
    in the DB, and extracts information from the DB.
    This is written based on the Query/Content model, in this model we have
    special functions for each type of data file that return a customized
    query and params to be uploaded. This is decorated with the appropriate
    decorator that establishes the connection to the DB, performs the functions,
    and closes the connection.

    The class specific for confocal experiments.
    """


    def __init__(self):
        super().__init__()
        self.data_id = generate_name()
        self.TABLE_NAME = 'data'
        self.read_bin_dir = '..\\exp-data\\'
        self.write_bin_dir = '..\\temp\\'

    @decorator_insert
    def insert(self, filename):

        """
                This function is used to upload log data into the SQL DB.
                :param: Takes class params and set of params to be inserted.
                :type: list
                :rtype: string,list
                :return: returns a query string and a list of contents.
        """

        query = 'INSERT INTO ' + self.TABLE_NAME + '(data_id, bin, filename, time_stamp) ' \
                'VALUES (%s,%s,%s, CURRENT_TIMESTAMP);'
        content = (self.data_id, get_bin(self.read_bin_dir + filename), filename)
        return (query,content)

    @decorator_extract
    def extract(self, data_id=None, key=None, filename=None):

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
        input = [name, key, filename]

        input_strings = [" data_id LIKE %s", " and key = %s", " and filename = %s"]
        query = 'SELECT * FROM ' + self.TABLE_NAME + ' WHERE'
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
        data.filename = [row[3] for row in raw]

        #The follwing writes each binary to a file
        for row in raw:
            write_bin(self.write_bin_dir + row[3], row[2])
        return data


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

    # SQL = SQL_confocal()
    # SQL.insert("13-21-21.txt")

    SQL = SQL_confocal()
    a = SQL.load(key=1)
    print(a.key)
