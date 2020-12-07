import mysql.connector
from tabulate import tabulate
Password=input("ENTER PASSWORD- ")
con=mysql.connector.connect(host="localhost",user="root",password=Password)
cur=con.cursor()
cur.execute("create database if not exists SHMhospital")
cur.execute("use shmhospital")
departments=[["ENT",7],["Dentist",8],["Pediatrician",6],["Cardiologist",10],["Ophthalmologist",9],\
    ["General Surgeon",10],["Psychiatrist",9],["Dermatologist",8]]
   
query1="create table if not exists Hospital_Log(PID int(4) not null primary key,Patient_Name \
    varchar(20),CPR_Number int(9),Reason varchar(100),Date_of_entry date,bill decimal(6,3))"
cur.execute(query1)

cur.execute("use shmhospital")

def billcount():
    dep=[]
    amount=0
    
    while True:
        if len(dep)>=5:
            q=input("All selected- Hit enter ")
            break                                          
        reason=input("Enter department number(9/Enter to exit)- ")                 
        if not reason or reason=='9':
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
        if x==dep[-1]:
            deps+=x
        else:
            deps+=x+","
    return amount,deps

def inpcheck(x):
    while True:
        try:
            inp=int(input(x))
        except:
            print("Invalid input. Try again")
            continue
        break
    return inp
        
def insert():
    while True:
        num=inpcheck("ENTER Patient_ID- ")
        query="select * from hospital_log where PID='"+str(num)+"'"
        cur.execute(query)
        rec = cur.fetchall()
        if not rec:
            break
        else:
            print("Entered ID already in use. ")
            continue
        
    name=input("ENTER NAME- ")
    cpr=inpcheck("ENTER CPR- ")
    print("""DEPARTMENTS- 1-ENT
             2-Dentist 
             3-Pediatrician 
             4-Cardiologist 
             5-Ophthalmologist
             6-General Surgeon
             7-Psychiatrist
             8-Dermatologist
             9/Enter-Exit
             (MAX FIVE)""")
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
    print('''What would you like to update?- 1-PID
                                2-Patient name
                                3-CPR NO.
                                4-Reason
                                5-Date of Entry
                                6/Enter-Exit''')
    while True:
        ch=input('Enter Choice(6/Enter to exit)- ')
        if not ch or ch=='6':
            break
        elif ch not in ('1','2','3','4','5','6'):
            print("Incorrect input. Try again")

        elif ch=='1':
            n=inpcheck('Enter new patient id- ')
            q=input("Hit enter to confirm ")
            query="update hospital_log set PID='"+str(n)+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        elif ch=='2':
            n=input('Enter New patient name- ')
            q=input("Hit enter to confirm ")
            query="update hospital_log set Patient_Name='"+n+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        elif ch=='3':
            n=inpcheck('Enter New CPR No.- ')
            q=input("Hit enter to confirm ")
            query="update hospital_log set CPR_Number='"+n+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        elif ch=='4':
            bill,reas=billcount()
            q=input("Hit enter to confirm ")
            query="update hospital_log set Reason='"+reas+"' where PID='"+str(x)+"'"
            cur.execute(query)
            query="update hospital_log set bill='"+str(bill)+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        elif ch=='5':
            n=input('Enter New Date- ')
            q=input("Hit enter to confirm ")
            query="update hospital_log set Date_of_entry='"+n+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        
def delete(n=''):
    query="delete from hospital_log where PID='"+str(n)+"'"
    cur.execute(query)
    print('Record of Patient Number' ,n,'is deleted')
    con.commit()
        
def search(upd,dele):
    if upd==True:
        n=inpcheck("Enter the patient id of the patient details to be updated- ")
    elif dele==True:
        n=inpcheck("Enter the patient id of the patient details to be deleted- ")
    else:
        n=inpcheck("Enter the patient id of the patient details to be searched- ")
    query="select * from hospital_log where PID='"+str(n)+"'"
    cur.execute(query)
    
    rec = cur.fetchall()
    if not rec:
        print('Not found. Try again')
        if upd==True:
            search(True,False)
        elif dele==True:
            search(False,True)
   
    else:
        header=('P.ID','Patient Name','CPR,Reason','Date of Entry',' Bill')
        print(tabulate(rec,headers=header,tablefmt='grid'))                
        if upd==True:
            update(n)
        elif dele==True:
            while True:
                q=input("Hit enter to confirm(1 to cancel) ")
                if not q:
                    delete(n)
                    break
                elif q=='1':
                    search(False,True)
                    break
                else:
                    print("Invalid input. Try again")
                    continue
                   

while True:
    do=inpcheck("""COMMANDS- 1-Display all records 
          2-Insert record
          3-Search for record
          4-Update record 
          5-Delete record\nENTER COMMAND-""")
    if do==1:
        display()
    elif do==2:
        insert()
    elif do==3:
        search(False,False)    #search
    elif do==4:
        search(True,False)    #update
    elif do==5:
        search(False,True)    #delete
    elif not str(do):
        continue
       
