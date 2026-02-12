import mysql.connector
from datetime import date 
import time
import re
db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hotel_management"
)
cur=db.cursor()
#print(db)
d=date.today()
t=time.strftime("%H:%M:%S")
owner={}
def owner_det():
    owner.clear()
    sql="SELECT * FROM `owner`"
    cur.execute(sql)
    result=cur.fetchall()
    for o in result:
        owner[o[3]]={"id":o[1],"password":o[4],"name":o[5],"contact_no":o[6],"state":o[7]}
#owner_det()    
#print(owner)    
def add():
    owner_det()
    print("***Welcome for owner registration***")
    aadhar=input("Enter your aadhar number=")
    if aadhar in owner:
        print("owner is already registered with this aadhar number")
    else:
        if len(aadhar) != 12 or not aadhar.isdigit():
            print("Invalid aadhar number Please Enter valid aadhar number")
        else:    
            opass=input("Enter Password (Have at least one number,one uppercase letter,one lowercase letter,one special character ($, @, #, %)and between 6 and 20 characters in length)=")
            reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#%])[A-Za-z\d@$#%]{6,20}$"
            pat = re.compile(reg)
            mat = re.search(pat, opass)
            if not mat:
                print("Invalid Password!!")
            else: 
                nm=input("Enter your name=")
                cno=input("Enter contact number=")
                if len(cno) != 10 or not cno.isdigit():
                    print("Invalid contact number please enter valid contact number")
                else:    
                    sql="INSERT INTO `owner` (`date`,`time`,`aadhar`,`password`,`name`,`contact_no`,`state`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    val=(d,t,aadhar,opass,nm,cno,"active")
                    cur.execute(sql,val)
                    db.commit()
                    owner_det()
                    print(f"Your registration Done successfully \n Your aadhar number is your username")
def dele():
    owner_det()
    aadhar=input("Enter your aadhar number=")
    if aadhar in owner:
        #print("yes")
        od=owner[aadhar]
        #print(od)
        if "password" in od:
            opass=input("Enter password=")
            if opass == od["password"]:
                sql="DELETE FROM `owner` WHERE `aadhar`= %s"
                val=(aadhar,)
                cur.execute(sql,val)
                db.commit()
                print("owner details deleted successfully")
            else:
                print("Invalid password")
    else:
        print("Invalid id ")                    
def deactive():
    owner_det()
    aadhar=input("Enter your aadhar number=")
    if aadhar in owner:
        #print("yes")
        od=owner[aadhar]
        #print(od)
        if "password" in od:
            opass=input("Enter password=")
            if opass == od["password"]:
                #sql="DELETE FROM `owner` WHERE `aadhar`= %s"
                sql="Update `owner` SET `state` = %s WHERE `aadhar` = %s"
                val=("deactivate",aadhar)
                cur.execute(sql,val)
                db.commit()
                print("owner deactivated successfully")
            else:
                print("Invalid password")
    else:
        print("Invalid id ")
def activate():
    owner_det()
    aadhar = input("Enter your aadhar number=")
    if aadhar in owner:
        od = owner[aadhar]
        opass = input("Enter password=")
        if opass == od["password"]:
            sql = "UPDATE `owner` SET `state` = %s WHERE `aadhar` = %s"
            val = ("active", aadhar)
            cur.execute(sql, val)
            db.commit()
            print("Owner activated successfully")
        else:
            print("Invalid password")
    else:
        print("Invalid aadhar number")              
while True:
    print("Welcome What you want to do..?\n 1.Owner registration \n 2.Delete owner \n 3.Deactivate owner \n 4.Activate owner \n 5.Exit")
    c=int(input("Enter your choice="))
    match c:
        case 1:
            add()
            print("____________________________________________________________")
        case 2:
            dele()
            print("____________________________________________________________")
        case 3:
            deactive()
            print("____________________________________________________________")
        case 4:
            activate()
            print("____________________________________________________________")
        case 5:
            print("Thank you..")
            print("____________________________________________________________")
            break
        case _:
            print("Invalid choice")
            print("____________________________________________________________")