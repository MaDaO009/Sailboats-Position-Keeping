import pymysql
db = pymysql.connect("192.168.0.105","root","root","star")
print('!!')
cursor = db.cursor()
print('Data base Connected')