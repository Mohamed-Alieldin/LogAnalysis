
Running The APP:
	you can run the app by placing the source code 'news_LogAnalysis' in the virtual environment where the database is created
	and then run the line python news_LogAnalysis.py after logging in the virtual environment.

	


Design
The code is divided into four parts:
	1. A root function named run_query to connect to the database. It takes the query string as input and returns the result.
	   Each query in the upcoming parts should call this function to connect to the database.
	2. Request number one part in which it includes the query to answer the first question and the results display.
	3. Request number two in which it includes the query to answer the second question and the results display.
	4. Request number three in which it includes the query to answer the third question and the results display.

The Views:
The code creates three views in the database, the source code includes the queries to create them
you will not need to run them prior to running the tool. However, running them before running the tool will result in no errors.
The views statements are as following:

1. "create or replace view count_per_author as
select author, cast(count(log.path) as int )as views from articles
inner join log on articles.slug = split_part(log.path,'/',3)
where split_part(log.path,'/',2) = 'article'
group by author order by views desc;"

2. "create or replace  view errors as
select date(time) as day , count(*) as error_requests from log
where status like '%404%'
group by day
order by error_requests desc;"

3."create or replace view requests as
select date(time) as day , count(*) as all_requests from log
group by day
order by all_requests desc;"