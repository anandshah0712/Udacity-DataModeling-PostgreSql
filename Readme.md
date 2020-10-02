Summary of the Project 

A) Purpose and Analytical Goals

1. Music streaming company ‘Sparkify’ currently have all their data stored in a directory of JSON logs and therefore there is no easy way 
   to query their data so the purpose of this project is to store the data from these JSON files into relational Postgres database so the 
   data can be queried efficiently through optimized sql queries.
   
2. Major analytical goal of the company is to get a better understanding of the kinds of songs the users are currently listening to as well 
   as the artists that they are following on the music streaming app. 

B) Database Schema design and ETL pipeline.

1. The database schema consists of new database called 'sparkify' which contains 1 fact table and 4 dimension tables as shown below along   
   with their column names. 

a. Fact Table
     songplays - records in log data associated with song plays i.e. records with page NextSong
     columns : songplay_id, start_time, user_id, level, song_id, artist_id, session_id,location, user_agent 

b. Dimension Tables
     users - contains all the users in the music streaming app
     columns : user_id, first_name, last_name, gender, level
     songs - contains all the songs in the music streaming app 
     columns : song_id, title, artist_id, year, duration
     artists - contains all the artists in the music streaming app
     columns : artist_id, name, location, latitude, longitude
     time - timestamps of records in songplays fact table broken down into specific units
     columns : start_time, hour, day, week, month, year, weekday
     
2. ETL pipeline transfers data from JSON files present in two local directories(song_data and log_data) into the above tables in Postgres 
   database using Python Code and SQL Queries.
   
3. ETL consists of below 3 python files which is present in the repository. 
   1.sql_queries.py - this file contains all the sql queries to drop/create the 4 dimension tables and 1 fact table as well  
                      as queries to insert data into the 5 tables. 
   2.create_tables.py - this file contains the below 3 functions which is called by the main() function in the same order as shown below  
     a.create_database()- function is called to connect to the server and drop the sparkify database if it exists and create a new database. 
     b.drop_tables(cur, conn) - function is called to drop the tables.
     c.create_tables(cur, conn) - function is called to create the tables.
   3.etl.py  - this is the main file to perform the ETL and consists of the below 2 functions. 
     a. process_song_file(cur, filepath) - function extracts the data from the 74 json files in song_data folder, performs transformations 
                                           using dataframes and finally loads data into the songs and artists dimension tables
     b. process_log_file(cur, filepath) -  function extracts the data from the 30 json files in log_data folder, performs transformations 
                                           using dataframes and finally loads data into the users and time dimension table as well as the   
                                           songplays fact table.
4. Please follow the below 2 steps in the same order to perform the entire ETL. 
    a. Open the terminal and run the below command to drop/create all the tables.
       Command : python3 create_tables.py
    b. Run the below command to load the data from the JSON files into the dimension/fact tables. 
       Command : python3 etl.py
       
5. Following sql queries can be run in python notebook to validate that the data has been succesfully loaded into the tables. 
   %load_ext sql
   %sql postgresql://student:student@127.0.0.1/sparkifydb
   %sql  SELECT sp.* FROM songplays sp INNER JOIN users a ON sp.user_id = a.user_id LIMIT 5;
   %sql  SELECT sp.* FROM songplays sp INNER JOIN time a ON sp.start_time = a.start_time LIMIT 5;
   %sql  SELECT sp.* FROM songplays sp INNER JOIN songs a ON sp.song_id = a.song_id LIMIT 5;
   %sql  SELECT sp.* FROM songplays sp INNER JOIN artists a ON sp.artist_id = a.artist_id LIMIT 5;
   
