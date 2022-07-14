from pathlib import Path
import functools, logging, random, subprocess
import os, inspect, datetime
import psycopg2 as pg2
import numpy as np
from .config import config

(database, user, password) = config()

def decorator_insert(original_function):
    """
This function is a decorator for any function that would insert data
into the DB and is designed in the Query/Content
    """

    @functools.wraps(original_function)
    def wrapper_function(*args, **kwargs):
        query, content = original_function(*args, **kwargs)
        conn = pg2.connect(database=database, user=user, password=password)
        cur = conn.cursor()
        executable = cur.mogrify(query, content)
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
        conn = pg2.connect(database=database, user=user, password=password)
        cur = conn.cursor()
        executable = cur.mogrify(a, b)
        cur.execute(executable)
        data = cur.fetchall()
        conn.close()

        return data

    return wrapper_function

def decorator_table_insert(original_function):
    """
This function is a decorator for any function that would insert data
into the DB and is designed in the Query/Content
    """

    @functools.wraps(original_function)
    def wrapper_function(*args, **kwargs):
        query = original_function(*args, **kwargs)
        conn = pg2.connect(database=database, user=user, password=password)
        cur = conn.cursor()
        executable = cur.mogrify(query)
        cur.execute(executable)
        conn.commit()
        conn.close()

    return wrapper_function