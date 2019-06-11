create or replace view count_per_author as
select author, cast(count(log.path) as int )as views from articles
inner join log on articles.slug = split_part(log.path,'/',3)
where split_part(log.path,'/',2) = 'article'
group by author order by views desc;

create or replace  view errors as
select date(time) as day , count(*) as error_requests from log
where status like '%404%'
group by day
order by error_requests desc;

create or replace view requests as
select date(time) as day , count(*) as all_requests from log
group by day
order by all_requests desc;