import mysql.connector
from datetime import date
import time
db=mysql.connector.connect(
		host="localhost",
		user="root",
		password="",
		database="Hotel_management"
)
cur=db.cursor()
#print(db)
d=date.today()
t=time.strftime("%H:%M:%S")
owner={}
def owner_det():
    sql="SELECT * FROM owner WHERE `state` = 'active'"
    cur.execute(sql)
    result=cur.fetchall()
    for o in result:
        owner[o[3]]={"id":o[0],"password":o[4],"name":o[5],"contact_no":o[6],"state":o[7]}
#owner_det()
#print(owner)
hotel={} 
r=False       
'''def login():
    login()
    global r
    global usernm'''
owner_det()
while True:
    hotel.clear()
    print("What you want to do \n 1.Login \n 2.Exit")
    c=int(input("Enter your choice="))
    match c:
        case 1:
            print("***HOTEL MANAGEMENT SYSTEM***")
            for lg in range(0,3):
                usernm=input("Enter Username=")
                pas=input("Enter Password=")
                if usernm in owner:
                    '''sql="SELECT password from owner WHERE aadhar = %s"
                    val=(usernm,)
                    cur.execute(sql,val)
                    result=cur.fetchone()
                    for p in result:
                    p=p'''
                    if pas == owner[usernm]["password"]:
                        print("Login Successfully✅")
                        r=True
                        sql="SELECT * FROM `hotels` WHERE `owner_id` = %s AND `state` = %s"
                        val=(owner[usernm]["id"],"active")
                        cur.execute(sql,val)
                        result=cur.fetchall()
                        #print(result)
                        for h in result:
                            hotel[h[0]]={"owner_id":h[3],"hotel_name":h[4],"status":h[5]}
                        #print(hotel)
                        def h_id():
                            print("Select The Hotel")
                            print("_____________________________________")
                            print(f"| {"Id":<5} | {"name":<25} |")
                            print("_____________________________________")
                            for h,hnm in hotel.items(): 
                                print(f"| {h:<5} | {hnm["hotel_name"]:<25} |")
                            print("_____________________________________")    
                            #hid=int(input("Enter hotel id="))
                            #return hid
                        while True:    
                            print("What you want to do \n 1.Add new hotel \n 2.other \n 3.exit")
                            choice=int(input("Enter your choice="))
                            match choice:
                                case 1:
                                    #login()
                                    #add()
                                    hotelnm=input("Enter Hotel name=")
                                    sql="INSERT INTO `hotels` (date,time,owner_id,hotel_name,status,state) VALUES (%s,%s,%s,%s,%s,%s)"
                                    val=(d,t,owner[usernm]["id"],hotelnm,"open","active")
                                    cur.execute(sql,val)
                                    db.commit()
                                    print("Hotel Register successfully")
                                    print("_____________________________________________________________")
                                case 2:
                                    while True:
                                        h_id()
                                        hid=int(input("Enter hotel id(if logging out from owner page enter 0)="))
                                        if hid == 0:
                                            print("Logging out from owner successfully ")
                                            print("_____________________________________________________________")
                                            break
                                        if hid in hotel:  
                                            print(f"\t \t \t ***Welcome to {hotel[hid]["hotel_name"]}***")
                                            while True:
                                                print("\n 1.Hotel \n 2.Menu category \n 3.Menu \n 4.Staff \n 5.Tables \n 6.Logout")
                                                c=int(input("Enter your choice="))
                                                match c:
                                                    case 1:
                                                        while True:
                                                            print("Welcome.. What you want to do..?\n 1.Update hotel status \n 2.Deactivate hotel\n 3.Delete hotel \n 4.Exit")
                                                            ch=int(input("Enter your choice="))
                                                            match ch:     
                                                                case 1:
                                                                    s=int(input("\n 1.Open \n 2.Closed \n Enter your choice="))
                                                                    if s == 1:
                                                                        sql="UPDATE `hotels` SET status = %s WHERE id = %s"
                                                                        val=("open",hid)
                                                                        cur.execute(sql,val)
                                                                        db.commit()
                                                                        print("Hotel Status updated successfully")
                                                                    if s == 2:
                                                                        sql="UPDATE `hotels` SET status = %s WHERE id = %s"
                                                                        val=("closed",hid)
                                                                        cur.execute(sql,val)
                                                                        db.commit()
                                                                        print("Hotel Status updated successfully") 
                                                                    if s >= 3:
                                                                        print("Invalid choice")
                                                                
                                                                    print("_____________________________________________________________")
                                                                case 2:
                                                                    #sql="DELETE FROM `hotels` WHERE id = %s"
                                                                    sql="UPDATE `hotels` SET `state` = %s WHERE id=  %s"
                                                                    val=("deactivate",hid)
                                                                    cur.execute(sql,val)
                                                                    db.commit()
                                                                    print("Hotel Deactivate successfully")
                                                                    print("_____________________________________________________________")
                                                                case 3:
                                                                    sql="DELETE FROM `hotels` WHERE id = %s"
                                                                    val=(hid,)
                                                                    cur.execute(sql,val)
                                                                    db.commit()
                                                                    print("Hotel Deleted successfully")
                                                                    print("_____________________________________________________________")
                                                                case 4:
                                                                    print("Exit successfully")
                                                                    #print("_____________________________________________________________")
                                                                    break
                                                                case _:
                                                                    print("Invalid choice")
                                                                    print("_____________________________________________________________")
                                                        print("====================================================================")
                                                    case 2:
                                                        while True:
                                                            print("What you want to do..?\n 1.Add category \n 2.Update category \n 3.Delete category \n 4.Check \n 5.Exit")
                                                            ch=int(input("Enter your choice="))
                                                            category={}
                                                            match ch:
                                                                case 1:
                                                                    while True:
                                                                        sql="SELECT * FROM `menu_category` WHERE `hotel_id` = %s"
                                                                        val=(hid,)
                                                                        cur.execute(sql,val)
                                                                        result=cur.fetchall()
                                                                        for cat in result:
                                                                            category[cat[4]]={"id":cat[0],"name":cat[5]}    
                                                                        cnm=input("Enter category name(if done enter 0)=")
                                                                        if cnm != "0":
                                                                            r=0
                                                                            for v in category.values():
                                                                                if cnm == v["name"]:
                                                                                    r=1
                                                                                    break
                                                                            if r:
                                                                                print("Category name is already added")
                                                                            else:
                                                                                sql1="INSERT INTO `menu_category` (`date`,`time`,`owner_id`,`hotel_id`,`name`,`status`,`state`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                                                                                val1=(d,t,owner[usernm]["id"],hid,cnm,"available","active")
                                                                                cur.execute(sql1,val1)
                                                                                db.commit()
                                                                                print("Category added successfully")
                                                                        else:
                                                                            break
                                                                    print("_____________________________________________________________")
                                                                case 2:
                                                                    sql="SELECT * FROM `menu_category` WHERE `hotel_id` = %s"
                                                                    val=(hid,)
                                                                    cur.execute(sql,val)
                                                                    result=cur.fetchall()
                                                                    print(f"{'id':<5}{'Category':<15}{'Status'}")
                                                                    catid=[]
                                                                    for mcat in result:
                                                                        print(f"{mcat[0]:<5}{mcat[5]:<15}{mcat[6]}")
                                                                        catid.append(mcat[0])
                                                                    cid=int(input("Enter Category Id="))
                                                                    if cid in catid:    
                                                                        print("What you want to update in category..?\n 1.Name \n 2.Status")
                                                                        ch1=int(input("Enter your choice="))
                                                                        match ch1:
                                                                            case 1:
                                                                                cnm=input("Enter category name=")
                                                                                sql2="UPDATE `menu_category` SET `name` = %s WHERE `id` = %s"
                                                                                val2=(cnm,cid)
                                                                                cur.execute(sql2,val2)
                                                                                db.commit()
                                                                                print("Category name updated successfully")
                                                                            case 2:
                                                                                '''cid=int(input("Enter Category Id="))
                                                                                if cid in catid:'''
                                                                                cstat=int(input("\n 1.available \n 2.unavailable \n Enter category status="))
                                                                                match cstat:
                                                                                    case 1:
                                                                                        sql2="UPDATE `menu_category` SET `status` = %s WHERE `id` = %s"
                                                                                        val2=("available",cid)
                                                                                        cur.execute(sql2,val2)
                                                                                        db.commit()
                                                                                        print("Categry Status updated successfully")
                                                                                    case 2:
                                                                                        sql2="UPDATE `menu_category` SET `status` = %s WHERE `id` = %s"
                                                                                        val2=("unavailable",cid)
                                                                                        cur.execute(sql2,val2)
                                                                                        db.commit()
                                                                                        print("Categry Status updated successfully")
                                                                                    case _:
                                                                                        print("Invalid choice")
                                                                            case _:
                                                                                print("Invalid choice")
                                                                    else:
                                                                        print("Id not found")
                                                                    print("_____________________________________________________________")
                                                                case 3:
                                                                    sql="SELECT * FROM `menu_category` WHERE `hotel_id` = %s"
                                                                    val=(hid,)
                                                                    cur.execute(sql,val)
                                                                    result=cur.fetchall()
                                                                    print(f"{'id':<5}{'Category':<15}{'Status'}")
                                                                    catid=[]
                                                                    for mcat in result:
                                                                        print(f"{mcat[0]:<5}{mcat[5]:<15}{mcat[6]}")
                                                                        catid.append(mcat[0])
                                                                    cid=int(input("Enter Category Id="))
                                                                    if cid in catid:    
                                                                        sql="UPDATE `menu_category` SET `state` = %s WHERE `id` = %s"
                                                                        val=("deleted",cid)
                                                                        cur.execute(sql,val)
                                                                        db.commit()
                                                                        print("Category deleted Successfully")
                                                                    else:
                                                                        print("Id not found")
                                                                    print("_____________________________________________________________")
                                                                case 4:
                                                                    sql="SELECT * FROM `menu_category` WHERE `hotel_id` = %s"
                                                                    val=(hid,)
                                                                    cur.execute(sql,val)
                                                                    result=cur.fetchall()
                                                                    print("_______________________________________")
                                                                    print(f"| {'id':<5} | {'Category':<15} | {'Status':<10} |")
                                                                    print("_______________________________________")
                                                                    for mcat in result:
                                                                        print(f"| {mcat[0]:<5} | {mcat[5]:<15} | {mcat[6]:<10} |")
                                                                    print("_______________________________________")
                                                                case 5:
                                                                    print("Exit successfully")
                                                                    #print("_____________________________________________________________")
                                                                    break
                                                                case _:
                                                                    print("Invalid choice")
                                                                    print("_____________________________________________________________")
                                                        print("====================================================================")
                                                    case 3:
                                                        cid=[]
                                                        mid=[]
                                                        def category():
                                                            sql="SELECT * FROM `menu_category` WHERE `hotel_id` = %s"
                                                            val=(hid,)
                                                            cur.execute(sql,val)
                                                            result=cur.fetchall()
                                                            print("_______________________________________")
                                                            print(f"| {'id':<5} | {'Category':<15} | {'Status':<10} |")
                                                            print("_______________________________________")
                                                            for mcat in result:
                                                                print(f"| {mcat[0]:<5} | {mcat[5]:<15} | {mcat[6]:<10} |")
                                                                cid.append(mcat[0])
                                                            print("_______________________________________")   
                                                        def menu():
                                                            sql="SELECT * FROM `menu` WHERE `hotel_id` = %s"
                                                            val=(hid,)
                                                            cur.execute(sql,val)
                                                            result=cur.fetchall()
                                                            print("_______________________________________")
                                                            print(f"| {'id':<5} | {'name':<25} | {'price':<10} | {'status':<12}")
                                                            print("_______________________________________")
                                                            for m in result:
                                                                print(f"| {m[0]:<5} | {m[6]:<25} | {m[7]:<10} | {m[8]:<12}")
                                                                mid.append(m[0])
                                                            print("_______________________________________")     
                                                        while True:    
                                                            print("What you want to do..?\n 1.Add menu \n 2.Update menu \n 3.Delete menu \n 4.Check menu \n 5.Exit")    
                                                            ch=int(input("Enter your choice="))
                                                            match ch:
                                                                case 1:
                                                                    category()
                                                                    while True:
                                                                        c_id=int(input("Enter category id in which to want to add menu(if done Enter zero)=")) 
                                                                        if c_id == 0:
                                                                            break
                                                                        else:    
                                                                            if c_id in cid:
                                                                                while True:
                                                                                    nm=input("Enter item name(if done enter zero)=")
                                                                                    if nm == "0":
                                                                                        break
                                                                                    else:
                                                                                        pr=int(input("Enter price="))
                                                                                        sql1="INSERT INTO `menu` (`date`,`time`,`owner_id`,`hotel_id`,`category_id`,`name`,`price`,`status`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                                                                                        val1=(d,t,owner[usernm]["id"],hid,c_id,nm,pr,"available")
                                                                                        cur.execute(sql1,val1)
                                                                                        db.commit()
                                                                                        print("Menu added successfully")
                                                                            else:
                                                                                print("Invalid category id")
                                                                            print("_____________________________________________________________")
                                                                case 2:
                                                                    menu()
                                                                    while True:
                                                                        print("What you want to update..? \n 1.name \n 2.price \n 3.Status \n 4.Exit")
                                                                        ch2=int(input("Enter your choice="))
                                                                        match ch2:
                                                                            case 1:
                                                                                m_id=int(input("Enter item id="))
                                                                                if m_id in mid:
                                                                                    nm=input("Enter item name=")
                                                                                    sql2="UPDATE `menu` SET `name` = %s WHERE `id` = %s"
                                                                                    val2=(nm,m_id)
                                                                                    cur.execute(sql2,val2)
                                                                                    db.commit()
                                                                                    print("Name updated successfully")
                                                                                else:
                                                                                    print("Id not found")
                                                                            case 2:
                                                                                m_id=int(input("Enter item id="))
                                                                                if m_id in mid:
                                                                                    pr=int(input("Enter item price="))
                                                                                    sql2="UPDATE `menu` SET `price` = %s WHERE `id` = %s"
                                                                                    val2=(pr,m_id)
                                                                                    cur.execute(sql2,val2)
                                                                                    db.commit()
                                                                                    print("Price updated successfully")
                                                                                else:
                                                                                    print("Id not found")
                                                                            case 3:
                                                                                mstat=int(input("\n 1.available \n 2.unavailable \n Enter category status="))
                                                                                match mstat:
                                                                                    case 1:
                                                                                        m_id=int(input("Enter item id="))
                                                                                        if m_id in mid:
                                                                                            sql2="UPDATE `menu` SET `status` = %s WHERE `id` = %s"
                                                                                            val2=("available",m_id)
                                                                                            cur.execute(sql2,val2)
                                                                                            db.commit()
                                                                                            print("Categry Status updated successfully")
                                                                                        else:
                                                                                            print("Id not found")
                                                                                    case 2:
                                                                                        m_id=int(input("Enter item id="))
                                                                                        if m_id in mid:
                                                                                            sql2="UPDATE `menu` SET `status` = %s WHERE `id` = %s"
                                                                                            val2=("unavailable",m_id)
                                                                                            cur.execute(sql2,val2)
                                                                                            db.commit()
                                                                                            print("Categry Status updated successfully")
                                                                                        else:
                                                                                            print("Id not found")
                                                                                    case _:
                                                                                        print("Invalid choice")
                                                                                print("Status updated successfully")
                                                                            case 4:
                                                                                break
                                                                            case _:
                                                                                print("Invalid choice")
                                                                    print("_____________________________________________________________")
                                                                case 3:
                                                                    menu()
                                                                    m_id=int(input("Enter item id="))
                                                                    if m_id in mid:
                                                                        sql2="DELETE FROM `menu` WHERE `id` = %s"
                                                                        val2=(m_id,)
                                                                        cur.execute(sql2,val2)
                                                                        db.commit()
                                                                        print("Item deleted successfully")
                                                                    else:
                                                                        print("Id not found")
                                                                    print("_____________________________________________________________")
                                                                case 4:
                                                                    menu()
                                                                    print("_____________________________________________________________")
                                                                case 5:
                                                                    print("Exit successfully")
                                                                    break
                                                                case _:
                                                                    print("Invalid choice")
                                                        print("====================================================================")
                                                    case 4:
                                                        while True:
                                                            print("\n 1. Chef \n 2. Waiter \n 3. Exit")
                                                            ch1=int(input("Enter your choice="))
                                                            match ch1:
                                                                case 1:
                                                                    while True:
                                                                        print("What you want to do..? \n 1.Add chef \n 2.Update chef details \n 3.Delete chef \n 4.check chef \n 5.Exit")
                                                                        ch=int(input("Enter your choice="))
                                                                        cid=[]
                                                                        chef={}
                                                                        sql="SELECT * FROM `chef_info` WHERE `hotel_id` = %s AND `designation` = %s"
                                                                        val=(hid,"chef")
                                                                        cur.execute(sql,val)
                                                                        result=cur.fetchall()
                                                                        for c in result:
                                                                            chef[c[4]]={"id":c[0],"name":c[5],"contact_no":c[6],"status":c[7]}
                                                                            cid.append(c[0])
                                                                        def chef_det():
                                                                            print("_____________________________________________________________")
                                                                            print(f"{"id":<5} | {"name":<10} | {"contact_no":<12} | {"Status":10}")
                                                                            print("_____________________________________________________________")
                                                                            for c in chef.values():
                                                                                print(f"{c["id"]:<5} | {c["name"]:<10} | {c["contact_no"]:<12} |")
                                                                        match ch:
                                                                            case 1:
                                                                                aadhar=input("Enter your aadhar number=")
                                                                                if aadhar in chef :
                                                                                    print("chef is already registered with this aadhar number")
                                                                                else:
                                                                                    if len(aadhar) != 12 or not aadhar.isdigit():
                                                                                        print("Invalid aadhar number Please Enter valid aadhar number")
                                                                                    else:    
                                                                                        nm=input("Enter your name=")
                                                                                        cno=input("Enter contact number=")
                                                                                        if len(cno) != 10 or not cno.isdigit():
                                                                                            print("Invalid contact number please enter valid contact number")
                                                                                        else:    
                                                                                            sql="INSERT INTO `chef_info` (`date`,`owner_id`,`hotel_id`,`aadhar`,`designation`,`name`,`contact_no`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                                                                                            val=(d,owner[usernm]["id"],hid,aadhar,"chef",nm,cno)
                                                                                            cur.execute(sql,val)
                                                                                            db.commit()
                                                                                            owner_det()
                                                                                            print(f"Chef added successfully")
                                                                                print("_____________________________________________________________")
                                                                            case 2:
                                                                                chef_det()
                                                                                c_id=int(input("Enter chef id="))
                                                                                if c_id in cid:
                                                                                    print("What you want to update..?\n 1.Name \n 2.Contact no")
                                                                                    ch1=int(input("Enter your choice="))
                                                                                    match ch1:
                                                                                        case 1:
                                                                                            cnm=input("Enter name=")
                                                                                            sql="UPDATE `chef_info` SET `name` = %s WHERE `id` = %s"
                                                                                            val=(cnm,c_id)
                                                                                            cur.execute(sql,val)
                                                                                            db.commit()
                                                                                            print("Name updated successfully")
                                                                                        case 2:
                                                                                            cno=input("Enter contact number=")
                                                                                            if len(cno) != 10 or not cno.isdigit():
                                                                                                print("Invalid contact number please enter valid contact number")
                                                                                            else:    
                                                                                                sql="UPDATE `chef_info` SET `contact_no` = %s WHERE `id` = %s"
                                                                                                val=(cno,c_id)
                                                                                                cur.execute(sql,val)
                                                                                                db.commit()
                                                                                                print("Contact number updated successfully")
                                                                                        case _:
                                                                                            print("Invalid choice")
                                                                                else:
                                                                                    print("Id not found")
                                                                                print("_____________________________________________________________")
                                                                            case 3:
                                                                                chef_det()
                                                                                c_id=int(input("Enter chef id="))
                                                                                if c_id in cid:
                                                                                    sql="DELETE FROM `chef_info` WHERE `id` = %s"
                                                                                    val=(c_id,)
                                                                                    cur.execute(sql,val)
                                                                                    db.commit()
                                                                                    print("Chef deleted successfully")
                                                                                else:
                                                                                    print("Id not found")
                                                                                print("_____________________________________________________________")
                                                                            case 4:
                                                                                chef_det()
                                                                                print("_____________________________________________________________")
                                                                            case 5:
                                                                                print("Exit Successfully")
                                                                                break
                                                                            case _:
                                                                                print("Invalid Choice")
                                                                case 2:
                                                                    while True:
                                                                        print("What you want to do..? \n 1.Add waiter \n 2.Update waiter details \n 3.Delete waiter \n 4.check waiter \n 5.Exit")
                                                                        ch=int(input("Enter your choice="))
                                                                        cid=[]
                                                                        chef={}
                                                                        sql="SELECT * FROM `chef_info` WHERE `hotel_id` = %s AND `designation` = %s"
                                                                        val=(hid,"waiter")
                                                                        cur.execute(sql,val)
                                                                        result=cur.fetchall()
                                                                        for c in result:
                                                                            chef[c[4]]={"id":c[0],"name":c[5],"contact_no":c[6],"status":c[7]}
                                                                            cid.append(c[0])
                                                                        def chef_det():
                                                                            print("_____________________________________________________________")
                                                                            print(f"{"id":<5} | {"name":<10} | {"contact_no":<12} | {"Status":10}")
                                                                            print("_____________________________________________________________")
                                                                            for c in chef.values():
                                                                                print(f"{c["id"]:<5} | {c["name"]:<10} | {c["contact_no"]:<12} |")
                                                                        match ch:
                                                                            case 1:
                                                                                aadhar=input("Enter your aadhar number=")
                                                                                if aadhar in chef :
                                                                                    print("Staff is already registered with this aadhar number")
                                                                                else:
                                                                                    if len(aadhar) != 12 or not aadhar.isdigit():
                                                                                        print("Invalid aadhar number Please Enter valid aadhar number")
                                                                                    else:    
                                                                                        nm=input("Enter your name=")
                                                                                        cno=input("Enter contact number=")
                                                                                        if len(cno) != 10 or not cno.isdigit():
                                                                                            print("Invalid contact number please enter valid contact number")
                                                                                        else:    
                                                                                            sql="INSERT INTO `chef_info` (`date`,`owner_id`,`hotel_id`,`aadhar`,`designation`,`name`,`contact_no`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                                                                                            val=(d,owner[usernm]["id"],hid,aadhar,"waiter",nm,cno)
                                                                                            cur.execute(sql,val)
                                                                                            db.commit()
                                                                                            owner_det()
                                                                                            print(f"Staff added successfully")
                                                                                print("_____________________________________________________________")
                                                                            case 2:
                                                                                chef_det()
                                                                                c_id=int(input("Enter staff id="))
                                                                                if c_id in cid:
                                                                                    print("What you want to update..?\n 1.Name \n 2.Contact no")
                                                                                    ch1=int(input("Enter your choice="))
                                                                                    match ch1:
                                                                                        case 1:
                                                                                            cnm=input("Enter name=")
                                                                                            sql="UPDATE `chef_info` SET `name` = %s WHERE `id` = %s"
                                                                                            val=(cnm,c_id)
                                                                                            cur.execute(sql,val)
                                                                                            db.commit()
                                                                                            print("Name updated successfully")
                                                                                        case 2:
                                                                                            cno=input("Enter contact number=")
                                                                                            if len(cno) != 10 or not cno.isdigit():
                                                                                                print("Invalid contact number please enter valid contact number")
                                                                                            else:    
                                                                                                sql="UPDATE `chef_info` SET `contact_no` = %s WHERE `id` = %s"
                                                                                                val=(cno,c_id)
                                                                                                cur.execute(sql,val)
                                                                                                db.commit()
                                                                                                print("Contact number updated successfully")
                                                                                        case _:
                                                                                            print("Invalid choice")
                                                                                else:
                                                                                    print("Id not found")
                                                                                print("_____________________________________________________________")
                                                                            case 3:
                                                                                chef_det()
                                                                                c_id=int(input("Enter chef id="))
                                                                                if c_id in cid:
                                                                                    sql="DELETE FROM `chef_info` WHERE `id` = %s"
                                                                                    val=(c_id,)
                                                                                    cur.execute(sql,val)
                                                                                    db.commit()
                                                                                    print("staff deleted successfully")
                                                                                else:
                                                                                    print("Id not found")
                                                                                print("_____________________________________________________________")
                                                                            case 4:
                                                                                chef_det()
                                                                                print("_____________________________________________________________")
                                                                            case 5:
                                                                                print("Exit Successfully")
                                                                                break
                                                                            case _:
                                                                                print("Invalid Choice")
                                                                case 3:
                                                                    break
                                                                case 4:
                                                                    print("Invalid choice")
                                                        print("====================================================================")
                                                    case 5:
                                                        while True:
                                                            print("What you wnat to do..?\n 1.Add table \n 2.Delete table \n 3.Check table \n 4.exit")
                                                            ch=int(input("Enter your choice="))
                                                            table=[]
                                                            sql="SELECT `table_no` FROM `table_det` WHERE `hotel_id` = %s"
                                                            val=(hid,)
                                                            cur.execute(sql,val)
                                                            result=cur.fetchall() 
                                                            for t in result:
                                                                table.append(t[0])
                                                            match ch:
                                                                case 1:
                                                                    while True:
                                                                        tno=int(input("Enter Table no(if done enter 0)="))
                                                                        if tno in table:
                                                                            print("Table number is already added")
                                                                        else:    
                                                                            if tno != 0:
                                                                                sql1="INSERT INTO `table_det` (`owner_id`,`hotel_id`,`table_no`,`status`) VALUES (%s,%s,%s,%s)"
                                                                                val1=(owner[usernm]["id"],hid,tno,"available")
                                                                                cur.execute(sql1,val1)
                                                                                db.commit()
                                                                                print("Table added successfully")
                                                                            else:
                                                                                break
                                                                            print("_____________________________________________________________")
                                                                case 2:
                                                                    tno=int(input("Enter Table no="))
                                                                    if tno in table:
                                                                        sql1="DELETE FROM `table_det` WHERE `table_no` = %s"
                                                                        val1=(tno,)
                                                                        cur.execute(sql1,val1)
                                                                        db.commit()
                                                                        print("Table deleted successfully")
                                                                    else:    
                                                                        print("Table not fount.. Incorrect table number")
                                                                    #print("Table deleted successfully")
                                                                    #print("_____________________________________________________________")
                                                                case 3: 
                                                                    sql1="SELECT * FROM `table_det` WHERE `hotel_id` = %s"
                                                                    val1=(hid,)
                                                                    cur.execute(sql1,val1)
                                                                    result=cur.fetchall()
                                                                    print("_____________________________________________________________")
                                                                    print(f"{"id":<5} {"Table no":<10} {"Order id":<10} {"Status"}")
                                                                    print("_____________________________________________________________")
                                                                    for r in result:
                                                                        print(f"{r[0]:<5} {r[3]:<10}  {r[5]}")
                                                                    print("_____________________________________________________________")
                                                                case 4:
                                                                    print("Exit successfully")
                                                                    break
                                                                case _:
                                                                    print("Invalid choice")
                                                        print("====================================================================")    
                                                    case 6:
                                                        print("Logging out successfully")
                                                        print("====================================================================")
                                                        break
                                                    case _:
                                                        print("Invalid choice")
                                                        print("====================================================================") 
                                        else:
                                            print("Invalid id")
                                    break
                                case 3:
                                    print("_____________________________________________________________")
                                    break
                                case _:
                                    print("Invalid choice")
                                    print("_____________________________________________________________")
                    else:
                        print("Incorrect Password")
                        print("_____________________________________________________________")
                else:
                    print("Invalid Username")
                    print("_____________________________________________________________")
                break
        case 2:
            print("Thank you")
            break
        case _:
            print("Invalid Choice")