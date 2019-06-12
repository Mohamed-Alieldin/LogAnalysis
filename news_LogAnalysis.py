#!/usr/bin/env python3

import psycopg2
import sys


def db_connect(db):
    """
    Create and return a database connection.

    The functions creates and returns a database connection to the
    database defined by DBNAME.
    """
    try:
        conn = psycopg2.connect(db)
        return conn
    except psycopg2.error as e:
        print("Unable to connect to the database")
        print(e.pgerror)
        print(e.diag.message_detail)
        sys.exit(1)


def execute_query(query, connection):
    """
    execute_query returns the results of an SQL query.

    execute_query takes an SQL query as a parameter and the db connection,
    creates a db cursor and
    executes the query and returns the results as a list of tuples.
    args:
    query - an SQL query statement to be executed.
    connection - a db connection to create the db cursor

    returns:
    A list of tuples containing the results of the query.
    """
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return (results)


def print_top_articles(connection):
    """
    Print out the top 3 articles of all time.
    args:
    connection - a db connection to be used in calling
     the query execution function
    """
    query = '''
    select articles.title , count(log.path) as views from articles
    inner join log on articles.slug = split_part(log.path,'/',3)
    where split_part(log.path,'/',2) = 'article'
    group by articles.title order by views desc limit 3;'''
    results = execute_query(query, connection)
    print("\n The most popular three articles of all time are:")
    for title, views in results:
        element = "\"{}\" with {} views".format(title, views)
        print(element)


def print_top_authors(connection):
    """
    Print a list of authors ranked by article views.
    args:
    connection - a db connection to be used in calling
     the query execution function
    """
    query = '''
    select authors.name , c.views || ' views' from authors
    inner join count_per_author c on authors.id = c.author
    order by c.views desc;
    '''
    results = execute_query(query, connection)
    print("\n The most popular article authors of all time are:")
    for author, views in results:
        element = "\"{}\" with {}".format(author, views)
        print(element)


def print_errors_over_one(connection):
    """
    Print out the error report.

    This function prints out the days and that day's error percentage where
    more than 1% of logged access requests were errors.
    args:
    connection - a db connection to be used in calling
     the query execution function
    """
    query = '''
    select to_char(requests.day, 'Mon dd,yyyy'),
    round(((100*errors.error_requests::decimal)/requests.all_requests
    ::decimal), 2)||'% erros' as error_Percentage
    from requests
    inner join errors on requests.day = errors.day
    where ((100*errors.error_requests::decimal)/requests.all_requests) > 1;
    '''
    results = execute_query(query, connection)
    print("\n The days with more than 1% of requests lead to errors are:")
    for day, percentage in results:
        element = "{} with {}".format(day, percentage)
        print(element)

if __name__ == '__main__':
    DBNAME = "dbname=news"
    conn = db_connect(DBNAME)
    print_top_articles(conn)
    print_top_authors(conn)
    print_errors_over_one(conn)
    conn.close()
