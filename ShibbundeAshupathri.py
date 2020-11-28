import mysql.connector
Password=input("ENTER PASSWORD- ")
con=mysql.connector.connect(host="localhost",user="root",password=Password)
if con.is_connected():
    print("connection is succesful")
cur=con.cursor()
cur.execute("create database if not exists SHMhospital")
cur.execute("use shmhospital")
print("database created")
def createtable():
    query1="create table if not exists Hospital_Log(PID int(4) not null primary key,Patient_Name varchar(20),CPR_Number int(9),Reason varchar(20),Date_of_entry date,bill decimal(6,3))"
    cur.execute(query1)
def insert():
    num=int(input("ENTER Patient_Number"))
    name=input("ENTER NAME")
    cpr=int(input("ENTER CPR"))
    reas=input("ENTER REASON FOR ADMISSION")
    date=input("ENTER DATE OF ADMISSION")
    bill=float(input("enter amount to be paid"))
    cur.execute("insert into Hospital_Log values({},'{}',{},'{}','{}','{}')".format(num,name,cpr,reas,date,bill))
    con.commit()
def search():
    n=int(input("enter the patient id of the patient details to be searched"))
    query="select * from hospital_log where PID='"+str(n)+"'"
    cur.execute(query)
    for k in cur:
        print(k)
createtable()
insert()
 search()
def display():
    cur.execute("select * from Hospital_Log")
    for k in cur:
        print(k)
def search():
	

while True:
	do=int(input("DO- "))
	if do==1:
		display()
	elif do==2:
		insertData()
	elif do==3:
		break
		
