# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS user_table"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create =("""CREATE TABLE IF NOT EXISTS songplay (songplay_id int Primary key,\
                                                                start_time varchar,\
                                                                user_id int NOT NULL,\
                                                                level varchar NOT NULL,\
                                                                song_id varchar NOT NULL,\
                                                                artist_id varchar NOT NULL,\
                                                                session_id int NOT NULL,\
                                                                location varchar,\
                                                                user_agent varchar)""")

user_table_create =("""CREATE TABLE IF NOT EXISTS user_table (user_id int PRIMARY KEY,\
                                                        first_name varchar NOT NULL,\
                                                        last_name varchar NOT NULL,\
                                                        gender varchar,\
                                                        level varchar NOT NULL)""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS song (song_id varchar PRIMARY KEY,\
                                                        title varchar NOT NULL,\
                                                        artist_id varchar NOT NULL,\
                                                        year int,\
                                                        duration float)""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artist_table (artist_id varchar PRIMARY KEY,\
                                                                    name varchar NOT NULL,\
                                                                    location varchar,\
                                                                    latitude float,\
                                                                    longitude float)""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (start_time varchar PRIMARY KEY,\
                                                        hour int,\
                                                        day int,\
                                                        week int,\
                                                        month int,\
                                                        year int,\
                                                        weekday int)""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplay (songplay_id,start_time,user_id,level,song_id,artist_id,session_id,location,user_agent) \
                            values(%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (songplay_id) DO NOTHING
""")

user_table_insert = ("""INSERT INTO user_table (user_id,first_name,last_name,gender,level) values(%s,%s,%s,%s,%s) ON CONFLICT (user_id) DO UPDATE \
                            set level = EXCLUDED.level
""")

song_table_insert = ("""INSERT INTO song (song_id,title,artist_id,year,duration) values(%s,%s,%s,%s,%s) ON CONFLICT (song_id) DO NOTHING
""")

artist_table_insert = ("""INSERT INTO artist_table (artist_id,name,location,latitude,longitude) values(%s,%s,%s,%s,%s) ON CONFLICT (artist_id) DO NOTHING
""")


time_table_insert = ("""INSERT INTO time (start_time,hour,day,week,month,year,weekday) values(%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (start_time) DO NOTHING
""")

# FIND SONGS

song_select = ("""Select song.song_id,artist_table.artist_id from song join artist_table on song.artist_id=artist_table.artist_id where song.title = %s and artist_table.name=%s and song.duration=%s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]