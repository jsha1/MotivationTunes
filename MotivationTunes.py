
# coding: utf-8

# In[11]:

import pafy
import sqlite3
import configparser


# In[13]:

config = configparser.ConfigParser()
config.read('config.ini')
playlistIds = config['media']['playlists'].split(',')

#DB_PATH = "/home/jerry/sandbox/youtube-dl/db/"
#MUSIC_PATH = "/home/jerry/sandbox/youtube-dl/tmp/"
DB_PATH = config['paths']['DB_PATH']
MUSIC_PATH = config['paths']['MUSIC_PATH']


# In[14]:

def downloadVideos(valid_pafys, c, conn):
    for pafy in valid_pafys:
        downloadVideo(pafy,c,conn)
        
def deleteAllDB():
    conn = sqlite3.connect(DB_PATH + 'MotivationTunes.db')
    c = conn.cursor()
    c.execute("DELETE FROM FROM video");
    conn.commit()
    conn.close()

def downloadVideo(pafy,c,conn):

    mark(pafy.videoid,c, 'DOWNLOADING')
    conn.commit()
   
    streams = pafy.audiostreams
    valid_streams = (stream for stream in streams if stream.extension in ('mp3','m4a','wma','flac','ogg'))
    chosen = valid_streams.next()
    if chosen:
    
        filename = pafy.title + "_" + pafy.videoid + "." + chosen.extension
        chosen.download(filepath=MUSIC_PATH + filename)
    else:
          markCompleted(pafy.videoid,c,'NO_AUDIO_STREAMS')
          return
    
    markCompleted(pafy.videoid,c,'COMPLETED')
    conn.commit()
  
    print("download complete!")


# In[15]:



def createTableIfNotExists(c):

    def createTable():
            # Create table
        c.execute('''CREATE TABLE
                 video ( 
                  video_id text primary key, 
                  status text,
                  updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                  )''')

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='video'");
    result = c.fetchone()
    if not result:
        createTable()
    
def videoAlreadyProcessed(c,video_id):
    c.execute("SELECT video_id FROM video WHERE video_id = ?", [(video_id)]);
    result = c.fetchone()
    print result
    return result
        
def mark(video_id, c, status):
    
    purchases = [(video_id, status)]
    c.executemany('INSERT INTO video (video_id, status) VALUES (?,?)', purchases)
    #printTable(c)
    
def markCompleted(video_id, c, status):
    
    purchases = [( status, video_id)]
    c.executemany('UPDATE video SET status = ? where video_id = ?', purchases)
    #printTable(c)
    
def printTable(c):
    
    for row in c.execute('SELECT * FROM video'):
        print row

def main():
    conn = sqlite3.connect(DB_PATH + 'MotivationTunes.db')
    c = conn.cursor()
    createTableIfNotExists(c)
    
    print playlistIds

    for playlistId in playlistIds:
        plurl = 'https://www.youtube.com/playlist?list=' + playlistId
        playlist = pafy.get_playlist(plurl)
        valid_pafys = []
        for item in playlist['items']:
            if not videoAlreadyProcessed(c, item['pafy'].videoid):
                valid_pafys.append(item['pafy'])

    print(str(len(valid_pafys)) + " videos to dl")
    downloadVideos(valid_pafys,c,conn)

    conn.close()
    print("completed")
    
        
if __name__ == '__main__':
    main()

        



# In[ ]:



