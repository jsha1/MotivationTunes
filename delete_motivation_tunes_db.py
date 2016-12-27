
# coding: utf-8

# In[3]:

import sqlite3
import sys


# In[5]:

DB_PATH = "/storage/emulated/0/qpython/scripts/motivationtunes/db/"    
    
def deleteAllDB():
    conn = sqlite3.connect(DB_PATH + 'MotivationTunes.db')
    c = conn.cursor()
    c.execute("DELETE FROM video where video_id in ('')");
    conn.commit()
    conn.close()

    
        
if __name__ == '__main__':
    deleteAllDB()

        


# In[ ]:



