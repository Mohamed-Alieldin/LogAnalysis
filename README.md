
# Log Analysis - Udacity
### Full Stack Web Development Nano Degree
_______________________
## About
This project is part of the full stack web development nano degree on Udacity. It represents a tool that will use information from the database to discover what kind of articles the site's readers like for a newspaper site.

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, your code will answer questions about the site's user activity.

The reporting tool should answer three questions which are:
1. **What are the most popular three articles of all time?** Which articles have been accessed the most? 
2. **Who are the most popular article authors of all time?** That is, when you sum up all of the articles each author has written, which authors get the most page views?
3. **On which days did more than 1% of requests lead to errors?**

## Prerequisites
* Python 3 [Download it from python.org.](https://www.python.org/downloads/)
* VirtualBox 3 [You can download it from virtualbox.org, here.](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
* Vagrant [Download it from vagrantup.com.](https://www.vagrantup.com/downloads.html)

## Installation

#### Download the VM configuration
There are a couple of different ways you can download the VM configuration:

You can download and unzip this file: [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) This will give you a directory called **FSND-Virtual-Machine**. It may be located inside your **Downloads** folder.

Note: If you are using Windows OS you will find a Time Out error, to fix it use the new [Vagrant file configuration](https://s3.amazonaws.com/video.udacity-data.com/topher/2019/March/5c7ebe7a_vagrant-configuration-windows/vagrant-configuration-windows.zip) to replace you current Vagrant file.

Alternately, you can use Github to fork and clone the repository [https://github.com/udacity/fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm).

Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with `cd`. Inside, you will find another directory called **vagrant**. Change directory to the **vagrant** directory.

#### Start the virtual machine
From your terminal, inside the **vagrant** subdirectory, run the command `vagrant up`. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

When `vagrant up` is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your newly installed Linux VM!

#### Running the database
The PostgreSQL database server will automatically be started inside the VM. You can use the `psql` command-line tool to access it and run SQL statements.

#### Download the Data
[Download the data here.](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) You will need to unzip this file after downloading it. The file inside is called `newsdata.sql`. Put this file into the `vagrant` directory, which is shared with your virtual machine.

 To build the reporting tool, you'll need to load the site's data into your local database.
 `cd` into the `vagrant` directory and use the command `psql -d news -f newsdata.sql`.
 Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.

**Exploring the data**
The database includes three tables:
+ The `authors` table includes information about the authors of articles.
+ The `articles` table includes the articles themselves.
+ The `log` table includes one entry for each time a user has accessed the site.

You can connect to your database using `psql -d` news and explore the tables using the `\dt` and `\d` table commands and `select` statements.

## Running The APP
1. Make sure to log into the VM as described above.
2. Place your source code in the `vagrant` directory.
3. Use the command `python <yourFileName.py>`

	


## Code Design
The code is includes four parts:
1. A root function named run_query to run queries in the database. It takes the query string and the connection as inputs and returns the result.
Each query in the upcoming parts should call this function to connect to the database.
2. Request number one part in which it includes the query to answer the first question and the results display.
3. Request number two in which it includes the query to answer the second question and the results display.
4. Request number three in which it includes the query to answer the third question and the results display.

#### Database Views
The code creates three views in the database, the source code includes the queries to create them
you will not need to run them prior to running the tool. However, running them before running the tool will result in no errors.

The views statements are as the following:
+ `count_per_author` view 
```SQL
create or replace view count_per_author as
select author, cast(count(log.path) as int )as views from articles
inner join log on articles.slug = split_part(log.path,'/',3)
where split_part(log.path,'/',2) = 'article'
group by author order by views desc;
```

+ `errors` view
```SQL
create or replace  view errors as
select date(time) as day , count(*) as error_requests from log
where status like '%404%'
group by day
order by error_requests desc;
```

+ requests view
``` SQL
create or replace view requests as
select date(time) as day , count(*) as all_requests from log
group by day
order by all_requests desc;
```