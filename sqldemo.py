import sqlite3

def create(c):
    c.execute('''CREATE TABLE QUESTIONS
       (ID INTEGER PRIMARY KEY,
        ISSUE TEXT NOT NULL,
        CHOICE TEXT ,
        ANSWER TEXT NOT NULL);''')
    print ("数据表创建成功")

conn = sqlite3.connect('question.db')
print ("Database is ready!")
c = conn.cursor()
# create(c)
c.execute("SELECT * FROM QUESTIONS")
# c.execute("DELETE FROM QUESTIONS")
print(c.fetchall())
conn.commit()
conn.close()