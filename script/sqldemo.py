import sqlite3

def create(c):
    c.execute('''CREATE TABLE QUESTIONS
       (ISSUE TEXT NOT NULL,
        CHOICE TEXT ,
        ANSWER TEXT NOT NULL,
        PRIMARY KEY(ISSUE,CHOICE,ANSWER));''')
    print ("数据表创建成功")

conn = sqlite3.connect('question.db')
print ("Database is ready!")
c = conn.cursor()
# create(c)
s="晚餐前___小时进行运动效果最好"
c.execute("SELECT count(*) FROM QUESTIONS")
# x = c.execute("SELECT * FROM QUESTIONS  where issue like '%五连冠%'")
# c.execute("DELETE FROM QUESTIONS")
# c.execute("DROP TABLE QUESTIONS")
print(c.fetchall())
# print(x.fetchall())
conn.commit()
conn.close()