import mysql.connector
from datetime import date
import time
import asyncio
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
                        while True:
                            h_id()
                            hid=int(input("Enter hotel Id(if you want to logging out Enter zero)="))
                            if hid == 0:
                                break
                            if hid in hotel:
                                print(f"\t \t \t ***Welcome to {hotel[hid]["hotel_name"]}***")
                                while True:
                                    print("\n 1.Chef \n 2.Waiter \n 3.Exit")
                                    ch1=int(input("Enter your choice="))
                                    match ch1:
                                        case 1:
                                            while True:
                                                chef={}        
                                                def chef_inf():
                                                    sql="SELECT * FROM `chef_info` WHERE `owner_id` = %s AND `hotel_id` = %s AND `designation` = %s AND `status` = %s"
                                                    val=(owner[usernm]["id"],hid,"chef","present")
                                                    cur.execute(sql,val)
                                                    result=cur.fetchall()
                                                    for c in result:
                                                        chef[c[0]]={"name":c[5]}
                                                    print("=========================================")
                                                    print(f"{'id':<5}  {'name':<20} ")
                                                    print("=========================================")    
                                                    for cd,cn in chef.items():
                                                        print(f"{cd:<5}  {cn["name"]:<15}")
                                                    print("_____________________________________")    
                                                chef_inf() 
                                                cid=int(input("Enter Chef id(if done enter zero)="))
                                                if cid == 0:
                                                    break
                                                if cid in chef:
                                                    while True:
                                                        order={}
                                                        od=[]
                                                        def orders_det():
                                                            order.clear()
                                                            od.clear()
                                                            sql="SELECT * FROM `orders` WHERE `owner_id` = %s AND `hotel_id` = %s AND `status` = %s"
                                                            val=(owner[usernm]["id"],hid,"placed")
                                                            cur.execute(sql,val)
                                                            result=cur.fetchall()
                                                            for o in result:
                                                                order[o[0]]={"table_no":o[6],"name":o[9],"quantity":o[10]}
                                                                od.append(o[0])       
                                                        def oplaced():
                                                            orders_det()
                                                            print("***Orders***")
                                                            print("===================================================================")
                                                            print(f"{'id':<5} | {'table_no':<10} | {'name':<20} | {'quantity':<5}")
                                                            print("===================================================================")
                                                            for oid,op in order.items():
                                                                print(f"{oid:<5} | {op["table_no"]:<10} | {op["name"]:<20} | {op["quantity"]:<5}")
                                                            print("____________________________________________________________________")   
                                                        oprepared={}    
                                                        def oprepare():
                                                            sql="SELECT * FROM `kitchen` WHERE `owner_id` = %s AND `hotel_id` = %s AND `status` = %s"
                                                            val=(owner[usernm]["id"],hid,"preparing")
                                                            cur.execute(sql,val)
                                                            result=cur.fetchall()
                                                            for o in result:
                                                                oprepared[o[6]]={"name":o[7]}
                                                            print("=========================================")
                                                            print(f"{'id':<5}  {'name':<20} ")
                                                            print("=========================================")      
                                                            for opid,oprep in oprepared.items():
                                                                print(f"{opid:<5}  {oprep["name"]:<15}")
                                                            print("_____________________________________")    
                                                        print("What you Want to do..?\n 1.Chek order list \n 2.pick order \n 3.placed order \n 4.logout")
                                                        ch=int(input("Enter your choice="))
                                                        match ch:
                                                            case 1:
                                                                oplaced()
                                                                sql ="UPDATE orders SET display = 'shown' WHERE hotel_id = %s AND status = 'placed'"
                                                                val=(hid,)   
                                                                cur.execute(sql,val)
                                                                db.commit()
                                                                print("____________________________________________________________________")
                                                            case 2:
                                                                oplaced()
                                                                oid=int(input("Enter order id="))
                                                                if oid in order:
                                                                    sql="INSERT INTO `kitchen`(`date`, `owner_id`, `hotel_id`, `chef_id`, `name`,`order_id`, `item_name`, `table_no`, `picked_time`,  `status`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                                                    val=(d,owner[usernm]["id"],hid,cid,chef[cid]["name"],oid,order[oid]["name"],order[oid]["table_no"],t,"preparing")
                                                                    cur.execute(sql,val)
                                                                    db.commit()
                                                                    sql1="UPDATE `orders` SET `status`= %s WHERE `owner_id` = %s AND `hotel_id` = %s AND `id` = %s"
                                                                    val1=("preparing",owner[usernm]["id"],hid,oid)
                                                                    cur.execute(sql1,val1)
                                                                    db.commit()
                                                                    print("order picked successfully")
                                                                else:
                                                                    print("Invalid id ")
                                                                print("____________________________________________________________________")
                                                            case 3:
                                                                oprepare()
                                                                oid=int(input("Enter order id="))
                                                                if oid in oprepared:
                                                                    sql="UPDATE `kitchen` SET `status`= %s , `placed_time` =%s WHERE owner_id= %s AND `hotel_id` = %s AND `order_id` = %s"
                                                                    val=("prepared",t,owner[usernm]["id"],hid,oid)
                                                                    cur.execute(sql,val)
                                                                    db.commit()
                                                                    sql1="UPDATE `orders` SET `status`= %s WHERE `owner_id` = %s AND `hotel_id` = %s AND `id` = %s"
                                                                    val1=("prepared",owner[usernm]["id"],hid,oid)
                                                                    cur.execute(sql1,val1)
                                                                    db.commit()
                                                                    print("order placed successfully")
                                                                else:
                                                                    print("Invalid id ")
                                                                print("____________________________________________________________________")
                                                            case 4:
                                                                print("Logging out Successfully")
                                                                print("====================================================================")
                                                                break
                                                else:
                                                    print("Invalid chef id")
                                        case 2:
                                            waiter={}
                                            def wait_info():
                                                sql="SELECT * FROM `chef_info` WHERE `owner_id` = %s AND `hotel_id` = %s AND `designation` = %s AND `status` = %s"
                                                val=(owner[usernm]["id"],hid,"waiter","present")
                                                cur.execute(sql,val)
                                                result=cur.fetchall()
                                                for w in result:
                                                    waiter[w[0]]={"name":w[5]}
                                                print("=========================================")
                                                print(f"{'id':<5}  {'name':<20} ")
                                                print("=========================================")    
                                                for wd,wn in waiter.items():
                                                    print(f"{wd:<5}  {wn["name"]:<15}")
                                                print("_____________________________________")    
                                            while True:
                                                wait_info() 
                                                wid=int(input("Enter waiter id(if done enter zero)="))
                                                if wid == 0:
                                                    break
                                                if wid in waiter:
                                                    while True:
                                                        print("What you Want to do..?\n 1.Chek order list \n 2.pick order \n 3.placed order \n 4.logout")
                                                        ch=int(input("Enter your choice="))
                                                        oprep={}
                                                        def check():
                                                            sql="SELECT * FROM `kitchen` WHERE `owner_id` = %s AND `hotel_id` = %s AND `status` = %s"
                                                            val=(owner[usernm]["id"],hid,"prepared")
                                                            cur.execute(sql,val)
                                                            result=cur.fetchall()
                                                            print(f"{"id":<5} {"name":<15} {"table_no":<5}")
                                                            for op in result:
                                                                print(f"{op[6]:<5} {op[7]:<15} {op[8]:<5}")
                                                                oprep[op[6]]={"name":op[7], "table_no":op[8]}
                                                            print("____________________________________________________________________")
                                                        match ch:
                                                            case 1:
                                                                check()
                                                            case 2:
                                                                check()
                                                                oid=int(input("Enter order id="))
                                                                if oid in oprep:
                                                                    sql="INSERT INTO `waiter`(`date`, `owner_id`, `hotel_id`, `waiter_id`, `name`,`order_id`, `item_name`, `table_no`, `picked_time`,  `status`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                                                    val=(d,owner[usernm]["id"],hid,wid,waiter[wid]["name"],oid,oprep[oid]["name"],oprep[oid]["table_no"],t,"picked")
                                                                    cur.execute(sql,val)
                                                                    db.commit()
                                                                    '''sql1="UPDATE `orders` SET `status`= %s WHERE `owner_id` = %s AND `hotel_id` = %s AND `id` = %s"
                                                                    val1=("preparing",owner[usernm]["id"],hid,oid)
                                                                    cur.execute(sql1,val1)
                                                                    db.commit()'''
                                                                    print("order picked successfully")
                                                                else:
                                                                    print("Invalid id ")
                                                                print("____________________________________________________________________")
                                                            case 3:
                                                                check()
                                                                oid=int(input("Enter order id="))
                                                                if oid in oprep:
                                                                    sql="UPDATE `waiter` SET `status`= %s , `placed_time` =%s WHERE owner_id= %s AND `hotel_id` = %s AND `order_id` = %s"
                                                                    val=("placed",t,owner[usernm]["id"],hid,oid)
                                                                    cur.execute(sql,val)
                                                                    db.commit()
                                                                    sql1="UPDATE `orders` SET `status`= %s WHERE `owner_id` = %s AND `hotel_id` = %s AND `id` = %s"
                                                                    val1=("served",owner[usernm]["id"],hid,oid)
                                                                    cur.execute(sql1,val1)
                                                                    db.commit()
                                                                    sql2="UPDATE `kitchen` SET `status`= %s , `placed_time` =%s WHERE owner_id= %s AND `hotel_id` = %s AND `order_id` = %s"
                                                                    val2=("completed",t,owner[usernm]["id"],hid,oid)
                                                                    cur.execute(sql2,val2)
                                                                    db.commit()
                                                                    print("order placed successfully")
                                                                else:
                                                                    print("Invalid id ")
                                                                print("____________________________________________________________________")
                                                            case 4:
                                                                print("Logging out Successfully")
                                                                print("====================================================================")
                                                                break
                                                else:
                                                    print("Invalid waiter id")
                                                print("____________________________________________________________________")
                                        case 3:
                                            break
                                            print("____________________________________________________________________")
                                        case _:
                                            print("Invalid choice")
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