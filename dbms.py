import oracledb
import tabulate
#pw=input('Enter the Password')
mydb=oracledb.connect(user="system",host="localhost",password='Vaidehi')
mycur=mydb.cursor()

#Printing a list of operations
print('''MENU
1.Inserting a new car model 
2.Inserting new car that can be rented 
3.Registering a new customer 
4.Buying a car 
5.Booking a rental car 
6.Picking up a rental car 
7.Returning a rental car 
8.Updating an entry when a rental car is in maintenance 
9.Viewing the Sales report 
10.Viewing the rental history of a particular vehicle 
11.View customers
12.Finding vehicals in a price range
13.Finding models in a price range 
14.Finding customers with a given member level 
15.Increse stock of a model 
16.Update customer membership level 
17.View all models available 
18.View all Vehicals available for rentals 
19.Enter features for a given model_id
20.Return a car from maintenance
21.Exit''')

while True:
    x=int(input('Enter choice:'))
    if x==1:
        name=input('Enter name of model: ')
        fuel=input('Enter Fuel type: ')
        engine=input('Enter Engine type: ')
        mileage=int(input('Enter Mileage: '))
        price=int(input('Enter the sales price: '))
        stock=int(input('Enter the stock: '))
        mycur.execute('''INSERT INTO MODEL (NAME, FUEL_TYPE, ENGINE_TYPE, MILEAGE, SALES_PRICE, STOCK)
        VALUES (:1,:2,:3,:4,:5,:6)''', (name, fuel, engine, mileage, price, stock))
        mydb.commit()
        mycur.execute('select max(MODEL_ID) from MODEL')
        for k in mycur: x=k[0]
        print('Model is entered with Model_ID',x)
    elif x==2:
        status='AVAILABLE'
        colour=input('Enter colour of the car: ')
        dom=input('Enter the Date of Manufacture(dd-mon-yy): ')
        rent=int(input('Enter rent Price: '))
        id=int(input('Enter Model_ID: '))
        try:
            mycur.execute('''INSERT INTO VEHICLE (VEHICAL_STATUS, COLOUR, DOM, RENT_PRICE, MODEL_ID)
        VALUES ( :1,:2,:3,:4,:5)''',(status,colour,dom,rent,id))
            mydb.commit()
            mycur.execute('select max(VEHICLE_ID) from VEHICLE')
            for k in mycur: x=k[0]
            print('Vehicle is entered with VEHICLE_ID',x)
        except:
            print('Invalid Model_ID')
    elif x==3:
        ml=input('Enter membership level: ')
        p=0; ls=input('Enter Lisence_no: ')
        name=input('Enter Name: ')
        ph=int(input('Enter Mobile Number: '))
        em=input('Enter Email: ')
        add=input('Enter Address: ')
        mycur.execute('''INSERT INTO CUSTOMER (MEMBER_LEVEL, POINTS, LICENSE_NO, NAME, MOBILE,
                      EMAIL, ADDRESS) VALUES (:1,:2,:3,:4,:5,:6,:7)''',(ml,p,ls,name,ph,em,add))
        mydb.commit()
        mycur.execute('select max(CUSTOMER_ID) from CUSTOMER')
        for k in mycur: x=k[0]
        print('Customer is entered with CUSTOMER_ID',x)
    elif x==4:
         print('The Cars that are available')
         h=['MODEL_ID','NAME','FUEL_TYPE','ENGINE_TYPE','MILEAGE','SALES_PRICE','STOCK']
         mycur.execute('SELECT * FROM MODEL WHERE STOCK>0')
         L=[]
         for k in mycur:
             l=[]
             for j in k: l+=[j]
             L+=[l]
         print(tabulate.tabulate(L,h,tablefmt='github'))
         mid=int(input('Enter MODEL_ID: '))
         mycur.execute('select FEATURE_ID, NAME, COST from FEATURES WHERE MODEL_ID=:1',(mid,))
         h=['Feature_ID','Feature','Cost']; L=[]
         for k in mycur:
             l=[]
             for j in k:l+=[j]
             L+=[l]
         print(tabulate.tabulate(L,h,tablefmt='github'))
         mycur.execute('SELECT SALES_PRICE FROM MODEL WHERE MODEL_ID=:1',(mid,))
         l=[]
         while True:
             f=input('Do you want any add-on features(Y/N): ')
             if f in 'Yy':
                 l+=[int(input('Enter Feature_ID: '))]
             elif f in 'nN': break
             else: print('Invalid Input')
         for k in mycur: cost=k[0]
         for k in l:
             mycur.execute('SELECT COST from FEATURES WHERE FEATURE_ID=:1',(k,))
             for j in mycur: cost+=j[0]
         dis=int(input('Enter Discount if any: '))
         type='PURCHASE'; refund=0;
         date=input("Enter today's date: ")
         met=input("Enter payment methord: ")
         cid=int(input("Enter customer_ID: "))
         mycur.execute('''INSERT INTO Transaction (Discount, Type ,Refund, DOT, Amount,
             Method, Model_ID, Customer_ID)
             VALUES (:1,:2,:3,:4,:5,:6,:7,:8)''',(dis,type,refund,date,cost,met,mid,cid))
         print('Total cost:',cost-(cost*dis/100))
         mydb.commit()
    elif x==5:
         print('The Cars that are available')
         h=['VEHICLE_ID','NAME','PRICE']
         mycur.execute('''SELECT V.MODEL_ID,V.VEHICLE_ID,NAME,RENT_PRICE  FROM VEHICLE V, MODEL M
                       WHERE V.MODEL_ID=M.MODEL_ID AND VEHICAL_STATUS='AVAILABLE' ''')
         L=[]
         for k in mycur:
             l=[]
             for j in k: l+=[j]
             L+=[l]
         print(tabulate.tabulate(L,h,tablefmt='github'))
         mid=int(input('Enter the Model_ID: '))
         vid=int(input('Enter the Vehicle_ID: '))
         date=input("Enter date you want to book for: ")
         d=int(input('Enter duration in days: '))
         cid=int(input('Enter customer_ID: '))
         dis=int(input('Enter Discount if any: '))
         refund=0;
         d1=input("Enter today's date: ")
         met=input("Enter payment methord: ")
         mycur.execute('SELECT RENT_PRICE FROM VEHICLE WHERE VEHICLE_ID=:1',(vid,))
         for k in mycur: cost=k[0]
         mycur.execute('''INSERT INTO Transaction (Discount, Type ,Refund, DOT, Amount,
             Method,MODEL_ID,Customer_ID)
             VALUES (:1,:2,:3,:4,:5,:6,:7,:8)''',(dis,'RENTAL',refund,date,cost,met,mid,cid))
         mycur.execute('select max(TRANSACTION_ID) from TRANSACTION')
         for k in mycur: tid=k[0]
         mycur.execute('''UPDATE VEHICLE SET VEHICAL_STATUS='BOOKED' WHERE VEHICLE_ID=:1''',(vid,))
         mycur.execute('''INSERT INTO RENTAL (RENT_STATUS,DURATION,PICKUP_DATE_SCHEDULED,
TRANSACTION_ID,VEHICLE_ID,CUSTOMER_ID) VALUES ('BOOKED',:1,:2,:3,:4,:5)''',(d,d1,tid,vid,cid))
         print('Total cost:',(cost-(d*cost/100))*24)
         mydb.commit()
         mycur.execute('select max(RENTAL_ID) from RENTAL')
         for k in mycur: x=k[0]
         print('Record is entered with RENTAL_ID',x)
    elif x==6:
        rid=int(input('Enter the rental_ID: '))
        date=input("Enter today's date: ")
        d2=input('Enter date of return: ')
        mycur.execute('''UPDATE RENTAL SET RENT_STATUS='RENTED',
        PickUp_Date_Actual=:1, Dropoff_Date_Scheduled=:2 WHERE RENTAL_ID = :3''',(date,d2,rid))
        mydb.commit()
        print("Rental car picked up successfully.")
    elif x==7:
        rid=int(input('Enter the rental_ID: '))
        date=input("Enter today's date: ")
        mycur.execute('''UPDATE RENTAL SET RENT_STATUS='RETURNED',
        Dropoff_Date_Actual=:1 WHERE RENTAL_ID = :2''',(date,rid))
        mydb.commit()
        print("Rental car is returned successfully")
    elif x==8:
        rid=int(input('Enter the VEHICLE_ID: '))
        mycur.execute('''UPDATE VEHICLE SET VEHICAL_STATUS='MAINTENANCE'
        WHERE VEHICLE_ID = :1''',(rid,))
        mydb.commit()
        print("Rental car picked up successfully for maintainence.")
    elif x==9:
         mycur.execute('SELECT SUM(AMOUNT) FROM TRANSACTION')
         for k in mycur: x=k[0]
         print('Total sales:',x)
    elif x==10:
         vid=int(input('Enter vehicle_id: '))
         mycur.execute('SELECT * FROM RENTAL WHERE VEHICLE_ID=:1',(vid,))
         for k in mycur:
             for j in k: print(j, end=',')
             print()
    elif x==11:
        mycur.execute('SELECT * FROM CUSTOMER')
        L=[]
        for k in mycur:
             l=[]
             for j in k: l+=[j]
             L+=[l]
        print(tabulate.tabulate(L,tablefmt='github'))
    elif x==12:
        ll=int(input('Enter lower bound: '))
        ul=int(input('Enter the upper bound: '))
        h=['VEHICLE_ID','VEHICAL_STATUS','COLOUR','DOM','RENT_PRICE','MODEL_ID','NAME']
        mycur.execute('''SELECT V.*,NAME FROM VEHICLE V,
        MODEL M WHERE V.MODEL_ID=M.MODEL_ID AND RENT_PRICE>:1 AND RENT_PRICE<:2''',(ll,ul))
        L=[]
        for k in mycur:
            l=[]
            for j in k: l+=[j]
            L+=[l]
        print(tabulate.tabulate(L,h,tablefmt='github'))
    elif x==13:
        ll=int(input('Enter lower bound: '))
        ul=int(input('Enter the upper bound: '))
        mycur.execute('SELECT * FROM MODEL WHERE SALES_PRICE>:1 AND SALES_PRICE<:2',(ll,ul))
        h=['MODEL_ID','NAME','FUEL_TYPE','ENGINE_TYPE','MILEAGE','SALES_PRICE','STOCK']
        L=[]
        for k in mycur:
            l=[]
            for j in k: l+=[j]
            L+=[l]
        print(tabulate.tabulate(L,h,tablefmt='github'))
    elif x==14:
        m=input('Enter membership level: ')
        h=['CUSTOMER_ID','MEMBER_LEVEL','POINTS','LICENSE_NO','NAME','MOBILE','EMAIL','ADDRESS']
        mycur.execute('SELECT * FROM CUSTOMER WHERE MEMBER_LEVEL=:1',(m,))
        L=[]
        for k in mycur:
            l=[]
            for j in k:l+=[j]
            L+=[l]
        print(tabulate.tabulate(L,h,tablefmt='github'))
    elif x==15:
        mid=int(input('Enter the MODEL_ID: '))
        s=int(input('Enter how much stock needs to be incresed: '))
        mycur.execute('''UPDATE MODEL SET STOCK=STOCK+:1
        WHERE MODEL_ID = :2''',(s,mid))
        mydb.commit()
        print("Stock has successfully been updated.")
    elif x==16:
        cid=int(input('Enter the CUSTOMER_ID: '))
        l=input('Enter the new Membership level: ')
        mycur.execute('''UPDATE CUSTOMER SET MEMBER_LEVEL=:1
        WHERE CUSTOMER_ID=:2''',(l,cid))
        mydb.commit()
        print("Membership level has been updated")
    elif x==17:
        h=['MODEL_ID', 'NAME', 'FUEL_TYPE', 'ENGINE_TYPE', 'MILEAGE', 'SALES_PRICE', 'STOCK']
        mycur.execute('SELECT * FROM MODEL WHERE STOCK>0')
        L=[]
        for k in mycur:
           l=[]
           for j in k: l+=[j]
           L+=[l]
        print(tabulate.tabulate(L,h,tablefmt='github'))
    elif x==18:
         h=['MODEL_ID','VEHICLE_ID','NAME','PRICE']
         mycur.execute('''SELECT V.MODEL_ID,V.VEHICLE_ID,NAME,RENT_PRICE  FROM VEHICLE V, MODEL M
                       WHERE V.MODEL_ID=M.MODEL_ID AND VEHICAL_STATUS='AVAILABLE' ''')
         L=[]
         for k in mycur:
             l=[]
             for j in k: l+=[j]
             L+=[l]
         print(tabulate.tabulate(L,h,tablefmt='github'))
    elif x==19:
        mid=int(input('Enter the model_id: '))
        a='y'
        while a in 'yY':
            n=input('Enter name of the feature: ')
            c=int(input('Enter cost of the feature: '))
            mycur.execute('INSERT INTO FEATURES(MODEL_ID,NAME,COST) VALUES(:1,:2,:3)',(mid,n,c))
            mydb.commit()
            mycur.execute('select max(FEATURE_ID) from FEATURES')
            for k in mycur: x=k[0]
            print('Feature is entered with FEATURE_ID',x)
            a=input('Do you want to add another feature(y/n):')
            if a in 'nN': break
    elif x==20:
        rid=int(input('Enter the VEHICLE_ID: '))
        mycur.execute('''UPDATE VEHICLE SET VEHICAL_STATUS='AVAILABLE'
        WHERE VEHICLE_ID = :1''',(rid,))
        mydb.commit()
        print("Rental car returned.")
    elif x==21:
         print('Exiting...')
         break
    else:
         print('Invalid Input')
