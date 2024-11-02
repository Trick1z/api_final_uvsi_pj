from typing import Union
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Response,status
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

import mysql.connector  # type: ignore
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
import os

from dateutil import parser
import pytz

load_dotenv()



# get DB
def get_DB():
    # connector = mysql.connector.connect(
    #     host=os.getenv("MYSQL_HOST"),
    #     user=os.getenv("MYSQL_username"),
    #     database=os.getenv("MYSQL_DATABASE"),
    # )
    
    connector = mysql.connector.connect(
        host= 'blista7kyg5hyq8lrlyp-mysql.services.clever-cloud.com',
        user='urgnzyqi63dc81zs',
        password = 'bgMpfvaqJi9qBRXwZejS',
        database='blista7kyg5hyq8lrlyp'
    )
    
    

    return connector


app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:4200"],  # Angular's dev server runs on port 4200
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://project-test-4300d.web.app"],  # Angular's dev server runs on port 4200
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["https://final-example-vuzz.onrender.com"],  # ระบุโดเมนที่อนุญาต
#     allow_credentials=True,
#     allow_methods=["*"],  # อนุญาตทุกวิธี
#     allow_headers=["*"],  # อนุญาตทุก Header
# )




# test get

# @app.get("/testdb")
# def get_test():
#     cnx = get_DB()
#     cursor = cnx.cursor()
#     query = "SELECT * FROM test WHERE del_frag = 'N'"
#     cursor.execute(query)

#     rows = cursor.fetchall()
#     cursor.close()
#     cnx.close()

#     lst = []

#     for row in rows:
#         lst.append({
#             "id" : row[0],
#             "name" : row[1],
#             "age" : row[2],
#             "create_date" : row[3]
#         })

#     return lst


# #test post
# class test(BaseModel):
#     CATEGORY_NAME :str
#     CATEGORY_DESCRIPTION :str
#     RECORD_STATUS :str
#     DEL_FLAG :str
#     CREATE_DATE : datetime
#     UPDATE_DATE : datetime

# @app.post("/testadd")
# async def add(test : test):
#     test.RECORD_STATUS = 'A'
#     test.DEL_FLAG = 'N'

#     cnx = get_DB()
#     cursor = cnx.cursor()

#     # query = "INSERT INTO test (CA) VALUES ( %s ,%s,%s,%s)"
#     query ="INSERT INTO category (CATEGORY_NAME ,CATEGORY_DESCRIPTION ,RECORD_STATUS,DEL_FRAG,CREATE_DATE ,UPDATE_DATE) VALUES ( %s ,%s,%s,%s,%s,%s)"
#     cursor.execute(query,(test.CATEGORY_NAME , test.CATEGORY_DESCRIPTION ,test.RECORD_STATUS,test.DEL_FLAG, test.CREATE_DATE ,test.UPDATE_DATE,))

#     cnx.commit()
#     test_id = cursor.lastrowid
#     cursor.close()
#     cnx.close()

#     return {"id" : test_id , "status" : 200 }


# #test del by put


# @app.put("/put_test/{id}")
# async def del_test(id: int):

#     cnx = get_DB()
#     cursor = cnx.cursor()


#     sql_update_query = "UPDATE test SET del_frag = %s WHERE id = %s"
#     cursor.execute(sql_update_query, ('Y', id))

#     cnx.commit()
#     cursor.close()
#     cnx.close()

#     return {"id" : id , "Status" : '200'}

# # test del
# @app.delete("/delete/{id}")
# async def dele(id: int):

#     cnx = get_DB()
#     cursor = cnx.cursor()

#     query = "DELETE FROM test WHERE id = %s"
#     cursor.execute(query, (id,))  # ส่ง item_id เป็น tuple

#     cnx.commit()
#     cursor.close()
#     cnx.close()

#     return {"id" : id , "Status" : '200'}


# -------------------------------------------------------CODE HERE ----------------------------------

# -----------------------------------------------------[POST] CATEGORY---------------------------------------


class add_category(BaseModel):
    CATEGORY_NAME: str
    CATEGORY_DESCRIPTION: str
    RECORD_STATUS: str
    DEL_FRAG: str
    CREATE_DATE: datetime
    UPDATE_DATE: datetime


@app.post("/add_category")
async def add_category(data: add_category):
    data.RECORD_STATUS = "A"
    data.DEL_FRAG = "N"

    CREATE_DATE = datetime.now()
    UPDATE_DATE = datetime.now()

    cnx = get_DB()
    cursor = cnx.cursor()

    query = "INSERT INTO category (CATEGORY_NAME ,CATEGORY_DESCRIPTION ,RECORD_STATUS,DEL_FRAG,CREATE_DATE ,UPDATE_DATE) VALUES ( %s ,%s,%s,%s,%s,%s)"
    cursor.execute(
        query,
        (
            data.CATEGORY_NAME,
            data.CATEGORY_DESCRIPTION,
            data.RECORD_STATUS,
            data.DEL_FRAG,
            CREATE_DATE,
            UPDATE_DATE,
        ),
    )

    cnx.commit()
    test_id = cursor.lastrowid
    cursor.close()
    cnx.close()

    return {"id": test_id, "status": 200}


# -----------------------------------------------------END [POST] CATEGORY ---------------------------------------

# -----------------------------------------------------[GET] CATEGORY---------------------------------------


@app.get("/get_category")
def get_category(): 
    cnx = get_DB()
    cursor = cnx.cursor()
    query = "SELECT * FROM category WHERE del_frag = 'N' and RECORD_STATUS = 'A';"
    cursor.execute(query)

    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    lst = []

    for row in rows:
        lst.append(
            {
                "CATEGORY_ID": row[0],
                "CATEGORY_NAME": row[1],
                "CATEGORY_DESCRIPTION": row[2],
                "RECORD_STATUS": row[3],
                "CREATE_DATE": row[5],
                "UPDATE_DATE": row[6],
            }
        )

    return lst


# ----------------------------------------------------- END [GET] CATEGORY---------------------------------------


# ----------------------------------------------------- [PUT_DATA] CATEGORY---------------------------------------
class putCategory(BaseModel):
    CATEGORY_NAME: str
    CATEGORY_DESCRIPTION: str


@app.put("/put_catedory/{id}")
async def put_del_category(id: int, data: putCategory):

    update_time = datetime.now()

    cnx = get_DB()
    cursor = cnx.cursor()

    sql_update_query = "UPDATE category SET CATEGORY_NAME = %s ,CATEGORY_DESCRIPTION = %s,UPDATE_DATE =%s WHERE CATEGORY_ID = %s"
    cursor.execute(
        sql_update_query,
        (data.CATEGORY_NAME, data.CATEGORY_DESCRIPTION, update_time, id),
    )

    cnx.commit()
    cursor.close()
    cnx.close()

    return {"id": id, "Status": "200"}


# ----------------------------------------------------- END [PUT_DATA] CATEGORY---------------------------------------


# ----------------------------------------------------- [PUTDEL] CATEGORY--------------------------------------
@app.put("/put_del_category/{id}")
async def put_del_category(id: int):

    update_time = datetime.now()

    cnx = get_DB()
    cursor = cnx.cursor()

    sql_update_query = (
        "UPDATE category SET del_frag = %s ,UPDATE_DATE = %s WHERE CATEGORY_ID = %s"
    )
    cursor.execute(sql_update_query, ("Y", update_time, id))

    cnx.commit()
    cursor.close()
    cnx.close()

    return {"id": id, "Status": "200"}


# ----------------------------------------------------- END [PUTDEL] CATEGORY--------------------------------------


# ----------------------------------------------------- [DELETE] CATEGORY--------------------------------------
@app.delete("/delete_category/{id}")
def delete_category(id: int):
    cnx = get_DB()
    cursor = cnx.cursor()

    query = "DELETE FROM category WHERE CATEGORY_ID = %s"
    cursor.execute(query, (id,))
    cnx.commit()
    cursor.close()
    cnx.close()

    return {"status": 200, "description": "done", "id": id}


# ----------------------------------------------------- END [DELETE] CATEGORY---------------------------------------
#
#
#
#
#
#
#
#
#
#
# -----------------------------------------------------[POST] STATUS---------------------------------------
class add_status(BaseModel):
    STATUS_NAME: str
    STATUS_DESCRIPTION: str
    RECORD_STATUS: str
    DEL_FRAG: str
    CREATE_DATE: datetime
    UPDATE_DATE: datetime


@app.post("/add_status")
async def add_status(data: add_status):
    data.RECORD_STATUS = "A"
    data.DEL_FRAG = "N"

    CREATE_DATE = datetime.now()
    UPDATE_DATE = datetime.now()

    cnx = get_DB()
    cursor = cnx.cursor()

    query = "INSERT INTO status (STATUS_NAME ,STATUS_DESCRIPTION ,RECORD_STATUS,DEL_FRAG,CREATE_DATE ,UPDATE_DATE) VALUES ( %s ,%s,%s,%s,%s,%s)"
    cursor.execute(
        query,
        (
            data.STATUS_NAME,
            data.STATUS_DESCRIPTION,
            data.RECORD_STATUS,
            data.DEL_FRAG,
            CREATE_DATE,
            UPDATE_DATE,
        ),
    )

    cnx.commit()
    test_id = cursor.lastrowid
    cursor.close()
    cnx.close()

    return {"id": test_id, "status": 200}


# -----------------------------------------------------END [POST] STATUS ---------------------------------------
# -----------------------------------------------------[GET] STATUS---------------------------------------


@app.get("/get_status")
def get_test():
    cnx = get_DB()
    cursor = cnx.cursor()
    query = "SELECT * FROM status WHERE del_frag = 'N' and RECORD_STATUS ='A'"
    cursor.execute(query)

    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    lst = []

    for row in rows:
        lst.append(
            {
                "STATUS_ID": row[0],
                "STATUS_NAME": row[1],
                "STATUS_DESCRIPTION": row[2],
                "RECORD_STATUS": row[3],
                "CREATE_DATE": row[5],
                "UPDATE_DATE": row[6],
            }
        )

    return lst


# ----------------------------------------------------- END [GET] STATUS---------------------------------------

# -----------------------------------------------------  [PUTDEL] STATUS---------------------------------------


@app.put("/put_del_status/{id}")
async def put_del_status(id: int):
    update_time = datetime.now()
    cnx = get_DB()
    cursor = cnx.cursor()

    sql_update_query = (
        "UPDATE status SET del_frag = %s , UPDATE_DATE = %s WHERE STATUS_ID = %s"
    )
    cursor.execute(sql_update_query, ("Y", update_time, id))

    cnx.commit()
    cursor.close()
    cnx.close()

    return {"id": id, "Status": "200"}


# ----------------------------------------------------- END [PUTDEL] STATUS---------------------------------------


# ----------------------------------------------------- [PUT_DATA] STATUS---------------------------------------
class putCategory(BaseModel):
    STATUS_NAME: str
    STATUS_DESCRIPTION: str


@app.put("/put_status/{id}")
async def put_status(id: int, data: putCategory):
    update_time = datetime.now()
    cnx = get_DB()
    cursor = cnx.cursor()

    sql_update_query = "UPDATE status SET STATUS_NAME = %s ,STATUS_DESCRIPTION = %s,UPDATE_DATE = %s  WHERE STATUS_ID = %s"
    cursor.execute(
        sql_update_query, (data.STATUS_NAME, data.STATUS_DESCRIPTION, update_time, id)
    )

    cnx.commit()
    cursor.close()
    cnx.close()

    return {"id": id, "Status": "200"}


# ----------------------------------------------------- END [PUT_DATA] STATUS---------------------------------------
#
#
#
#
#
#
#
#
#
#
# -----------------------------------------------------[GET] PRODUCT ---------------------------------------


@app.get("/get_product")
def get_test():
    cnx = get_DB()
    cursor = cnx.cursor()
    # query = "SELECT * FROM product WHERE del_frag = 'N'"
    query = "SELECT * FROM product WHERE del_frag = 'N' and RECORD_STATUS = 'A'; "
    cursor.execute(query)

    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    lst = []

    for row in rows:
        lst.append(
            {
                "P_ID": row[0],
                "P_NAME": row[1],
                "P_DESCRIPTION": row[2],
                "P_DOP": row[3],
                "P_PRICE": row[4],
                "P_SERIALNUMBER": row[5],
                "P_EQUIPMENTNUMBER": row[6],
                "P_BAND": row[7],
                "CATEGORY_ID": row[8],
                "STATUS_ID": row[9],
                "STUDENT_ID": row[10],
                "RECORD_STATUS": row[11],
                "DEL_FRAG": row[12],
                "CREATE_DATE": row[13],
                "UPDATE_DATE": row[14],
            }
        )

    return lst


# ----------------------------------------------------- END [GET] PRODUCT---------------------------------------

# -----------------------------------------------------[GET] PRODUCT BY CATEGORY ID---------------------------------------


@app.get("/get_product/status")
def get_test():
    cnx = get_DB()
    cursor = cnx.cursor()
    query = "SELECT * FROM product WHERE del_frag = 'N' and STATUS_ID = 6 and RECORD_STATUS = 'A';  "  # หา product ที่่ว่าง
    cursor.execute(query)

    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    lst = []

    for row in rows:
        lst.append(
            {
                "P_ID": row[0],
                "P_NAME": row[1],
                "P_DESCRIPTION": row[2],
                "P_DOP": row[3],
                "P_PRICE": row[4],
                "P_SERIALNUMBER": row[5],
                "P_EQUIPMENTNUMBER": row[6],
                "P_BAND": row[7],
                "CATEGORY_ID": row[8],
                "STATUS_ID": row[9],
                "STUDENT_ID": row[10],
                "RECORD_STATUS": row[11],
                "DEL_FRAG": row[12],
                "CREATE_DATE": row[13],
                "UPDATE_DATE": row[14],
            }
        )

    return lst


# ----------------------------------------------------- END [GET] PRODUCT BY CATEGORY ID---------------------------------------


# hit add BTN
class param(BaseModel):
    text: str


@app.put("/put_waitProduct/{id}")
async def put_status(id: int, param: param):

    wait = param.text

    cnx = get_DB()
    cursor = cnx.cursor()

    sql_update_query = """UPDATE product SET 
                        RECORD_STATUS = %s 
                        WHERE P_ID = %s
                        """
    cursor.execute(
        sql_update_query,
        (
            wait,
            id,
        ),
    )

    cnx.commit()
    cursor.close()
    cnx.close()

    return {"id": id, "Status": "200"}


# hit delete on add  BTN

# @app.put("/put_readyProduct/{id}")
# async def put_status(id: int):

#     wait = 'A'

#     cnx = get_DB()
#     cursor = cnx.cursor()

#     sql_update_query = '''UPDATE product SET
#                         RECORD_STATUS = %s
#                         WHERE P_ID = %s
#                         '''
#     cursor.execute(sql_update_query, (wait ,id,))

#     cnx.commit()
#     cursor.close()
#     cnx.close()

#     return {"id" : id , "Status" : '200'}


# -----------------------------------------------------[GET] PRODUCT BY P_ID ---------------------------------------


@app.get("/get_product/{id}")
def get_test(id: int):
    cnx = get_DB()
    cursor = cnx.cursor()
    query = "SELECT * FROM product WHERE P_ID = %s and RECORD_STATUS = 'A' and DEL_FRAG = 'N'"
    cursor.execute(query, (id,))

    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    lst = []

    for row in rows:
        lst.append(
            {
                "P_ID": row[0],
                "P_NAME": row[1],
                "P_DESCRIPTION": row[2],
                "P_DOP": row[3],
                "P_PRICE": row[4],
                "P_SERIALNUMBER": row[5],
                "P_EQUIPMENTNUMBER": row[6],
                "P_BAND": row[7],
                "CATEGORY_ID": row[8],
                "STATUS_ID": row[9],
                "STUDENT_ID": row[10],
                "RECORD_STATUS": row[11],
                "DEL_FRAG": row[12],
                "CREATE_DATE": row[13],
                "UPDATE_DATE": row[14],
            }
        )

    return lst


# -----------------------------------------------------END[GET] PRODUCT BY ID ---------------------------------------


# -----------------------------------------------------[POST] PRODUCT ---------------------------------------
class add_product(BaseModel):

    P_NAME: str
    CATEGORY_ID: int
    STATUS_ID: int
    P_PRICE: int
    P_DOP: str
    P_BAND: str
    P_SERIALNUMBER: str
    P_EQUIPMENTNUMBER: str
    P_DESCRIPTION: str
    STUDENT_ID: int
    RECORD_STATUS: str
    DEL_FRAG: str
    CREATE_DATE: datetime
    UPDATE_DATE: datetime


@app.post("/add_product")
async def add_product(data: add_product):
    data.RECORD_STATUS = "A"
    data.DEL_FRAG = "N"
    dop = data.P_DOP
    
    def convertTime(date:String):
        utc_time = parser.isoparse(date)

        # ตั้งค่า timezone เป็น UTC
        utc_time = utc_time.replace(tzinfo=pytz.UTC)

        # แปลงเป็น timezone ที่ต้องการ (เช่น เวลาประเทศไทย)
        local_time = utc_time.astimezone(pytz.timezone("Asia/Bangkok"))
        
        return local_time
        
    res_dop = convertTime(dop)
    
    CREATE_DATE = datetime.now()
    UPDATE_DATE = datetime.now()

    cnx = get_DB()
    cursor = cnx.cursor()

    query = "INSERT INTO product (P_NAME ,CATEGORY_ID,STATUS_ID,P_PRICE,P_DOP,P_BAND,P_SERIALNUMBER,P_EQUIPMENTNUMBER,P_DESCRIPTION,STUDENT_ID,RECORD_STATUS,DEL_FRAG,CREATE_DATE ,UPDATE_DATE) VALUES ( %s ,%s,%s,%s,%s,%s,%s ,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(
        query,
        (
            data.P_NAME,
            data.CATEGORY_ID,
            data.STATUS_ID,
            data.P_PRICE,
            res_dop,
            data.P_BAND,
            data.P_SERIALNUMBER,
            data.P_EQUIPMENTNUMBER,
            data.P_DESCRIPTION,
            data.STUDENT_ID,
            data.RECORD_STATUS,
            data.DEL_FRAG,
            CREATE_DATE,
            UPDATE_DATE,
        ),
    )

    cnx.commit()
    test_id = cursor.lastrowid
    cursor.close()
    cnx.close()

    return {"id": test_id, "status": 200}


# ----------------------------------------------------- END [POST] PRODUCT ---------------------------------------


# ----------------------------------------------------- [PUT_DATA] PRODUCT---------------------------------------
class putProduct(BaseModel):
    P_NAME: str
    P_DESCRIPTION: str
    P_DOP: str
    P_PRICE: int
    P_SERIALNUMBER: str
    P_EQUIPMENTNUMBER: str
    P_BAND: str
    CATEGORY_ID: int
    STATUS_ID: int
    UPDATE_DATE: datetime


@app.put("/put_product/{id}")
async def put_status(id: int, data: putProduct):
    # def convertTime(date:String):
    #     utc_time = parser.isoparse(date)

    #     # ตั้งค่า timezone เป็น UTC
    #     utc_time = utc_time.replace(tzinfo=pytz.UTC)

    #     # แปลงเป็น timezone ที่ต้องการ (เช่น เวลาประเทศไทย)
    #     local_time = utc_time.astimezone(pytz.timezone("Asia/Bangkok"))
        
    #     return local_time
    
    

    update_time = datetime.now()
    cnx = get_DB()
    cursor = cnx.cursor()
    
    # res_dop = convertTime(data.P_DOP)
    
    

    sql_update_query = """
    UPDATE product SET 
    P_NAME = %s ,P_DESCRIPTION = %s ,P_DOP = %s,
    P_PRICE =%s ,P_SERIALNUMBER = %s, P_EQUIPMENTNUMBER = %s,P_BAND = %s,
    CATEGORY_ID =%s ,STATUS_ID = %s,
    UPDATE_DATE = %s
    WHERE P_ID = %s
    """
    cursor.execute(
        sql_update_query,
        (
            data.P_NAME,
            data.P_DESCRIPTION,
            data.P_DOP,
            data.P_PRICE,
            data.P_SERIALNUMBER,
            data.P_EQUIPMENTNUMBER,
            data.P_BAND,
            data.CATEGORY_ID,
            data.STATUS_ID,
            update_time,
            id
        ),
    )

    cnx.commit()
    cursor.close()
    cnx.close()

    return {"id": id, "Status": "200"}


# ----------------------------------------------------- END [PUT_DATA] PRODUCT---------------------------------------

# -----------------------------------------------------  [PUTDEL] PRODUCT---------------------------------------


@app.put("/put_del_product/{id}")
async def put_del_product(id: int):
    update_time = datetime.now()
    cnx = get_DB()
    cursor = cnx.cursor()

    sql_update_query = (
        "UPDATE product SET del_frag = %s , UPDATE_DATE = %s WHERE P_ID = %s"
    )
    cursor.execute(sql_update_query, ("Y", update_time, id))

    cnx.commit()
    cursor.close()
    cnx.close()

    return {"id": id, "Status": "200"}


# ----------------------------------------------------- END [PUTDEL] PRODUCT---------------------------------------

# -----------------------------------------------------[GET] STUDENT ---------------------------------------


@app.get("/get_student")
def get_student():
    cnx = get_DB()
    cursor = cnx.cursor()
    query = "SELECT * FROM student WHERE del_frag = 'N' and RECORD_STATUS = 'A'"
    cursor.execute(query)

    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    lst = []

    for row in rows:
        lst.append(
            {
                "STUDENT_ID": row[0],
                "STUDENT_NAME": row[1],
                "STUDENT_CODE": row[2],
                "STUDENT_YEAR": row[3],
                "STUDENT_FACULTY": row[4],
                "STUDENT_MAJOR": row[5],
                "RECORD_STATUS": row[6],
                "DEL_FRAG": row[7],
                "CREATE_DATE": row[8],
                "UPDATE_DATE": row[9],
            }
        )

    return lst


# -----------------------------------------------------END [GET] STUDENT ---------------------------------------

# -----------------------------------------------------[GET] BY CODE STUDENT ---------------------------------------


@app.get("/get_student/{code}")
def get_student(code: str):
    cnx = get_DB()
    cursor = cnx.cursor()
    query = "SELECT * FROM student WHERE STUDENT_CODE = %s and RECORD_STATUS = 'A'"
    cursor.execute(query, (code,))

    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    lst = []

    if not rows:  # ถ้าไม่มีข้อมูล
        return {"status": 404, "error": "Student not found."}

    for row in rows:
        lst.append(
            {
                "STUDENT_ID": row[0],
                "STUDENT_NAME": row[1],
                "STUDENT_CODE": row[2],
                "STUDENT_YEAR": row[3],
                "STUDENT_FACULTY": row[4],
                "STUDENT_MAJOR": row[5],
                "RECORD_STATUS": row[6],
                "DEL_FRAG": row[7],
                "CREATE_DATE": row[8],
                "UPDATE_DATE": row[9],
            }
        )

    return {"status": 200, "data": lst}


# -----------------------------------------------------END [GET] BY CODE STUDENT ---------------------------------------


# -----------------------------------------------------[POST] borrow ---------------------------------------
class StudentInfo(BaseModel):
    STUDENT_ID: int
    STUDENT_NAME: str
    STUDENT_CODE: str
    STUDENT_YEAR: str
    STUDENT_FACULTY: str
    STUDENT_MAJOR: str
    RECORD_STATUS: str
    DEL_FRAG: str
    CREATE_DATE: datetime
    UPDATE_DATE: datetime


# Class สำหรับข้อมูลผลิตภัณฑ์
class ProductInfo(BaseModel):
    P_ID: int
    P_NAME: str
    P_DESCRIPTION: str
    P_DOP: str
    P_PRICE: int
    P_SERIALNUMBER: str
    P_EQUIPMENTNUMBER: str
    P_BAND: str
    CATEGORY_ID: int
    STATUS_ID: int
    STUDENT_ID: int
    RECORD_STATUS: str
    DEL_FRAG: str
    CREATE_DATE: datetime
    UPDATE_DATE: datetime


class StudentWithProducts(BaseModel):
    STUDENT_INFO: StudentInfo
    PRODUCT_INFO: List[ProductInfo]


# 7



@app.post("/borrow")
def add_product(data: StudentWithProducts):
    s_id = data.STUDENT_INFO.STUDENT_ID

    # @app.put("")
    def changeStatus(s_id: int):
        for i in range(len(data.PRODUCT_INFO)):
            p_id = data.PRODUCT_INFO[i].P_ID
            status_id = 7
            record_id = "A"

            cnx = get_DB()
            cursor = cnx.cursor()

            sql_update_query = "UPDATE product SET STUDENT_ID = %s , STATUS_ID = %s ,RECORD_STATUS = %s WHERE P_ID = %s"
            cursor.execute(sql_update_query, (s_id, status_id, record_id, p_id))

            cnx.commit()
            cursor.close()
            cnx.close()

        for j in range(len(data.PRODUCT_INFO)):

            p_id = data.PRODUCT_INFO[j].P_ID

            record_status = "A"
            del_frag = "N"
            create_date = datetime.now()

            cnx = get_DB()
            cursor = cnx.cursor()

            query = "INSERT INTO borrow (P_ID,STUDENT_ID,RECORD_STATUS,DEL_FRAG,CREATE_DATE) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(query, (p_id, s_id, record_status, del_frag, create_date))

            cnx.commit()
            test_id = cursor.lastrowid
            cursor.close()
            cnx.close()

    changeStatus(s_id)

    return {"status": 200}


# ----------------------------------------------------- END [POST] borrow ---------------------------------------

# -----------------------------------------------------[GET] BORROW ---------------------------------------


@app.get("/get_borrow")
def get_borrow():
    cnx = get_DB()
    cursor = cnx.cursor()
    query = "SELECT * FROM borrow WHERE del_frag = 'N' and RECORD_STATUS = 'A'"
    cursor.execute(query)

    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    lst = []

    for row in rows:
        lst.append(
            {
                "LIST_ID": row[0],
                "P_ID": row[1],
                "STUDENT_ID": row[2],
                "RECORD_STATUS": row[3],
                "DEL_FRAG": row[4],
                "CREATE_DATE": row[5],
                "UPDATE_DATE": row[6],
            }
        )

    return lst


# -----------------------------------------------------END [GET] BORROW ---------------------------------------



# -----------------------------------------------------[PUT] BORROW back---------------------------------------

class studentBorrowBack(BaseModel):
    P_ID :int
    LIST_ID : int
    STUDENT_ID : int


@app.put("/put_borrow_back")
async def put_del_borrow(data: studentBorrowBack):
    p_id = data.P_ID
    l_id = data.LIST_ID
    s_id = data.STUDENT_ID
    update_time = datetime.now()

    cnx = get_DB()
    cursor = cnx.cursor()

    # Update borrow table
    sql_update_query_borrow = (
        "UPDATE borrow SET del_frag = %s, UPDATE_DATE = %s WHERE LIST_ID = %s"
    )
    cursor.execute(sql_update_query_borrow, ("Y", update_time, l_id))
    cnx.commit()

    # Update product table
    sql_update_query_product = (
        "UPDATE product SET STATUS_ID = %s, STUDENT_ID = %s WHERE P_ID = %s"
    )
    cursor.execute(sql_update_query_product, (6, 0, p_id))
    cnx.commit()

    cursor.close()
    cnx.close()

    return {"status": "success", "updated_list_id": l_id, "updated_product_id": p_id}


# -----------------------------------------------------END [PUT] BORROW back---------------------------------------


# -----------------------------------------------------[GET] BORROW  by '' ---------------------------------------


@app.get("/get_borrow_y")
def get_borrow():
    cnx = get_DB()
    cursor = cnx.cursor()
    query = "SELECT * FROM borrow WHERE del_frag = 'y' and RECORD_STATUS = 'A'"
    cursor.execute(query)

    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    lst = []

    for row in rows:
        lst.append(
            {
                "LIST_ID": row[0],
                "P_ID": row[1],
                "STUDENT_ID": row[2],
                "RECORD_STATUS": row[3],
                "DEL_FRAG": row[4],
                "CREATE_DATE": row[5],
                "UPDATE_DATE": row[6],
            }
        )

    return lst


# -----------------------------------------------------END [GET] BORROW ---------------------------------------





# ----------------------------------------------------[get product by category id]------------------

@app.get("/get_product_by_Category/{id}")
def get_test(id: int):
    cnx = get_DB()
    cursor = cnx.cursor()
    query = "SELECT * FROM product WHERE CATEGORY_ID = %s and RECORD_STATUS = 'A'"
    cursor.execute(query, (id,))

    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    lst = []

    for row in rows:
        lst.append(
            {
                "P_ID": row[0],
                "P_NAME": row[1],
                "P_DESCRIPTION": row[2],
                "P_DOP": row[3],
                "P_PRICE": row[4],
                "P_SERIALNUMBER": row[5],
                "P_EQUIPMENTNUMBER": row[6],
                "P_BAND": row[7],
                "CATEGORY_ID": row[8],
                "STATUS_ID": row[9],
                "STUDENT_ID": row[10],
                "RECORD_STATUS": row[11],
                "DEL_FRAG": row[12],
                "CREATE_DATE": row[13],
                "UPDATE_DATE": row[14],
            }
        )

    return lst


# ----------------------------------------------------END   [get product by category id]------------------


# ----------------------------------------------------[get product by category id and status is 'ว่าง']------------------

@app.get("/get_product_by_Category_Status/{id}")
def get_test(id: int):
    cnx = get_DB()
    cursor = cnx.cursor()
    # query = "SELECT * FROM product WHERE CATEGORY_ID = %s and STATUS_ID = 6"
    query = "SELECT * FROM product WHERE del_frag = 'N' and STATUS_ID = 6 and RECORD_STATUS = 'A' and CATEGORY_ID = %s "
    
    cursor.execute(query, (id,))

    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    lst = []

    for row in rows:
        lst.append(
            {
                "P_ID": row[0],
                "P_NAME": row[1],
                "P_DESCRIPTION": row[2],
                "P_DOP": row[3],
                "P_PRICE": row[4],
                "P_SERIALNUMBER": row[5],
                "P_EQUIPMENTNUMBER": row[6],
                "P_BAND": row[7],
                "CATEGORY_ID": row[8],
                "STATUS_ID": row[9],
                "STUDENT_ID": row[10],
                "RECORD_STATUS": row[11],
                "DEL_FRAG": row[12],
                "CREATE_DATE": row[13],
                "UPDATE_DATE": row[14],
            }
        )

    return lst


# ----------------------------------------------------END   [get product by category id]------------------





# ----------------------------------------------------[get product by category id and status is 'ว่าง' and N]------------------

# @app.get("/get_product_by_Category_Status_n/{id}")
# def get_test(id: int):
#     cnx = get_DB()
#     cursor = cnx.cursor()
#     # query = "SELECT * FROM product WHERE CATEGORY_ID = %s and STATUS_ID = 6"
#     query = "SELECT * FROM product WHERE del_frag = 'N' and STATUS_ID = 6 and RECORD_STATUS = 'N' and CATEGORY_ID = %s "
    
#     cursor.execute(query, (id,))

#     rows = cursor.fetchall()
#     cursor.close()
#     cnx.close()

#     lst = []

#     for row in rows:
#         lst.append(
#             {
#                 "P_ID": row[0],
#                 "P_NAME": row[1],
#                 "P_DESCRIPTION": row[2],
#                 "P_DOP": row[3],
#                 "P_PRICE": row[4],
#                 "P_SERIALNUMBER": row[5],
#                 "P_EQUIPMENTNUMBER": row[6],
#                 "P_BAND": row[7],
#                 "CATEGORY_ID": row[8],
#                 "STATUS_ID": row[9],
#                 "STUDENT_ID": row[10],
#                 "RECORD_STATUS": row[11],
#                 "DEL_FRAG": row[12],
#                 "CREATE_DATE": row[13],
#                 "UPDATE_DATE": row[14],
#             }
#         )

#     return lst


# ----------------------------------------------------END   [get product by category id]------------------

@app.get("/get_account")
def get_borrow():
    cnx = get_DB()
    cursor = cnx.cursor()
    query = "SELECT * FROM account WHERE del_frag = 'N' and RECORD_STATUS = 'A'"
    cursor.execute(query)

    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    lst = []

    for row in rows:
        lst.append(
            {
                "USER_ID": row[0],
                "USER_USER": row[1],
                "USER_PW": row[2],
                "USER_NAME": row[3],
                "RECORD_STATUS": row[4],
                "DEL_FRAG": row[5],
                "CREATE_DATE": row[6],
                "UPDATE_DATE": row[7],
            }
        )

    return lst

class usernames(BaseModel):
    username : str
    password : str
    
    
# @app.put("/account")
# def check_account(data: usernames):
#     user = data.username
#     pw = data.password
    
    
#     cnx = get_DB()
#     cursor = cnx.cursor()
    
#     sql_update_query = "UPDATE account SET USER_USER = %s , USER_PW = %s WHERE USER_USER = %s and USER_PW = %s"
#     cursor.execute(sql_update_query, (user,pw,user,pw))

#     cnx.commit()
#     # cursor.close()
#     # cnx.close()
    
#     cursor.close()
#     cnx.close()


#     return HTTPException

# @app.post("/login")
# async def login(data:usernames):
#     # Check if the username exists
    
#     if data.username not in users_db:
#         raise HTTPException(status_code=400, detail="Invalid username or password")
    
#     # Check if the password matches
#     if users_db[username] != password:
#         raise HTTPException(status_code=400, detail="Invalid username or password")
    
#     return {"message": "Login successful!"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)


@app.post("/account")

async def get_account(data:usernames):
    cnx = get_DB()
    cursor = cnx.cursor()
    
    sql_update_query = "SELECT * FROM account WHERE USERNAME = %s and PASSWORD = %s"
    cursor.execute(sql_update_query, (data.username ,data.password))


    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    lst = []
        
    if not rows:
        # raise HTTPException(status_code=204, status = "Incorrect username or password")
        return {"message": 204,"status" : "Incorrect username or password"}
    else:  
        for row in rows:
            lst ={
                "USER_USER" : row[1],
                "USER_PW" : row[2],
                "USER_NAME" : row[3]
            }

        return {"message":200,"status": "Success","list":lst}


# __________________________________________ count _________________________________________________
# all

@app.get('/count/{text}')
def get_count(text:str):
    
    def all():
        cnx = get_DB()
        cursor = cnx.cursor()

        sql_update_query = "SELECT COUNT(*) FROM borrow WHERE RECORD_STATUS ='A'"
        cursor.execute(sql_update_query)


        rows = cursor.fetchall()
        cursor.close()
        cnx.close()

        lst = []
            
        for row in rows:
            lst = {
                "count" : row[0]
            }

        return {"message":200,"status": "Success","list":lst}
    
    def returned():
        cnx = get_DB()
        cursor = cnx.cursor()

        sql_update_query = "SELECT COUNT(*) FROM borrow WHERE RECORD_STATUS ='A' and DEL_FRAG ='Y'"
        cursor.execute(sql_update_query)


        rows = cursor.fetchall()
        cursor.close()
        cnx.close()

        lst = []
            
        for row in rows:
            lst = {
                "count" : row[0]
            }

        return {"message":200,"status": "Success","list":lst}
    def not_returned():
        cnx = get_DB()
        cursor = cnx.cursor()

        sql_update_query = "SELECT COUNT(*) FROM borrow WHERE RECORD_STATUS ='A' and DEL_FRAG ='N'"
        cursor.execute(sql_update_query)


        rows = cursor.fetchall()
        cursor.close()
        cnx.close()

        lst = []
            
        for row in rows:
            lst = {
                "count" : row[0]
            }

        return {"message":200,"status": "Success","list":lst}
    
    if text == 'all':
       return all()
    elif text == 'returned':
       return returned()
    elif text == 'not_returned':
       return not_returned()
    else:
        return {"status": 'error','message':'ไม่พบข้อมูล'}
    
    
    #testpush
    