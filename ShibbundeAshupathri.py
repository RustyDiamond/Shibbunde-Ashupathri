import mysql.connector
from tabulate import tabulate
while True:
    try:
        Password=input("ENTER PASSWORD--- ")
        con=mysql.connector.connect(host="localhost",user="root",password=Password)
    except mysql.connector.errors.ProgrammingError:
        print("Incorrect password. Try again. ")
        continue
    break
cur=con.cursor()
cur.execute("create database if not exists SHMhospital")
cur.execute("use shmhospital")
departments=[["ENT",7],["Dentist",8],["Pediatrician",6],["Cardiologist",10],["Ophthalmologist",9],["General Surgeon",10],["Psychiatrist",9],["Dermatologist",8]]
query1="create table if not exists Hospital_Log(PID int(4) not null primary key,Patient_Name varchar(20),Sex char(1),Date_Of_Birth date,CPR_Number int(9),Phone_num int(6))"
cur.execute(query1)

query1="create table if not exists Patient_Reciept(PID int(4) not null primary key,Reason varchar(100),bill decimal(6,3),Date_of_entry date)"
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
        num=inpcheck("ENTER Patient_ID---: ")
        query="select * from hospital_log where PID='"+str(num)+"'"
        cur.execute(query)
        rec = cur.fetchall()
        if not rec:
            break
        else:
            print("Entered ID already in use. ")
            continue
        
    name=input("ENTER NAME---: ")
    while True:
        gend=input("ENTER GENDER---:")
        if len(gend)>1 or gend not in ('f','F','m','M'):
            print("Invalid input ")
            continue
        gend=gend.upper()
        break
    birth=input("ENTER DATE OF BIRTH--- ")
    while True:
        cpr=inpcheck("ENTER CPR---: ")
        if len(str(cpr))==5:
            break
        else:
            print("Invalid CPR Number. Make sure 5 digits are present ")
    while True:
        phone=inpcheck("ENTER PHONE NUMBER---: ")
        if len(str(phone))==6:
            break
        else:
            print("Invalid Phone Number. Make sure 6 digits are present ")
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
    date=input("ENTER DATE OF ADMISSION--- ")
    cur.execute("insert into Hospital_Log values({},'{}','{}','{}',{},{})".format(num,name,gend,birth,cpr,phone))
    cur.execute("insert into Patient_Reciept values({},'{}',{},'{}')".format(num,reas,bill,date))
    con.commit()


def display():
    while True:
        op=input("""What would you like to display?
        ---------------------------
        1-All records
        ---------------------------
        2-Patient Bill
        ---------------------------
        3/Enter-Exit \n--""")
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
            header=('P.ID','Patient Name','CPR','date of birth','Date of Entry',' Bill')
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
                    cur.execute("select Hospital_Log.PID,Patient_Name,CPR_Number,Reason,Bill,Date_of_Entry,Phone_num from Patient_Reciept,Hospital_Log where Hospital_Log.PID = Patient_Reciept.PID order by Date_of_entry asc")
                    z=cur.fetchall()
                    header=('P.ID','Patient Name','CPR','Reason','Bill','Date of Entry','Phone No.')
                    print(tabulate(z,headers=header,tablefmt='fancy_grid')) 
                    q=input("Hit enter to continue ")
                    print("")
                    break
                elif op1=='2':
                    cur.execute("select Hospital_Log.PID,Patient_Name,CPR_Number,Reason,Bill,Date_of_Entry,Phone_num from Patient_Reciept,Hospital_Log where Hospital_Log.PID = Patient_Reciept.PID order by Date_of_entry desc")
                    z=cur.fetchall()
                    header=('P.ID','Patient Name','CPR','Reason','Bill','Date of Entry','Phone No.')
                    print(tabulate(z,headers=header,tablefmt='fancy_grid'))
                    q=input("Hit enter to continue ")
                    print("")
                    break
    
                    
def update(x=''):
    print("")
    print('''What would you like to update?
                --> 1-PID
                --> 2-Patient name
                --> 3-Gender
                --> 4-Date of birth
                --> 5-CPR NO.
                --> 6-Phone Number
                --> 7-Reason
                --> 8-Date of Entry
                --> 9/Enter-Exit''')
               
    while True:
        ch=input('Enter Choice(9/Enter to exit)- ')
        print("")
        if not ch or ch=='9':
            break
        elif ch not in ('1','2','3','4','5','6','7','8','9'):
            print("Incorrect input. Try again")

        elif ch=='1':
            n=inpcheck('Enter new Patient ID-- ')
            query="update hospital_log set PID='"+str(n)+"' where PID='"+str(x)+"'"   #Patient table
            cur.execute(query)

            query="update Patient_Reciept set PID='"+str(n)+"' where PID='"+str(x)+"'"   #Reciept table
            cur.execute(query)
            con.commit()

            m="select * from hospital_log where PID='"+str(n)+"'"
            cur.execute(m)
            z=cur.fetchall()
            header=('P.ID','Patient Name','Sex','Date of Birth','CPR','Phone Number')
            print(" Patient Log")
            print(tabulate(z,headers=header,tablefmt='fancy_grid'))

            m="select * from Patient_Reciept where PID='"+str(n)+"'"
            cur.execute(m)
            z=cur.fetchall()
            header=('P.ID','Reason','Bill','Date of Entry')
            print(" Patient Reciept")
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
            header=('P.ID','Patient Name','Sex','Date of Birth','CPR','Phone Number')
            print(tabulate(z,headers=header,tablefmt='fancy_grid'))
            q=input("Hit enter to continue ")
            print("")

        elif ch=='3':
            while True:
                n=input("ENTER GENDER---:")
                if len(n)>1 or n not in ('f','F','m','M'):
                    print("Invalid input ")
                    continue
                break
            query="update hospital_log set Sex='"+str(n)+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
            m="select * from hospital_log where PID='"+str(x)+"'"
            cur.execute(m)
            z=cur.fetchall()
            header=('P.ID','Patient Name','Sex','Date of Birth','CPR','Phone Number')
            print(tabulate(z,headers=header,tablefmt='fancy_grid'))
            q=input("Hit enter to continue ")
            print("")

        elif ch=='4':
            n=input('Enter New Date of Birth- ')
            query="update hospital_log set Date_Of_Birth='"+n+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
            m="select * from hospital_log where PID='"+str(x)+"'"
            cur.execute(m)
            z=cur.fetchall()
            header=('P.ID','Patient Name','Sex','Date of Birth','CPR','Phone Number')
            print(tabulate(z,headers=header,tablefmt='fancy_grid'))
            q=input("Hit enter to continue ")  

        elif ch=='5':
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
            header=('P.ID','Patient Name','Sex','Date of Birth','CPR','Phone Number')
            print(tabulate(z,headers=header,tablefmt='fancy_grid'))
            q=input("Hit enter to continue ")
            print("")

        elif ch=='6':
            while True:
                n=inpcheck('Enter New Phone Number.- ')
                if len(str(n))==6:
                    break
                else:
                    print("*Invalid Phone Number. Make sure 6 digits are present* ")
            query="update hospital_log set Phone_num='"+str(n)+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
            m="select * from hospital_log where PID='"+str(x)+"'"
            cur.execute(m)
            z=cur.fetchall()
            header=('P.ID','Patient Name','Sex','Date of Birth','CPR','Phone Number')
            print(tabulate(z,headers=header,tablefmt='fancy_grid'))
            q=input("Hit enter to continue ")
            print("")
        elif ch=='7':
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
            query="update Patient_Reciept set Reason='"+reas+"' where PID='"+str(x)+"'"
            cur.execute(query)
            query="update Patient_Reciept set bill='"+str(bill)+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
            m="select * from Patient_Reciept where PID='"+str(x)+"'"
            cur.execute(m)
            z=cur.fetchall()
            header=('P.ID','Reason',' Bill','Date of Entry')
            print(tabulate(z,headers=header,tablefmt='fancy_grid')) 
            q=input("Hit enter to continue ")                 

        elif ch=='8':
            n=input('Enter New Date of Entry- ')
            query="update Patient_Reciept set Date_of_entry='"+n+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
            m="select * from Patient_Reciept where PID='"+str(x)+"'"
            cur.execute(m)
            z=cur.fetchall()
            header=('P.ID','Reason',' Bill','Date of Entry')
            print(tabulate(z,headers=header,tablefmt='fancy_grid'))
            q=input("Hit enter to continue ")
        
def delete(n=''):
    query="delete from hospital_log where PID='"+str(n)+"'"
    cur.execute(query)
    query="delete from Patient_Reciept where PID='"+str(n)+"'"
    cur.execute(query)
    print('Record of Patient Number' ,n,'is deleted')
    con.commit()
        

    if upd==True:
        n=inpcheck("Enter the patient name of the patient details to be updated(0 to cancel)- ")
    elif dele==True:
        n=inpcheck("Enter the patient name of the patient details to be deleted(0 to cancel)- ")
    else:
        n=inpcheck("Enter the patient name of the patient details to be searched(0 to cancel)- ")
    if n==0:
        return
    query="select * from hospital_log where Patient_Name='"+str(n)+"'"
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
            

def search(upd,dele):
    if upd==True:
        n=inpcheck("Enter the patient id of the patient details to be updated(0 to cancel)- ")
    elif dele==True:
        n=inpcheck("Enter the patient id of the patient details to be deleted(0 to cancel)- ")
    else:
        n=inpcheck("Enter the patient id of the patient details to be searched(0 to cancel)- ")
    if n==0:
        return
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
        header=('P.ID','Patient Name','Sex','Date of Birth','CPR','Phone Number')
        print(" Patient Log")
        print(tabulate(rec,headers=header,tablefmt='fancy_grid'))

        m="select * from Patient_Reciept where PID='"+str(n)+"'"
        cur.execute(m)
        z=cur.fetchall()
        header=('P.ID','Reason','Bill','Date of Entry')
        print(" Patient Reciept")
        print(tabulate(z,headers=header,tablefmt='fancy_grid'))

                     
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
                    break
                else:
                    print("Invalid input. Try again")
                    continue      

while True:
    print("""    ------COMMANDS------
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
        do=input("""ENTER COMMAND- """)
        if not do:
            break
        elif do not in('1','2','3','4','5','6'):
            print("Invalid input. Try again ")
            continue

        break
    if do=='1':
        print("")
        s1 = "II---DISPLAY---II"
        kop1 = s1.center(70,"-")
        print(kop1)
        print("")
        display()
    elif do=='2':
        print("")
        s2 = "II---INSERT---II"
        kop2 = s2.center(70,"-")
        print(kop2)
        print("")
        insert()
    elif do=='3':
        print("")
        s3 = "II---SEARCH---II"
        kop3 = s3.center(70,"-")
        print(kop3)
        print("")
        search(False,False)    #search
    elif do=='4':
        print("")
        s4 = "II---UPDATE---II"
        kop4 = s4.center(70,"-")
        print(kop4)
        print("")
        search(True,False)    #update
    elif do=='5':
        print("")
        s5 = "II---DELETE---II"
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



       

