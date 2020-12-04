import mysql.connector
Password=input("ENTER PASSWORD- ")
con=mysql.connector.connect(host="localhost",user="root",password=Password)
if con.is_connected():
    print("connection is succesful")
cur=con.cursor()
cur.execute("create database if not exists SHMhospital")
cur.execute("use shmhospital")
print("database created")
departments=[["Cardiologist",10],["Dermatologist",8],["Optometrist",9],["General Surgeon",10],\
                ["Psychiatrist",9],["Pediatrician",6]]   #The names dont really have to be here,
                                                         #the amounts are enough but I put it in anyway



def createtable():     
    query1="create table if not exists Hospital_Log(PID int(4) not null primary key,\
        Patient_Name varchar(20),CPR_Number int(9),Reason varchar(100),Date_of_entry date,bill decimal(6,3))"
    cur.execute(query1)

createtable()  




def billcount():
    dep=[]
    amount=0
    
    while True:
        if len(dep)>=6:
            break                                          #Buttons to select dep would be good
        reason=input("Enter department number- ")          #tweak this however you want Rishi       
        if not reason:
            break
        if int(reason) not in (1,2,3,4,5,6):
            print("Not available ")
            continue
        curdep=departments[int(reason)-1][0]
        if curdep in dep:
            print("Already selected ")
        elif int(reason) in (1,2,3,4,5,6) and curdep not in dep:
            dep.append(curdep)
            print(curdep)
            amount+=departments[int(reason)-1][1] 
    deps=""
    for x in dep:
        deps+=x
    return amount,deps


def insert():
    num=int(input("ENTER Patient_Number- "))
    name=input("ENTER NAME- ")
    cpr=int(input("ENTER CPR- "))
    print("""ENTER DEPARTMENT- 1-Cardiologist 
                  2-Dermatologist 
                  3-Optometrist 
                  4-General Surgeon 
                  5-Psychiatrist 
                  6-Pediatrician
                  Hit enter when done- """)
    bill,reas=billcount()
    date=input("ENTER DATE OF ADMISSION- ")
    cur.execute("insert into Hospital_Log values({},'{}',{},'{}','{}','{}')".format(num,name,cpr,reas,date,bill))
    con.commit()


def display():
    cur.execute("select * from Hospital_Log")
    for k in cur:
        print(k)

def update():
    x=int(input('Enter id of patient , that is to be updated'))
    print('''1:PID
          2:Patient name
          3:CPR NO.
          4:Reason
          5:Date of Entry
          6:Bill
          7:Return- ''')
    while True:
        ch=input('Enter Choice- ')
        if int(ch) not in (1,2,3,4,5,6,7):
            print("Incorrect input. Try again")

        elif not ch:
            break

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
            n=input('Enter New Reason- ')
            query="update hospital_log set Reason='"+n+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        elif ch=='5':
            n=input('Enter New Date- ')
            query="update hospital_log set Date_of_entry='"+n+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        elif ch=='6':
            bill,reas=billcount()
            query="update hospital_log set bill='"+str(bill)+"' where PID='"+str(x)+"'"
            cur.execute(query)
            con.commit()
        
def search():
    n=int(input("Enter the patient id of the patient details to be searched- "))
    query="select * from hospital_log where PID='"+str(n)+"'"
    cur.execute(query)
    
    
    mnop = cur.fetchall()
    if not mnop:
        print('Not found. Try again')
        search()
    if mnop:
        print(mnop)

while True:
    do=int(input("""COMMANDS- 1-Display all records 
          2-Insert record
          3-Update record 
          4-Search for record- """))
    if do==1:
        display()
    elif do==2:
        insert()
    elif do==3:
        update()
    elif do==4:
        search()


       
