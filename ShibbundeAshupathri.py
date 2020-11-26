import mysql.connector
Password=input("ENTER PASSWORD- ")
con=mysql.connector.connect(host="localhost",user="root",password=Password,database="shibbunde_ashupathri")
cur=con.cursor()
cur.execute("create table if not exists Hospital_Log(Patient_Number int(4) primary key,\
	Patient_Name varchar(20),CPR_Number int(5),Reason varchar(20),Date date)")
       
def insertData():
    num=int(input("ENTER Patient_Number"))
    name=input("ENTER NAME")
    cpr=int(input("ENTER CPR"))
    reas=input("ENTER REASON FOR ADMISSION")
    date=input("ENTER DATE OF ADMISSION")
    cur.execute("insert into Hospital_Log values({},'{}',{},'{}','{}')".format(num,name,cpr,reas,date))
    con.commit()
 
def display():
    cur.execute("select * from Hospital_Log")
    for k in cur:
        print(k)

while True:
	do=int(input("DO- "))
	if do==1:
		display()
	elif do==2:
		insertData()
	elif do==3:
		break
		
