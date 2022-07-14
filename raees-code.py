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

def get_project_root() -> Path: # new feature in Python 3.x i.e. annotations
    """Returns project root folder."""
    return Path(__file__).parent.parent

#
#
# rootdir = get_project_root()
# logfiledir = rootdir / 'logs/'
# if not logfiledir.exists():
#     os.mkdir(logfiledir)
#     print('Creating directory for logging at:'.format(logfiledir.resolve()))
# logging.basicConfig()
# log = logging.getLogger('custom_log')
# log.setLevel(logging.DEBUG)
# log.info('ciao')

def generate_name():
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    now = (datetime.datetime.now()).strftime("%H-%M-%S")
    name = str(today) + '-' + str(now)

    return name

def get_module_name():
    fname = inspect.stack()[-1].filename
   #print(fname)
    p = Path(fname)
    return p.parts[-1].split('.')[0]


def create_logger(loggername):
    rootdir = get_project_root()
    logfiledir = rootdir / 'logs/'
    if not logfiledir.exists():
        os.mkdir(logfiledir)
        print('Creating directory for logging at:'.format(logfiledir.resolve()))

    log = logging.getLogger(loggername)
    log.setLevel(logging.DEBUG)
    # create a file handler that logs even debug messages
    fh = logging.FileHandler((logfiledir / str(loggername+ '.log')).resolve())
    fh.setLevel(logging.DEBUG)
    # create a console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    log.addHandler(fh)
    log.addHandler(ch)
    return log


# this code is adapted from https://wiki.python.org/moin/PythonDecoratorLibrary#Logging_decorator_with_specified_logger_
# .28or_default.29


class log_with(object):
    '''Logging decorator that allows you to log with a specific logger.
    '''
    # Customize these messages
    ENTRY_MESSAGE = 'Entering {}'
    EXIT_MESSAGE = 'Exiting {}'

    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, func):
        '''Returns a wrapper that wraps func. The wrapper will log the entry and exit points of the function
        with logging.INFO level.
        '''
        # set logger if it was not set earlier
        if not self.logger:
            #logging.basicConfig()
            modname = get_module_name() #func.__module__
            self.logger = create_logger(modname)
            # self.logger = logging.getLogger(modname)
            # self.logger.setLevel(logging.DEBUG)
            # # create a file handler that logs info messages
            # fh = logging.FileHandler((logfiledir / str(modname + '.log')).resolve())
            # fh.setLevel(logging.INFO)
            # # create a console handler with a higher log level
            # ch = logging.StreamHandler()
            # ch.setLevel(logging.ERROR)
            # # create formatter and add it to the handlers
            # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            # fh.setFormatter(formatter)
            # ch.setFormatter(formatter)
            # # add the handlers to the logger
            # self.logger.addHandler(fh)
            # self.logger.addHandler(ch)

        @functools.wraps(func)
        def wrapper(*args, **kwds):
            self.logger.info(self.ENTRY_MESSAGE.format(func.__name__))  # logging level .info(). Set to .debug() if you want to
            f_result = func(*args, **kwds)
            self.logger.info(self.EXIT_MESSAGE.format(func.__name__))   # logging level .info(). Set to .debug() if you want to
            return f_result
        return wrapper

class Data:
  def __init__(self, data):
    self.key = [row[0] for row in data]
    self.data_id = [row[1] for row in data]
    self.rawdata0 = [row[2] for row in data]
    self.rawdata1 = [row[3] for row in data]
    self.sample = [row[4] for row in data]
    self.count_time = [row[5] for row in data]
    self.reset_time = [row[6] for row in data]
    self.avg = [float(row[7]) for row in data]
    self.threshold = [row[8] for row in data]
    self.aom_delay = [row[9] for row in data]
    self.mw_delay = [row[10] for row in data]
    self.type = [row[11] for row in data]
    self.start = [row[12] for row in data]
    self.stepsize = [row[13] for row in data]
    self.steps = [row[14] for row in data]
    self.PTS = [row[15] for row in data]
    self.SRS = [row[16] for row in data]
    self.avgCount = [float(row[17]) for row in data]
    self.x_arr = [row[18] for row in data]
    self.time_stamp = [row[19] for row in data]

class SQL:
    """
    This class interacts with the SQL DB , uploads to the DB, creates tables
    in the DB, and extracts information from the DB.
    This is written based on the Query/Content model, in this model we have
    special functions for each type of data file that return a customized
    query and params to be uploaded. This is decorated with the appropriate
    decorator that establishes the connection to the DB, performs the functions,
    and closes the connection.
    """

    def __init__(self):

        self.data_id = generate_name()


    def decorator_insert(original_function):
        """
    This function is a decorator for any function that would insert data
    into the DB and is designed in the Query/Content
        """

        @functools.wraps(original_function)
        def wrapper_function(*args,**kwargs):
            query,content = original_function(*args,**kwargs)
            conn = pg2.connect(database='DuttlabDB', user='postgres', password='duttlab')
            cur = conn.cursor()
            executable = cur.mogrify(query,content)
            cur.execute(executable)
            conn.commit()
            conn.close()
        return wrapper_function

    def decorator_extract(original_function):
        """
    This function is a decorator for any function that would extract data
    into the DB and is designed in the Query/Content
    |
        """

        @functools.wraps(original_function)
        def wrapper_function(*args, **kwargs):
            a, b = original_function(*args, **kwargs)
            conn = pg2.connect(database='DuttlabDB', user='postgres', password='duttlab')
            cur = conn.cursor()
            executable = cur.mogrify(a, b)
            cur.execute(executable)
            data = cur.fetchall()
            conn.close()

            return Data(data)

        return wrapper_function

    @decorator_insert
    def SQL_data(self,params1,params):

        """
                This function is used to upload log data into the SQL DB.
                :param: Takes class params and set of params to be inserted.
                :type: list
                :rtype: string,list
                :return: returns a query string and a list of contents.
        """

        query = 'INSERT INTO qpulse(data_id,raw_data0,raw_data1,sample,count_time,reset_time,avg,threshold,AOM_delay,microwave_delay,type' \
                ',start,stepsize,steps,PTS,SRS,avgCount,x_arr,time_stamp) ' \
                'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP)'
        content = (self.data_id,params1[0],params1[1],(params[0])[0],(params[0])[1],(params[0])[2],(params[0])[3],
                   (params[0])[4],(params[0])[5],(params[0])[6],(params[1])['type'],int((params[1])['start']),
                   int((params[1])['stepsize']),int((params[1])['steps']),(str((params[2])['PTS']) )
                    ,(str((params[2])['SRS'])),params[3],params[4])
        return (query,content)

    @decorator_insert
    def insert_random_data(self):

        """
                This function is used to upload log data into the SQL DB.
                :param: Takes class params and set of params to be inserted.
                :type: list
                :rtype: string,list
                :return: returns a query string and a list of contents.
        """

        query = 'INSERT INTO qpulse(data_id,raw_data0,raw_data1,sample,count_time,reset_time,avg,threshold,AOM_delay,microwave_delay,type' \
                ',start,stepsize,steps,PTS,SRS,avgCount,x_arr,time_stamp) ' \
                'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP)'
        content = (self.data_id, np.random.randint(0,10), 'asdf', np.random.rand(5), np.random.rand(5), np.random.rand(), np.random.rand(),
                   np.random.rand(), np.random.rand(), np.random.rand(), np.random.rand(), np.random.rand(),
                   np.random.rand(), np.random.rand(), 'asfd','asdf', np.random.rand(), np.random.randint(0,10))
        return (query, content)


    @decorator_insert
    def SQL_seq_test_data(self,params,data):

        """
                        This function is used to upload data into the SQL DB from the sequence_test file.
                        :param: Takes class params and set of params to be inserted.
                        :type: list
                        :rtype: string,list
                        :return: returns a query string and a list of contents.
                """
        query = 'INSERT INTO qpulse(data_id,amplitude,pulsewidth,sb_freq,iq_scale_factor,phase,' \
                'skew_phase,num_pulses,seq,s_wavedata0,s_wavedata1,s_c1markerdata,s_c2markerdata,tt,time_stamp)' \
                ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,' \
                '%s,CURRENT_TIMESTAMP)'
        content = (self.data_id,params["amplitude"], params["pulsewidth"], params["SB freq"],
                   params["IQ scale factor"], params["phase"], params["skew phase"],
                   params["num pulses"], str(data[0]),data[1], data[2],
                   data[3],data[4],data[5])
        return (query,content)

    @decorator_extract
    def SQL_extract_data(data_id=None, key=None, sample=None, count_time=None, reset_time=None,
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

    def test(self):
        parameters = [50000, 300, 2000, 10, 10, 820, 10]
        scan = dict([('type', 'amplitude'), ('start', '0'), ('stepsize', '50'), ('steps', '20')])
        mw = {'PTS': [True, '2.870', False, '2.840', '0.001', '100', '2.940'], 'SRS':
            [False, '2.870', False, '2.840', '0.001', '100', '2.940']}
        avgCount = 50

        rawdata0 = [random.randint(1, 1000) for item in range(10)]
        rawdata1 = [random.randint(1, 1000) for item in range(10)]
        x_arr = [x for x in range(3)]

        rawdata = [rawdata0, rawdata1]
        logdata = [parameters, scan, mw, avgCount, x_arr]

        SQL().SQL_data(rawdata,logdata)

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

    # a = SQL.SQL_extract_data(sample=50000)
    # print(a.avg)

    a = SQL()
    for i in range(0, 10):
        a.test()
