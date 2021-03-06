# Sparkify Postgres ETL

This is third project for data engineering nanodegree at udacity. 
In this project, the following concepts were applied:
- Data Warehouses On AWS
- Build an ETL pipeline for a database hosted on Redshift

## Context

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

### Data
- song data: stored under data/song_data, each file is in JSON format and contains metadata about a song and the artist of that song. Sample song data looks like:
```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```
- log data: The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. Sample log data looks like:
```
{"artist":"Slipknot","auth":"Logged In","firstName":"Aiden","gender":"M","itemInSession":0,"lastName":"Ramirez","length":192.57424,"level":"paid","location":"New York-Newark-Jersey City, NY-NJ-PA","method":"PUT","page":"NextSong","registration":1540283578796.0,"sessionId":19,"song":"Opium Of The People (Album Version)","status":200,"ts":1541639510796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"20"}
```

## Project Structure
data files are store in AWS S3 buckets, the project workspace includes five files:

1. create_tables.py where you'll create your fact and dimension tables for the star schema in Redshift.
2. etl.py where you'll load data from S3 into staging tables on Redshift and then process that data into your analytics tables on Redshift.
3. sql_queries.py where you'll define you SQL statements, which will be imported into the two other files above.
4. create_cluster.ipynb Infrastructure as Code file where you'll use python to create a redshift cluster
5. test.ipynb test code for the database
6. README.md provides discussion on your project.

## How to Run
1. Read configuration from dwh.cfg which contains configuration of your AWS, it looks like this:
```
[CLUSTER]
host = 
db_name = dwhproject
db_user = dwhuser
db_password = Passw0rd
db_port = 5439

[IAM_ROLE]
arn = 

[S3]
log_data = 's3://udacity-dend/log_data'
log_jsonpath = 's3://udacity-dend/log_json_path.json'
song_data = 's3://udacity-dend/song_data'

[AWS]
key = 
secret = 

[DWH]
dwh_cluster_type = multi-node
dwh_num_nodes = 4
dwh_node_type = dc2.large
dwh_iam_role_name = dwhRole
dwh_cluster_identifier = dwhCluster
```
2. Run the following in terminal to create table
```
python create_table.py
```

3. Run the following in terminal to fill table
```
python etl.py
```

4. If nothing pops up, which means success, then we can run some query in jupyter notebook to test it

## Project Steps
**Create Tables**
1. Design schemas for your fact and dimension tables
2. Write a SQL CREATE statement for each of these tables in sql_queries.py
3. Complete the logic in create_tables.py to connect to the database and create these tables
4. Write SQL DROP statements to drop tables in the beginning of create_tables.py if the tables already exist. This way, you can run create_tables.py whenever you want to reset your database and test your ETL pipeline.
5. Launch a redshift cluster and create an IAM role that has read access to S3.
6. Add redshift database and IAM role info to dwh.cfg.
7. Test by running create_tables.py and checking the table schemas in your redshift database. You can use Query Editor in the AWS Redshift console for this.

**ETL Process**

1. Implement the logic in etl.py to load data from S3 to staging tables on Redshift.
2. Implement the logic in etl.py to load data from staging tables to analytics tables on Redshift.
3. Test by running etl.py after running create_tables.py and running the analytic queries on your Redshift database to compare your results with the expected results.
4. Delete your redshift cluster when finished.

