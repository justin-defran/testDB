from abc import ABC, abstractmethod

class SQL_abstract(ABC):
    '''
    A class, specific to each table in the database, which establishes an "uplink-downlink" connection for data saving
    and retrieval.
    '''

    def __init__(self):
        pass

    def insert(self):
        '''
        The arguments should be all the stuff you want to save in the database. One argument for insert() corresponds to
        one column in the database. Outputs a (query,content) tuple. Should be wrapped by the insert_decorator.
        '''
        pass

    def extract(self):
        '''
        The arguments should be the keyword arguments that you want to be searchable. Outputs a (query,content) tuple.
        Should be wrapped by the extract_decorator.
        '''
        pass

    def format(self):
        '''
        The argument should be a data class. Do whatever you want in this method to get the data looking as you want it.
        The output should be your formatted data.
        '''
        pass

    def load(self, **kwargs):
        '''
        Access the data here. Note that extract is defined to have a decorator. After completing the extract method and
        the decorator function, the result is passed through format for final adjustments.

        Kwargs are the searchable parameters.
        '''
        return self.format(self.extract(**kwargs))
