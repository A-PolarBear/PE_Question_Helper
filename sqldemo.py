import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",       # 数据库主机地址
  user="root",    # 数据库用户名
  passwd="10356",   # 数据库密码
)

mycursor = mydb.cursor()
 
# mycursor.execute("CREATE DATABASE Questions")

sql = "DROP TABLE IF EXISTS sites"  # 删除数据表 sites
 
mycursor.execute(sql)


# print(mydb)