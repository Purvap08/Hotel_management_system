import mysql.connector
from datetime import date
import time
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import pyautogui
import os
w, h = A4
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
#print(d,t)
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
                    if pas == owner[usernm]["password"]:
                        print("Login Successfully✅")
                        r=True
                        sql="SELECT * FROM `hotels` WHERE `owner_id` = %s AND `state` = %s"
                        val=(owner[usernm]["id"],"active")
                        cur.execute(sql,val)
                        result=cur.fetchall()
                        #print(result)
                        for h1 in result:
                            hotel[h1[0]]={"owner_id":h1[3],"hotel_name":h1[4],"status":h1[5]}
                        #print(hotel)
                        def h_id():
                            print("Select The Hotel")
                            print("_____________________________________")
                            print(f"| {"Id":<5} | {"name":<25} |")
                            print("_____________________________________")
                            for h1,hnm in hotel.items(): 
                                print(f"| {h1:<5} | {hnm["hotel_name"]:<25} |")
                            print("_____________________________________")  
                        while True:
                            h_id()
                            hid=int(input("Enter hotel Id(if you want to logging out Enter zero)="))
                            if hid == 0:
                                break
                            if hid in hotel:
                                print(f"\t \t \t ***Welcome to {hotel[hid]["hotel_name"]}***")
                                while True:
                                    print("What you Want to do..?\n 1.Order \n 2.Staff Attendence \n 3.Bill \n 4.logout")
                                    ch=int(input("Enter your choice="))
                                    match ch:
                                        case 1:
                                            waiter={}
                                            def staff():
                                                sql="SELECT * FROM `chef_info` WHERE `owner_id` = %s AND hotel_id = %s AND `designation` = %s"
                                                val=(owner[usernm]["id"],hid,"waiter")
                                                cur.execute(sql,val)
                                                result=cur.fetchall()
                                                for w in result:
                                                    waiter[w[0]]={"name":w[6]}
                                                print(f"{"Id":<5}  {"name":<15}")    
                                                for w1,wnm in waiter.items():
                                                    print(f"{w1:<5}  {wnm["name"]:<15}")    
                                            while True:
                                                staff()
                                                wid=int(input("Enter waiter id(if done enter 0)="))
                                                if wid == 0:
                                                    break
                                                if wid not in waiter:
                                                    print("Id not found")
                                                else:    
                                                    t_no=[]
                                                    #sql2="SELECT * FROM `table_det` WHERE `hotel_id` =%s AND`status` = %s"
                                                    #val2=(hid,"available")
                                                    sql2="SELECT * FROM `table_det` WHERE `hotel_id` =%s"
                                                    val2=(hid,)
                                                    cur.execute(sql2,val2)
                                                    result2=cur.fetchall()
                                                    print("***Available Tables***")
                                                    print(f"{'Table no'}")
                                                    for t1 in result2:
                                                        print(f"{t1[3]}")
                                                        t_no.append(t1[3])
                                                    tno=int(input("Enter table number="))
                                                    '''if tno == 0:
                                                        break'''
                                                    if tno not in t_no:
                                                        print("Invalid table number")
                                                    else: 
                                                        existing_customer=False
                                                        sql_check =" SELECT * FROM `customers` WHERE `hotel_id` = %s AND `table_no` = %s AND `status` = 'active'"
                                                        val_check = (hid, tno)
                                                        cur.execute(sql_check, val_check)
                                                        cust = cur.fetchall()
                                                        if cust:
                                                            cust = cust[0]  
                                                            customer_id = cust[0]
                                                            table_n = cust[6]
                                                            cnm = cust[7]
                                                            print("Table already occupied")
                                                            print(f"next Order for Customer: {table_n} ({cnm})")
                                                            customer_id = cust[0] 
                                                            existing_customer=True
                                                        else:    
                                                            cnm=input("Enter Customer name=")
                                                            cno=input("Enter contact number=")
                                                            if len(cno) != 10 or not cno.isdigit():
                                                                print("Invalid contact number please enter valid contact number")
                                                        category={}
                                                        sql="SELECT * FROM menu_category WHERE `hotel_id` = %s AND `status` = %s"
                                                        val=(hid,"available")
                                                        cur.execute(sql,val)
                                                        result=cur.fetchall()
                                                        print("_____________________________________")
                                                        print(f"{'id':<5} | {'Category name':<15}")
                                                        print("_____________________________________")
                                                        for c in result:
                                                            print(f"{c[0]:<5} | {c[5]:<15}")
                                                            category[c[0]]={"name":c[5]}
                                                        print("_____________________________________")
                                                        order={}    
                                                        while True:
                                                            c_id=int(input("Enter category id(if done enter zero)="))
                                                            if c_id == 0:
                                                                while True:
                                                                    print("Do you want to placed the order..?\n 1.Confirm \n 2.Edit \n 3.Cancel")
                                                                    ch = int(input("Enter your choice="))
                                                                    match ch:
                                                                        case 1:
                                                                            if not existing_customer:
                                                                                sql2="INSERT INTO `customers`(`date`, `time`, `owner_id`, `hotel_id`, `table_no`, `name`, `contact_no`, `status`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                                                                                val2 = (d,t,owner[usernm]["id"],hid,tno,cnm,cno,"active")
                                                                                cur.execute(sql2, val2)
                                                                                db.commit()
                                                                            for m_id, item in order.items():
                                                                                sql1 = "INSERT INTO `orders`(`date`, `time`, `owner_id`, `hotel_id`, `waiter_id`, `table_no`,`category_id`, `menu_id`, `name`, `quantity`, `price`, `total`, `status`)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  
                                                                                val1 = (d,t,owner[usernm]["id"],hid,wid,tno,item["category_id"],m_id,item["name"],item["quantity"],item["price"],item["total"],"placed")
                                                                                cur.execute(sql1, val1)
                                                                            db.commit()
                                                                            print("Your order Placed")
                                                                            break
                                                                        case 2:
                                                                            for i,v in order.items():
                                                                                print(i,v)
                                                                            m_id1=int(input("Enter menu id(if done Enter zero)="))
                                                                            if m_id1 in order:
                                                                                print("\n 1.Add quantity \n 2.delete quantity")
                                                                                ch1=int(input("Enter your Choice="))
                                                                                if ch1 == 1:
                                                                                    iqu=int(input("Enter quantity to add="))
                                                                                    order[m_id1]["quantity"] += iqu
                                                                                    order[m_id1]["total"] += iqu * order[m_id1]["price"]
                                                                                    print("Item Added Successfully")
                                                                                if ch1 ==2:
                                                                                    iqu=int(input("Enter quantity to remove="))
                                                                                    if iqu <= order[m_id1]["quantity"] and iqu > 0:
                                                                                        order[m_id1]["quantity"] -= iqu
                                                                                        order[m_id1]["total"] -= iqu * order[m_id1]["price"]
                                                                                        print("Item remove Successfully")
                                                                                    else:
                                                                                        print("Invalid Quantity")
                                                                            else:
                                                                                print("Id not found")
                                                                        case 3:
                                                                            print("Order cancel")
                                                                            break
                                                                        case _:
                                                                            print("Invalid Choice")
                                                                break
                                                            else:
                                                                if c_id in category:
                                                                    menu={}
                                                                    sql1="SELECT * FROM `menu` WHERE `category_id` = %s AND `status` = %s"
                                                                    val1=(c_id,"available")
                                                                    cur.execute(sql1,val1)
                                                                    result1=cur.fetchall()
                                                                    print("_____________________________________")
                                                                    print(f"{'id':<5} | {'name':<20} | {'price':<10}")
                                                                    print("_____________________________________")
                                                                    for m in result1:
                                                                        print(f"{m[0]:<5} | {m[6]:<20} | {m[7]:<10}")
                                                                        menu[m[0]]={"name":m[6],"price":m[7]}
                                                                    print("_____________________________________")
                                                                    while True:
                                                                        m_id=int(input("Enter menu Id(if done Enter zero)="))
                                                                        if m_id == 0:
                                                                            break
                                                                        else:
                                                                            if m_id in menu:
                                                                                qu=int(input("Enter quantity="))
                                                                                if m_id in order:
                                                                                    order[m_id]["quantity"] += qu
                                                                                    order[m_id]["total"] += qu * order[m_id]["price"]
                                                                                else:    
                                                                                    order[m_id]={"category_id":c_id,"name":menu[m_id]['name'],"quantity":qu,"price":menu[m_id]['price'],"total":qu*menu[m_id]['price']}
                                                                                    print("Item Added successfully")
                                                                            else:
                                                                                print("Id not found")
                                                                                
                                                                else:
                                                                    print("Id not found")
                                            print("____________________________________________________________________")
                                        case 2:
                                            chef_det={}
                                            def chef():
                                                sql="SELECT * FROM `chef_info` WHERE `hotel_id` = %s"
                                                val=(hid,)
                                                cur.execute(sql,val)
                                                result=cur.fetchall()
                                                print("_____________________________________")
                                                print(f"{'id':<5} | {'name':<10}")
                                                print("_____________________________________")
                                                for cd in result:
                                                    chef_det[cd[0]]={"name":cd[5]}
                                                    print(f"{cd[0]:<5} | {cd[5]:<15}")
                                                print("_____________________________________") 
                                            chef_atten={}    
                                            def atten():
                                                sql="SELECT * FROM  `chef_attendence` WHERE `date` = %s AND `hotel_id` = %s"
                                                val=(d,hid)
                                                cur.execute(sql,val)
                                                result=cur.fetchall()
                                                for ca in result:
                                                    chef_atten[ca[4]]={"status":ca[10]}
                                            chef()
                                            chef_id=int(input("Enter Chef id="))
                                            if chef_id in chef_det:        
                                                print("\n 1.Intime \n 2.Break time \n 3.Break end \n 4.Out time \n 5. Exit")
                                                ch=int(input("Enter Your Choice="))
                                                match ch:
                                                    case 1:
                                                        atten()
                                                        if chef_id in chef_atten:
                                                            print("In time is already marked")
                                                        else:   
                                                            sql="INSERT INTO `chef_attendence` (`date`,`owner_id`,`hotel_id`,`chef_id`, `name`, `in_time`,`attendence`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                                                            val=(d,owner[usernm]["id"],hid,chef_id,chef_det[chef_id]["name"],t,"present")
                                                            cur.execute(sql,val)
                                                            db.commit()
                                                            sql1="UPDATE `chef_info` SET `status`= %s WHERE `owner_id` = %s AND `hotel_id` = %s AND `id` = %s"
                                                            val1=("present",owner[usernm]["id"],hid,chef_id)
                                                            cur.execute(sql1,val1)
                                                            db.commit()
                                                            print("In Time Mark Successfully")
                                                    case 2:
                                                        atten()
                                                        if chef_id in chef_atten and chef_atten[chef_id]["status"] == "present":
                                                            sql="UPDATE `chef_attendence` SET `break_start`=%s , `attendence`= %s WHERE `chef_id`=%s AND `hotel_id` = %s AND `date` = %s "
                                                            val=(t,"break",chef_id,hid,d)
                                                            cur.execute(sql,val)
                                                            db.commit()
                                                            sql1="UPDATE `chef_info` SET `status`= %s WHERE `owner_id` = %s AND `hotel_id` = %s AND `id` = %s"
                                                            val1=("break",owner[usernm]["id"],hid,chef_id)
                                                            cur.execute(sql1,val1)
                                                            db.commit()
                                                            print("Break time mark successfully")
                                                        else:
                                                            print("Your intime is not marked or may be break time is already marked")
                                                    case 3:
                                                        atten()
                                                        if chef_id in chef_atten and chef_atten[chef_id]["status"] == "break":
                                                            sql="UPDATE `chef_attendence` SET `break_end`=%s , `attendence`= %s WHERE `chef_id`=%s AND `hotel_id` = %s AND `date` = %s "
                                                            val=(t,"present",chef_id,hid,d)
                                                            cur.execute(sql,val)
                                                            db.commit()
                                                            sql1="UPDATE `chef_info` SET `status`= %s WHERE `owner_id` = %s AND `hotel_id` = %s AND `id` = %s"
                                                            val1=("present",owner[usernm]["id"],hid,chef_id)
                                                            cur.execute(sql1,val1)
                                                            db.commit()
                                                            print("Break end time mark successfully")
                                                            atten()
                                                        else:
                                                            print("ERROR : Break out time is already marked")
                                                    case 4:
                                                        atten()
                                                        if chef_id in chef_atten and chef_atten[chef_id]["status"] == "present":
                                                            sql="UPDATE `chef_attendence` SET `out_time`=%s , `attendence`= %s WHERE `chef_id`=%s AND `hotel_id` = %s AND `date` = %s "
                                                            val=(t,"(out)present",chef_id,hid,d)
                                                            cur.execute(sql,val)
                                                            db.commit()
                                                            sql1="UPDATE `chef_info` SET `status`= %s WHERE `owner_id` = %s AND `hotel_id` = %s AND `id` = %s"
                                                            val1=("out",owner[usernm]["id"],hid,chef_id)
                                                            cur.execute(sql1,val1)
                                                            db.commit()
                                                            print("Out time mark successfully")
                                                        else:
                                                            print("ERROR")
                                                    case 5:
                                                        print("Exit Successfully")
                                                    case _:
                                                        print("Invalid Choice")
                                            else:
                                                print("Id not found")
                                            print("____________________________________________________________________")
                                        case 3:
                                            order_done={}
                                            sql="SELECT * FROM `orders` WHERE `owner_id` = %s AND `hotel_id` = %s AND `status` = %s"
                                            val=(owner[usernm]["id"],hid,"served")
                                            cur.execute(sql,val)
                                            result=cur.fetchall()
                                            '''for o in result:
                                                order_done[o[7]]={"table_number":o[5],"name":o[8],"quantity":o[9],"price":o[10],"total":o[11]}'''
                                            for o in result:
                                                tbl = o[6]  # table number

                                                if tbl not in order_done:
                                                    order_done[tbl] = []

                                                order_done[tbl].append({
                                                    "item_id": o[8],
                                                    "name": o[9],
                                                    "quantity": o[10],
                                                    "price": o[11],
                                                    "total": o[12]
                                                })    
                                            #print(order_done)
                                            bno=[]
                                            def bill():
                                                global b_no
                                                sql="SELECT * FROM `final_bills` WHERE `owner_id` = %s AND `hotel_id` = %s"
                                                val=(owner[usernm]["id"],hid)
                                                cur.execute(sql,val)
                                                result=cur.fetchall()
                                                for bn in result:
                                                    bno.append(bn[0])
                                                b_no=len(bno)+1
                                            bill()    
                                            table_no=int(input("Enter table number="))
                                            if table_no in order_done:
                                                def invoice():
                                                    invoice_no=b_no
                                                    invoice_name=f"{invoice_no}.pdf"
                                                    c = canvas.Canvas(invoice_name, pagesize=A4)
                                                    #c.drawString(50, h - 50, "Hello, world!")
                                                    c.drawString(180, h-100,hotel[hid]["hotel_name"])
                                                    c.drawString(50, h-120,f"Invoice Number :{invoice_no}")
                                                    c.drawString(50, h-135,f"date:{d}")
                                                    c.drawString(300,h-120,f"time:{t}")
                                                    c.drawString(300, h-135, f"Table No : {table_no}")
                                                    c.drawString(50, h-160,"--------------------------------------------------------------------")
                                                    c.drawString(50, h-180,"Item Id")
                                                    c.drawString(100,h-180,"Item name")  
                                                    c.drawString(180,h-180,"Quantity")
                                                    c.drawString(230,h-180,"price")
                                                    c.drawString(280,h-180,"q*price")
                                                    c.drawString(50, h-200,"--------------------------------------------------------------------")
                                                    t1=0
                                                    y=h-220
                                                    for i in order_done[table_no]:
                                                        c.drawString(50, y,f"{i["item_id"]}") 
                                                        c.drawString(100,y,f"{i["name"]}") 
                                                        c.drawString(180,y,f"{i["quantity"]}")
                                                        c.drawString(230,y,f"{i["price"]}")  
                                                        c.drawString(280,y,f"{i["total"]}")
                                                        y=y-20  
                                                        t1=t1+i["total"]
                                                    #order_done["grand total"]=t1   
                                                    c.drawString(50, y,"--------------------------------------------------------------------")
                                                    y=y-20
                                                    c.drawString(50, y,f"Total amount={t1}" )
                                                    y=y-20
                                                    c.drawString(120, y,"**********************************")
                                                    y=y-20
                                                    c.drawString(150, y,"Thank you visit again")
                                                    c.showPage()
                                                    c.save() 
                                                    for i1 in order_done[table_no]:
                                                        sql2="INSERT INTO `bill`(`date`, `time`, `bill_no`, `owner_id`, `hotel_id`, `table_no`, `item_id`, `item_name`, `quantity`, `price`, `total`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                                        val2=(d,t,b_no,owner[usernm]["id"],hid,table_no,i1["item_id"],i1["name"],i1["quantity"],i1["price"],i1["total"])
                                                        cur.execute(sql2,val2)
                                                        db.commit()
                                                    sql3="INSERT INTO `final_bills`(`date`, `time`, `bill_no`, `owner_id`, `hotel_id`, `table_no`, `grand_total`, `status`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"   
                                                    val3=(d,t,b_no,owner[usernm]["id"],hid,table_no,t1,"paid")
                                                    cur.execute(sql3,val3)
                                                    db.commit()
                                                    sql4="UPDATE `customers` SET `status` = %s WHERE `owner_id` = %s AND `hotel_id` = %s AND table_no = %s "
                                                    val4=("completed",owner[usernm]["id"],hid,table_no)
                                                    cur.execute(sql4,val4)
                                                    db.commit()
                                                    sql4="UPDATE `orders` SET `status` = %s WHERE `owner_id` = %s AND `hotel_id` = %s AND table_no = %s "
                                                    val4=("completed",owner[usernm]["id"],hid,table_no)
                                                    cur.execute(sql4,val4)
                                                    db.commit()
                                                    print("Bill saved successfully")
                                                    time.sleep(2)
                                                    os.popen(invoice_name)
                                                    time.sleep(7)
                                                    pyautogui.hotkey('alt','f4')
                                                invoice()    
                                            else:
                                                print("Invalid Table number")
                                            print("____________________________________________________________________")
                                        case 4:
                                            print("Logging out successfully")
                                            print("====================================================================")
                                            break
                                        case 5:
                                            print("Invalid choice")
                                            print("____________________________________________________________________")
                            else:
                                print("Invalid hotel id")
                                print("____________________________________________________________________")
                        break    
                    else:
                        print("Invalid Password")
                else:
                    print("Invalid username")
        case 2:
            print("Thank you")
            break
        case _:
            print("Invalid Choice")                
            
            