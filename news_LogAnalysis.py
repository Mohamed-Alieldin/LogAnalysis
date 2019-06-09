#!/usr/bin/env python3

import psycopg2


# My root function to connect to the database
def run_query(query):
    db_Conn = psycopg2.connect("dbname=news")
    cursor = db_Conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    db_Conn.close()
    return (result)

# Request No.1
# What are the most popular three articles of all time?
query_1 = '''select articles.title , cast (count(log.path) as int )as views from articles
inner join log on articles.slug = split_part(log.path,'/',3)
where split_part(log.path,'/',2) = 'article'
 group by articles.title order by views desc limit 3;'''

popular_articles = run_query(query_1)
print("\n The most popular three articles of all time are:")
for article in popular_articles:
    print(article[0], "{} views".format(article[1]))


# Request No.2
# Who are the most popular article authors of all time?
query_2 = ''' create or replace view count_per_author as
select author, cast(count(log.path) as int )as views from articles
inner join log on articles.slug = split_part(log.path,'/',3)
where split_part(log.path,'/',2) = 'article'
group by author order by views desc;

select authors.name , c.views || ' views' from authors
inner join count_per_author c on authors.id = c.author
order by c.views desc;
'''
popular_authors = run_query(query_2)
print("\n The most popular article authors of all time are:")
for author in popular_authors:
    print(author[0], author[1])

# Request No.3
# On which days did more than 1% of requests lead to errors?
query_3 = '''create or replace  view errors as
select date(time) as day , count(*) as error_requests from log
where status like '%404%'
group by day
order by error_requests desc;

create or replace view requests as
select date(time) as day , count(*) as all_requests from log
group by day
order by all_requests desc;

select to_char(requests.day, 'Mon dd,yyyy'),
round(((100*errors.error_requests::decimal)/requests.all_requests::decimal), 2)
||'% erros' as error_Percentage
from requests
inner join errors on requests.day = errors.day
where ((100*errors.error_requests::decimal)/requests.all_requests) > 1;'''

days = run_query(query_3)
print("\n The days with more than 1% of requests lead to errors are:")
for day in days:
    print(day[0], day[1])
