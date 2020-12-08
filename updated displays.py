import mysql.connector
from tabulate import tabulate
Password=input("ENTER PASSWORD-")
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
        if reason not in ('1','2','3','4','5','6','7','8',):
            print("Not available ")
            continue
        curdep=departments[int(reason)-1][0]
        if curdep in dep:
            print("Already selected ")
        elif reason in ('1','2','3','4','5','6','7','8','9') and curdep not in dep:
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
    print("")
    while True:
        num=inpcheck("---ENTER Patient_ID---: ")
        query="select * from hospital_log where PID='"+str(num)+"'"
        cur.execute(query)
        rec = cur.fetchall()
        if not rec:
            break
        else:
            print("Entered ID already in use. ")
            continue
        
    name=input("---ENTER NAME---: ")
    while True:
        cpr=inpcheck("---ENTER CPR---: ")
        if len(str(cpr))==5:
            break
        else:
            print("Invalid CPR Number. Make sure 5 digits are present ")
    print("""---DEPARTMENTS---
             -> 1-ENT
             -> 2-Dentist 
             -> 3-Pediatrician 
             -> 4-Cardiologist 
             -> 5-Ophthalmologist
             -> 6-General Surgeon
             -> 7-Psychiatrist
             -> 8-Dermatologist
             -> 9/Enter-Exit
             ***(MAX FIVE)""")
    bill,reas=billcount()
    date=input("---ENTER DATE OF ADMISSION--- ")
    cur.execute("insert into Hospital_Log values({},'{}',{},'{}','{}','{}')".format(num,name,cpr,reas,date,bill))
    con.commit()


def display():
    while True:
        op=input("""What would you like to display?
        ---------------------------
        1-All records
        ---------------------------
        2-All records by date
        ---------------------------
        3/Enter-Exit
        ---------------------------""")
        if op=='3' or not op:
            break
        elif op not in('1','2','3'):
            print("Invalid input. Try again ")
            print("")
            continue
        
        elif op=='1':
            RECORD=[]
            cur.execute("select * from Hospital_Log")
            RECORD=cur.fetchall()
            header=('P.ID','Patient Name','CPR','Reason','Date of Entry',' Bill')
            print(tabulate(RECORD,headers=header,tablefmt='fancy_grid'))
            print("")
            q=input("Hit enter to continue ")
        elif op=='2':
            while True:
                x=[('1','Old to New'),
                   ('2','New to Old')]
                h=('Hit','Order')
                print(tabulate(x,headers=h,tablefmt='fancy_grid'))
                op1=input('Order-') 
                
                if op1 not in('1','2'):
                    print("Invalid input. Try again ")
                    continue
                elif op1=='1':
                    cur.execute("select * from Hospital_Log order by Date_of_entry asc")
                    z=cur.fetchall()
                    header=('P.ID','Patient Name','CPR','Reason','Date of Entry',' Bill')
                    print(tabulate(z,headers=header,tablefmt='fancy_grid')) 
                    q=input("Hit enter to continue ")
                    print("")
                    break
                elif op1=='2':
                    cur.execute("select * from Hospital_Log order by Date_of_entry desc")
                    z=cur.fetchall()
                    header=('P.ID','Patient Name','CPR','Reason','Date of Entry',' Bill')
                    print(tabulate(z,headers=header,tablefmt='fancy_grid'))
                    q=input("Hit enter to continue ")
                    print("")
                    break
                    
def update(x=''):
    print("")
    print('''What would you like to update?
                --> 1-PID
                --> 2-Patient name
                --> 3-CPR NO.
                --> 4-Reason
                --> 5-Date of Entry
                --> 6/Enter-Exit''')
               
    while True:
        ch=input('Enter Choice(6/Enter to exit)- ')
        print("")
        if not ch or ch=='6':
            break
        elif ch not in ('1','2','3','4','5','6'):
            print("Incorrect input. Try again")

        elif ch=='1':
            n=inpcheck('Enter new patient id-- ')
            query="update hospital_log set PID='"+str(n)+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
            m="select * from hospital_log where PID='"+str(n)+"'"
            cur.execute(m)
            z=cur.fetchall()
            header=('P.ID','Patient Name','CPR','Reason','Date of Entry',' Bill')
            print(tabulate(z,headers=header,tablefmt='fancy_grid'))
            q=input("Hit enter to continue ")
            print("")
            
        elif ch=='2':
            n=input('Enter New patient name-- ')
            query="update hospital_log set Patient_Name='"+str(n)+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
            m="select * from hospital_log where PID='"+str(x)+"'"
            cur.execute(m)
            z=cur.fetchall()
            header=('P.ID','Patient Name','CPR','Reason','Date of Entry',' Bill')
            print(tabulate(z,headers=header,tablefmt='fancy_grid'))
            q=input("Hit enter to continue ")
            print("")
               
        elif ch=='3':
            while True:
                n=inpcheck('Enter New CPR No.- ')
                if len(str(n))==5:
                    break
                else:
                    print("*Invalid CPR Number. Make sure 5 digits are present* ")
            query="update hospital_log set CPR_Number='"+str(n)+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
            m="select * from hospital_log where PID='"+str(x)+"'"
            cur.execute(m)
            z=cur.fetchall()
            header=('P.ID','Patient Name','CPR','Reason','Date of Entry',' Bill')
            print(tabulate(z,headers=header,tablefmt='fancy_grid'))
            q=input("Hit enter to continue ")
            print("")
        elif ch=='4':
            print("""---ENTER NEW DEPARTMENTS---
                    --> 1-ENT
                    --> 2-Dentist 
                    --> 3-Pediatrician 
                    --> 4-Cardiologist 
                    --> 5-Ophthalmologist
                    --> 6-General Surgeon
                    --> 7-Psychiatrist
                    --> 8-Dermatologist
                    --> 9/Enter-Exit
                    --> (MAX FIVE)""")
            bill,reas=billcount()
            query="update hospital_log set Reason='"+reas+"' where PID='"+str(x)+"'"
            cur.execute(query)
            query="update hospital_log set bill='"+str(bill)+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
            m="select * from hospital_log where PID='"+str(x)+"'"
            cur.execute(m)
            z=cur.fetchall()
            header=('P.ID','Patient Name','CPR','Reason','Date of Entry',' Bill')
            print(tabulate(z,headers=header,tablefmt='fancy_grid')) 
            q=input("Hit enter to continue ")                 

        elif ch=='5':
            n=input('Enter New Date- ')
            query="update hospital_log set Date_of_entry='"+n+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
            m="select * from hospital_log where PID='"+str(x)+"'"
            cur.execute(m)
            z=cur.fetchall()
            header=('P.ID','Patient Name','CPR','Reason','Date of Entry',' Bill')
            print(tabulate(z,headers=header,tablefmt='fancy_grid'))
            q=input("Hit enter to continue ")
        
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
            search(False,False)
   
    else:
        header=('P.ID','Patient Name','CPR','Reason','Date of Entry',' Bill')
        print(tabulate(rec,headers=header,tablefmt='fancy_grid'))
                     
        if upd==True:
            update(n)
        elif dele==True:
            while True:
                q=input("Hit enter to confirm / 1 to cancel- ")
                if not q:
                    delete(n)
                    q=input("Hit enter to continue ")   
                    break
                elif q=='1':
                    search(False,True)
                    q=input("Hit enter to continue ")   
                    break
                else:
                    print("Invalid input. Try again")
                    continue
                   

while True:
    print("""   ------COMMANDS------
    ---------------------------
    1-Display all records
    ---------------------------
    2-Insert record
    ---------------------------
    3-Search for record
    ---------------------------
    4-Update record
    ---------------------------
    5-Delete record
    ---------------------------
    6/Enter- Exit
    ---------------------------""")
    while True:
        do=input("""ENTER COMMAND-""")
        if do not in('1','2','3','4','5','6'):
            print("Invalid input. Try again ")
            continue
        break
    if do=='1':
        print("")
        s1 = "II---DISPLAY SELECTED---II"
        kop1 = s1.center(70,"-")
        print(kop1)
        print("")
        display()
    elif do=='2':
        print("")
        s2 = "II---INSERT SELECTED---II"
        kop2 = s2.center(70,"-")
        print(kop2)
        print("")
        insert()
    elif do=='3':
        print("")
        s3 = "II---SEARCH SELECTED---II"
        kop3 = s3.center(70,"-")
        print(kop3)
        print("")
        search(False,False)    #search
    elif do=='4':
        print("")
        s4 = "II---UPDATE SELECTED---II"
        kop4 = s4.center(70,"-")
        print(kop4)
        print("")
        search(True,False)    #update
    elif do=='5':
        print("")
        s5 = "II---DELETE SELECTED---II"
        kop5 = s5.center(70,"-")
        print(kop5)
        print("")
        search(False,True)    #delete
    elif not do or do=='6':
        print("")
        s6 = "II---EXIT---II"
        kop6 = s6.center(70,"-")
        print(kop6)
        print("")
        break
