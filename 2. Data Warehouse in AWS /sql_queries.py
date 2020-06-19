import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events_table"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_song_table"
songplay_table_drop = "DROP TABLE IF EXISTS songplay_table"
user_table_drop = "DROP TABLE IF EXISTS user_table"
song_table_drop = "DROP TABLE IF EXISTS song_table"
artist_table_drop = "DROP TABLE IF EXISTS artist_table"
time_table_drop = "DROP TABLE IF EXISTS time_table"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events_table
                                    (artist varchar,
                                    auth varchar,
                                    firstName varchar,
                                    gender varchar,
                                    itemInSession int,
                                    lastName varchar,
                                    length float,
                                    level varchar,
                                    location varchar,
                                    method varchar,
                                    page varchar,
                                    registration float,
                                    sessionId int,
                                    song varchar,
                                    status int,
                                    ts timestamp,
                                    userAgent varchar,
                                    userId int)""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_song_table
                                (num_songs int,
                                artist_id varchar,
                                artist_latitude float,
                                artist_longitude float,
                                artist_location varchar,
                                artist_name varchar,
                                song_id varchar,
                                title varchar,
                                duration float,
                                year int)""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplay_table
                            (songplay_id int identity(0,1) primary key,
                            start_time varchar  SORTKEY,
                            user_id int NOT NULL,
                            level varchar NOT NULL,
                            song_id varchar NOT NULL DISTKEY,
                            artist_id varchar NOT NULL,
                            session_id int NOT NULL,
                            location varchar,
                            user_agent varchar)""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS user_table
                        (user_id int SORTKEY PRIMARY KEY,
                        first_name varchar NOT NULL,
                        last_name varchar NOT NULL,
                        gender varchar,
                        level varchar NOT NULL)""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS song_table
                        (song_id varchar DISTKEY PRIMARY KEY,
                        title varchar NOT NULL,
                        artist_id varchar NOT NULL,
                        year int,
                        duration float)""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artist_table
                        (artist_id varchar PRIMARY KEY,
                        name varchar NOT NULL,
                        location varchar,
                        latitude float,
                        longitude float)""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time_table
                        (start_time timestamp SORTKEY PRIMARY KEY,
                        hour int,
                        day int,
                        week int,
                        month int,
                        year int,
                        weekday int)""")

# STAGING TABLES

staging_events_copy = ("""copy staging_events_table from {bucket_path} 
                          credentials 'aws_iam_role={role_arn}'
                          region 'us-west-2'
                          format as JSON {json_path}
                          timeformat as 'epochmillisecs';
""").format(bucket_path=config['S3']['LOG_DATA'],role_arn = config['IAM_ROLE']['ARN'],json_path=config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""copy staging_song_table from {bucket_path} 
                          credentials 'aws_iam_role={role_arn}'
                          region 'us-west-2'
                          COMPUPDATE OFF
                          TIMEFORMAT as 'epochmillisecs'
                          TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
                          FORMAT AS JSON 'auto';
""").format(bucket_path=config['S3']['SONG_DATA'],role_arn = config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplay_table(start_time,user_id,level,song_id,artist_id,session_id,location,user_agent)
                            SELECT e.ts as start_time,
                            e.userID as user_id,
                            e.level as level,
                            s.song_id as song_id,
                            s.artist_id as artist_id,
                            e.sessionId as session_id,
                            e.location as location,
                            e.userAgent as user_agent 
                            FROM staging_events_table e
                            JOIN staging_song_table s ON (e.song=s.title AND e.artist=s.artist_name)
                            WHERE e.userId is NOT NULL AND e.level is NOT NULL AND s.song_id is NOT NULL AND s.artist_id is NOT NULL
                            AND e.sessionId is NOT NULL AND e.page='NextSong';
""")

user_table_insert = ("""INSERT INTO user_table(user_id,first_name,last_name,gender,level)
                        SELECT DISTINCT(userId), firstName as first_name, lastName as last_name, gender,level
                        FROM staging_events_table  WHERE userId is NOT NULL AND page='NextSong';
""")

song_table_insert = ("""INSERT INTO song_table(song_id,title,artist_id,year,duration)
                        SELECT DISTINCT(song_id),title,artist_id,year,duration
                        FROM staging_song_table  WHERE song_id is NOT NULL;
""")

artist_table_insert = ("""INSERT INTO artist_table(artist_id,name,location,latitude,longitude)
                          SELECT DISTINCT(artist_id),
                          artist_name as name,
                          artist_location as location,
                          artist_latitude as latitude,
                          artist_longitude as longitude
                          FROM staging_song_table WHERE artist_name is NOT NULL AND artist_id is NOT NULL;
""")

time_table_insert = ("""INSERT INTO time_table(start_time,hour,day,week,month,year,weekday)
                        SELECT DISTINCT(ts) as start_time, EXTRACT(hour FROM ts) as hour, EXTRACT(day FROM ts) as day,
                        EXTRACT(week FROM ts) as week, EXTRACT(month FROM ts) as month, EXTRACT(year FROM ts) as year,
                        EXTRACT(dayofweek FROM ts) as weekday
                        FROM staging_events_table WHERE page = 'NextSong';
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
