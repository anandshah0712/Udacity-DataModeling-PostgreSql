# DROP TABLES

song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
user_table_drop = "drop table if exists users"
time_table_drop = "drop table if exists time"
songplays_table_drop = "drop table if exists songplays"

# CREATE TABLES

songplays_table_create = ("""
create table songplays (
    songplay_id SERIAL PRIMARY KEY,
    start_time bigint NOT NULL,
    user_id integer NOT NULL,
    level varchar(10) NOT NULL,
    song_id varchar(25),
    artist_id varchar(25),
    session_id integer NOT NULL,
    location varchar(255) NOT NULL,
    user_agent varchar(255) NOT NULL
)
""")

song_table_create = ("""
create table songs (
    song_id varchar(25) PRIMARY KEY,
    title varchar(255),
    artist_id varchar(25) NOT NULL, 
    year integer NOT NULL,
    duration numeric NOT NULL
)
""")

artist_table_create = ("""
create table artists (
    artist_id varchar(25) PRIMARY KEY, 
    name varchar(255) NOT NULL,
    location varchar(255), 
    latitude varchar(255),
    longitude varchar(255)
)
""")

user_table_create = ("""
create table users (
    user_id integer PRIMARY KEY,
    first_name varchar(255),
    last_name varchar(255), 
    gender varchar(1) NOT NULL,
    level varchar(10) NOT NULL
)
""")

time_table_create = ("""
create table time (
    start_time bigint PRIMARY KEY,
    hour integer NOT NULL,
    day integer NOT NULL, 
    week integer NOT NULL,
    month integer NOT NULL,
    year integer NOT NULL,
    weekday integer NOT NULL
)
""")

# INSERT RECORDS

song_table_insert = (
"""insert into songs(song_id,title,artist_id,year,duration)
values(%s,%s,%s,%s,%s)ON CONFLICT (song_id) 
DO NOTHING""")

artist_table_insert = (
"""insert into artists(artist_id,name,location,latitude,longitude)
values(%s,%s,%s,%s,%s)ON CONFLICT (artist_id) 
DO NOTHING""")

user_table_insert = (
"""insert into users(user_id,first_name,last_name,gender,level)
values(%s,%s,%s,%s,%s)ON CONFLICT (user_id) 
DO UPDATE SET level = users.level""")

time_table_insert = (
"""insert into time(start_time,hour,day,week,month,year,weekday)
values(%s,%s,%s,%s,%s,%s,%s)ON CONFLICT (start_time) 
DO NOTHING""")

songplay_table_insert = (
"""insert into songplays(start_time,user_id,level,song_id,artist_id,session_id,location,user_agent)
values(%s,%s,%s,%s,%s,%s,%s,%s)ON CONFLICT (songplay_id) 
DO NOTHING""")

# SELECT RECORDS

song_select = (
"""
    SELECT s.artist_id, s.song_id 
        FROM songs s
    INNER JOIN artists a
        ON s.artist_id = a.artist_id
    WHERE a.name = %s
        AND s.title = %s
        AND s.duration = %s;
"""
)

# QUERY LISTS

create_table_queries = [song_table_create,artist_table_create,user_table_create,time_table_create,songplays_table_create]
drop_table_queries = [song_table_drop, artist_table_drop,user_table_drop,time_table_drop,songplays_table_drop]
