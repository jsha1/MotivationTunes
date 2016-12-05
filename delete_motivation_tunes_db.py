
# coding: utf-8

# In[3]:

import sqlite3


# In[5]:

DB_PATH = "/storage/emulated/0/qpython/motivationtunes/db/"    
    
def deleteAllDB():
    conn = sqlite3.connect(DB_PATH + 'MotivationTunes.db')
    c = conn.cursor()
    c.execute("DELETE FROM video");
    conn.commit()
    conn.close()

    
        
if __name__ == '__main__':
    deleteAllDB()

        


# In[ ]:



