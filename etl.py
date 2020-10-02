import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    
    """
    The function loops through all the JSON files in song_data folder and loads data into python dataframe.
    """
    
    # open song file
    df = pd.read_json(filepath,lines=True)

    # insert song record
    song_data = pd.DataFrame(df, columns= ['song_id', 'title','artist_id','year','duration'])
    song_data = song_data.values
    song_data = song_data.tolist()
    song_data = song_data[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = pd.DataFrame(df, columns= ['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']) 
    artist_data = artist_data.values
    artist_data = artist_data.tolist()
    artist_data = artist_data[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
       
    """
    The function loops through all the JSON files in log_data folder and loads data into python dataframe.
    """
    
    # open log file
    df = pd.read_json(filepath,lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.DataFrame(df, columns= ['ts']) 
    t1 = pd.DataFrame(df, columns= ['ts']) 
    t['ts'] = pd.to_datetime(t['ts'],unit = 'ms')
    
    # insert time data records
    time_data = pd.DataFrame(t1, columns= ['ts'])
    time_data['hour'] = t.ts.dt.hour
    time_data['day'] = t.ts.dt.day
    time_data['weekofyear'] = t.ts.dt.week
    time_data['month'] = t.ts.dt.month
    time_data['year'] = t.ts.dt.year
    time_data['weekday'] = t.ts.dt.weekday
    time_data = time_data.values.tolist()
    column_labels = ['ts','hour','day','weekofyear','month','year','weekday']
    time_df = pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = pd.DataFrame(df, columns= ['userId', 'firstName','lastName','gender','level'])
    user_df = user_df.dropna()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts,row.userId,row.level,songid,artistid,row.sessionId,row.location,row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    
    """
    Calls function : process_song_file to process all the files in song_data folder and function : process_log_file to process all the files in 
    log_data folder 
    """
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    print(process_song_file.__doc__)
    process_data(cur, conn, filepath='data/song_data', func=process_song_file) 
    
    print(process_log_file.__doc__)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
