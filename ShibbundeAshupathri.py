import mysql.connector
from tabulate import tabulate
Password=input("ENTER PASSWORD- ")
con=mysql.connector.connect(host="localhost",user="root",password=Password)
if con.is_connected():
    print("connection is succesful")
cur=con.cursor()
cur.execute("create database if not exists SHMhospital")
cur.execute("use shmhospital")
print("database created")
departments=[["ENT",7],["Dentist",8],["Pediatrician",6],["Cardiologist",10],["Ophthalmologist",9],\
    ["General Surgeon",10],["Psychiatrist",9],["Dermatologist",8]]



def createtable():     
    query1="create table if not exists Hospital_Log(PID int(4) not null primary key,Patient_Name \
    varchar(20),CPR_Number int(9),Reason varchar(100),Date_of_entry date,bill decimal(6,3))"
    cur.execute(query1)

createtable()  




def billcount():
    dep=[]
    amount=0
    
    while True:
        if len(dep)>=8:
            print("DONE")
            break                                          #Buttons to select dep would be good
        reason=input("Enter department number(9/Enter to exit)- ")          #tweak this however you want Rishi       
        if not reason or reason==9:
            print("DONE")
            break
        if int(reason) not in (1,2,3,4,5,6,7,8,9):
            print("Not available ")
            continue
        curdep=departments[int(reason)-1][0]
        if curdep in dep:
            print("Already selected ")
        elif int(reason) in (1,2,3,4,5,6,7,8,9) and curdep not in dep:
            dep.append(curdep)
            print(curdep)
            amount+=departments[int(reason)-1][1] 
    deps=""
    for x in dep:
        deps+=x+","
    return amount,deps


def insert():
    num=int(input("ENTER Patient_ID- "))
    name=input("ENTER NAME- ")
    cpr=int(input("ENTER CPR- "))
    print("""DEPARTMENTS- 1-ENT
             2-Dentist 
             3-Pediatrician 
             4-Cardiologist 
             5-Ophthalmologist
             6-General Surgeon
             7-Psychiatrist
             8-Dermatologist
             9/Enter-Exit""")
    bill,reas=billcount()
    date=input("ENTER DATE OF ADMISSION- ")
    cur.execute("insert into Hospital_Log values({},'{}',{},'{}','{}','{}')".format(num,name,cpr,reas,date,bill))
    con.commit()


def display():
    RECORD=[]
    cur.execute("select * from Hospital_Log")
    RECORD=cur.fetchall()
    header=('P.ID','Patient Name','CPR,Reason','Date of Entry',' Bill')
    print(tabulate(RECORD,headers=header,tablefmt='grid'))
def update(x=''):
    if not x:
        x=int(input('Enter id of patient , that is to be updated- '))
    print('''What would you like to update?- 1-PID
                                2-Patient name
                                3-CPR NO.
                                4-Reason
                                5-Date of Entry
                                6/Enter-Exit''')
    while True:
        ch=input('Enter Choice(6/Enter to exit)- ')
        if not ch or ch==6:
            break
        elif int(ch) not in (1,2,3,4,5,6):
            print("Incorrect input. Try again")

        

        elif ch=='1':
            n=int(input('Enter new patient id- '))
            query="update hospital_log set PID='"+str(n)+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        elif ch=='2':
            n=input('Enter New patient name- ')
            query="update hospital_log set Patient_Name='"+n+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        elif ch=='3':
            n=input('Enter New CPR No.- ')
            query="update hospital_log set CPR_Number='"+n+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        elif ch=='4':
            bill,reas=billcount()
            query="update hospital_log set Reason='"+reas+"' where PID='"+str(x)+"'"
            cur.execute(query)
            query="update hospital_log set bill='"+str(bill)+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        elif ch=='5':
            n=input('Enter New Date- ')
            query="update hospital_log set Date_of_entry='"+n+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        
def delete():
    n=input('Enter ID of patient that is to be deleted')
    query="delete from hospital_log where PID='"+str(n)+"'"
    cur.execute(query)
    print('Record of Patient' ,n,'is deleted')
    con.commit()
        
def search():
    n=int(input("Enter the patient id of the patient details to be searched- "))
    query="select * from hospital_log where PID='"+str(n)+"'"
    cur.execute(query)
    
    
    rec = cur.fetchall()
    if not rec:
        print('Not found. Try again')
        search()
    else:
        print(rec)
        op=input("""Would you like to update? 1-Yes
                          2/Enter-No\n-- """)
        if op=='1':
            update(n)

while True:
    do=int(input("""COMMANDS- 1-Display all records 
          2-Insert record
          3-Update record 
          4-Search for record
          5-Delete record\nENTER COMMAND-"""))
    if do==1:
        display()
    elif do==2:
        insert()
    elif do==3:
        update()
    elif do==4:
        search()
    elif do==5:
        delete()
    elif not str(do):
        continue

       
