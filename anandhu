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
    query1="create table if not exists Hospital_Log(PID int(4) not null primary key,Patient_Name varchar(20),CPR_Number varchar(9),Reason varchar(20),Date_of_entry date,bill decimal(10,3))"
    cur.execute(query1)
def insert():
    num=int(input("ENTER Patient_Number"))
    name=input("ENTER NAME")
    cpr=input("ENTER CPR")
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


def update():
    x=int(input('Enter id of patient , that is to be updated'))
    print('1:PID,2:Patient name,3: CPR NO., 4:Reason,5: Date of Entry,6:Bill,7:Return')
    while True:
        ch=int(input('enter choice'))
        if ch==1:
            n=int(input('Enter new patient id'))
            query="update hospital_log set PID='"+str(n)+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        elif ch==2:
            n=input('enter New patient name')
            query="update hospital_log set Patient_Name= '"+n+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        elif ch==3:
            n=input('enter New CPR No.')
            query="update hospital_log set CPR_Number='"+n+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        elif ch==4:
            n=input('enter New Reason')
            query="update hospital_log set Reason='"+n+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        elif ch==5:
            n=input('enter New Date')
            query="update hospital_log set Date_of_entry='"+n+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        elif ch==6:
            n=input('enter New bill')
            query="update hospital_log set bill='"+str(n)+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        elif ch==7:
            return
        else:
            break

createtable()
#insert()
#search()
update()
       
        
    
    
    
    

