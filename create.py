import oracledb
#pw=input('Enter the Password')
mydb=oracledb.connect(user="system",host="localhost",password='Vaidehi')
mycur=mydb.cursor()

#Creating the sequences required for primary keys
mycur.execute('create sequence MODEL_NO increment by 1 start with 1000 maxvalue 2000 minvalue 1000')
mycur.execute('create sequence VEHICLE_NO increment by 1 start with 2000 maxvalue 3000 minvalue 2000')
mycur.execute('create sequence CUSTOMER_NO increment by 1 start with 3000 maxvalue 4000 minvalue 3000')
mycur.execute('create sequence TRANSACTION_NO increment by 1 start with 4000 maxvalue 5000 minvalue 4000')
mycur.execute('create sequence RENTAL_NO increment by 1 start with 5000 maxvalue 6000 minvalue 5000')
mycur.execute('create sequence FEATURE_NO increment by 1 start with 6000 maxvalue 7000 minvalue 6000')


#Creating the tables
mycur.execute('''create table MODEL (MODEL_ID int DEFAULT MODEL_NO.nextval primary key,
NAME varchar(100), FUEL_TYPE varchar(50),ENGINE_TYPE varchar(50),MILEAGE decimal(10,2), SALES_PRICE decimal(10,2),
STOCK int, constraint CHK_MILEAGE check (MILEAGE>=0), constraint CHK_SALES_PRICE check (SALES_PRICE>=0),
constraint CHK_STOCK check (STOCK>=0))''')

mycur.execute('''create table VEHICLE (VEHICLE_ID int DEFAULT VEHICLE_NO.nextval primary key,
VEHICAL_STATUS varchar(20), COLOUR varchar(50), DOM date, RENT_PRICE decimal(10,2), MODEL_ID int,
constraint CHK_STATUS check (VEHICAL_STATUS in ('RENTED', 'AVAILABLE', 'MAINTENANCE', 'BOOKED')),
constraint CHK_RENT_PRICE check (RENT_PRICE>=0), foreign key(MODEL_ID) references MODEL(MODEL_ID))''')

mycur.execute('''create table CUSTOMER (CUSTOMER_ID int DEFAULT CUSTOMER_NO.nextval primary key,
MEMBER_LEVEL varchar(50), POINTS int,LICENSE_NO varchar(100),NAME varchar(100), MOBILE varchar(20) unique,
EMAIL varchar(100) unique, ADDRESS varchar(255) , constraint CHK_POINTS check (POINTS>=0))''')

mycur.execute('''create table TRANSACTION (TRANSACTION_ID int DEFAULT TRANSACTION_NO.nextval primary key,
DISCOUNT decimal(10,2),TYPE varchar(50),REFUND decimal(10,2),DOT date, AMOUNT decimal(10,2),METHOD varchar(50),
MODEL_ID int,CUSTOMER_ID int, constraint CHK_DISCOUNT check (DISCOUNT>=0),constraint CHK_REFUND check (REFUND>=0),
constraint CHK_AMOUNT check (AMOUNT>=0), constraint CHK_TYPE check (TYPE IN ('PURCHASE', 'RENTAL', 'RESALE')),
foreign key(MODEL_ID) references MODEL(MODEL_ID), foreign key(CUSTOMER_ID) references CUSTOMER(CUSTOMER_ID))''')

mycur.execute('''create table RENTAL (RENTAL_ID int DEFAULT RENTAL_NO.nextval primary key,
RENT_STATUS varchar(50),DURATION int, PICKUP_DATE_ACTUAL date, PICKUP_DATE_SCHEDULED date,
DROPOFF_DATE_ACTUAL date, DROPOFF_DATE_SCHEDULED date,TRANSACTION_ID int,VEHICLE_ID int,CUSTOMER_ID int,
constraint CHK_DURATION check (DURATION > 0), constraint CHK_ST check (RENT_STATUS IN ('RETURNED', 'RENTED',
'BOOKED','DAMAGED')), foreign key (TRANSACTION_ID) references TRANSACTION(TRANSACTION_ID),
foreign key (VEHICLE_ID) references VEHICLE(VEHICLE_ID), foreign key (CUSTOMER_ID) references
CUSTOMER(CUSTOMER_ID))''')

mycur.execute('''Create table FEATURES ( FEATURE_ID int , MODEL_ID int, NAME varchar(100), COST decimal(10,2),
CONSTRAINT fk_model_id FOREIGN KEY (MODEL_ID) REFERENCES MODEL(MODEL_ID))''')

#END OF FILE 1 (used for creating the structure)
