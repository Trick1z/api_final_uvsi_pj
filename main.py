from typing import Union
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, File, Response, status, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
import os
import base64
from dateutil import parser
import pytz
import io
import csv
from openpyxl import load_workbook
import hashlib
from bs4 import BeautifulSoup
load_dotenv()


# get DB
def get_DB():
    # deploy docker
    # connector = mysql.connector.connect(
    #     host='host.docker.internal',
    #     user='root',
    #     database='mydb'
    # )

    # localhost
    connector = mysql.connector.connect(
        host='localhost',
        user='root',
        database='mydb'
    )

    return connector


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # Angular's dev server runs on port 4200
    allow_origins=["*", "http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Angular's dev server runs on port 4200
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


def query_get(order: String):

    cnx = get_DB()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(order)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    if not rows:
        return None
        # return {"message": 404, "data": None}
    else:
        return rows


def query_post(order: String, data: tuple, res: str):
    cnx = get_DB()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(order, data)

    match res:
        case "login":
            rows = cursor.fetchall()
            cursor.close()
            cnx.close()
            return {"message": 200, "data": rows}
        case "update":
            cnx.commit()
            cursor.close()
            cnx.close()
            return {"message": 200, "data": None}
        case "id":
            cnx.commit()
            id = cursor.lastrowid
            cursor.close()
            cnx.close()
            return {"message": 200, "ID": id}


def query_put(order: String, data: tuple):
    cnx = get_DB()
    cursor = cnx.cursor()
    cursor.execute(order, (data))
    cnx.commit()
    cursor.close()
    cnx.close()

    return {"message": 200, "status": "delete_frag has change"}


# API HERE GOES HERE
# get


@app.get('/get.{table}')
def get_data(table: str):
    try:
        res = query_get(
            f"SELECT * FROM {table} WHERE DEL_FRAG = 'N' and RECORD_STATUS ='A'")
        return res
    except Exception as err:
        return {"message": err, "status": "Something Went Wrong!"}


@app.get('/get.product/{id}')
def get_products_id(id: int):
    try:
        rows = query_get(
            f"SELECT * FROM product WHERE PRODUCT_ID = {id} and DEL_FRAG = 'N' and RECORD_STATUS = 'A'")
        return {"message": 200, "data": rows}
    except Exception as err:
        return {"message": err, "status": "somthing went wrong!!"}

    # product by category id


@app.get('/get.product.category/{id}')
def get_products_category_id(id: int):
    try:
        rows = query_get(
            f"SELECT * FROM product WHERE CATEGORY_ID = {id} and DEL_FRAG = 'N' and RECORD_STATUS = 'A'")
        return {"message": 200, "data": rows}
    except Exception as err:
        return {"message": err, "status": "somthing went wrong!!"}
    # product by category and status 'ว่าง'


@app.get('/get.product.category.status/{id}')
def get_products_category_status_id(id: int):
    try:
        rows = query_get(
            f"SELECT * FROM product WHERE CATEGORY_ID = {id} and STATUS_ID = 6 and DEL_FRAG = 'N' and RECORD_STATUS = 'A' and on_hold='N'")

        return {"message": 200, "data": rows}
    except Exception as err:
        return {"message": err, "status": "somthing went wrong!!"}

    # product by status id


@app.get('/get.product.status/{id}')
def get_products_category_id(id: int):
    try:
        rows = query_get(
            f"SELECT * FROM product WHERE STATUS_ID = {id} and DEL_FRAG = 'N' and RECORD_STATUS = 'A' and on_hold='N'")

        return {"message": 200, "data": rows}
    except Exception as err:
        return {"message": err, "status": "somthing went wrong!!"}
    # img


@app.get('/get.img/{id}')
def get_img(id: int):
    try:
        rows = query_get(
            f"SELECT * FROM img WHERE PRODUCT_ID = {id} and DEL_FRAG = 'N' and RECORD_STATUS = 'A' ")
        return {"message": 200, "data": rows}
    except Exception as err:
        return {"message": err, "status": "something went wrong !!"}

    # student


@app.get('/get.student')
def get_student():
    try:
        res = query_get(
            "SELECT * FROM student WHERE DEL_FRAG = 'N' and RECORD_STATUS = 'A'")
        return {"message": 200, "data": res}
    except Exception as err:
        return {"message": err, "status": "something went wrong !!"}

    # student by code


@app.get('/get.student/{code}')
def get_student(code: str):
    try:
        res = query_get(
            f"SELECT * FROM student WHERE STUDENT_CODE = '{code}' and DEL_FRAG = 'N' and RECORD_STATUS = 'A'")

        if not res:
            return err
        return {"message": 200, "data": res}
    except Exception as err:
        return {"message": err, "status": "something went wrong !!"}

    # borrow


@app.get('/get.borrow/{status}')
def get_borrow(status: str):
    try:
        res = query_get(
            f"SELECT * FROM borrow WHERE DEL_FRAG = '{status}' and RECORD_STATUS = 'A'")

        return {"message": 200, "data": res}
    except Exception as err:
        return {"message": err, "status": "something went wrong !!"}


# post
    # account


class usernames(BaseModel):
    username: str
    password: str


def custom_hash(data: str) -> str:
    hashed = hashlib.sha256(data.encode()).hexdigest()
    truncated_hash = hashed[:16]
    formatted_hash = f"0x{truncated_hash.upper()}"
    return formatted_hash


@app.post("/post.account")
async def get_account(data: usernames):

    hash_pw = custom_hash(data.password)

    rows = query_post(
        "SELECT * FROM account WHERE USERNAME = %s and PASSWORD = %s", (data.username, hash_pw), 'login')

    if not rows["data"]:
        # raise HTTPException(status_code=204, status = "Incorrect username or password")
        return {"message": 204, "status": "Incorrect username or password"}
    else:

        return {"message": 200, "status": "Success", "data": rows["data"]}

    # category


class category(BaseModel):
    CATEGORY_NAME: str
    CATEGORY_DESCRIPTION: str


@app.post('/post.category')
def post_category(data: category):
    try:
        res = query_post("INSERT INTO category (CATEGORY_NAME ,CATEGORY_DESCRIPTION) VALUES (%s,%s)",
                         (data.CATEGORY_NAME, data.CATEGORY_DESCRIPTION), 'update')
        return res
    except Exception as err:
        return {"message": err, "status": "somthing went wrong!!"}

    # status


class status(BaseModel):
    STATUS_NAME: str
    STATUS_DESCRIPTION: str


@app.post('/post.status')
def post_category(data: status):
    try:
        res = query_post("INSERT INTO status (STATUS_NAME ,STATUS_DESCRIPTION) VALUES (%s,%s)",
                         (data.STATUS_NAME, data.STATUS_DESCRIPTION), 'update')
        return res
    except Exception as err:
        return {"message": err, "status": "somthing went wrong!!"}

    # product


class addProduct(BaseModel):
    PRODUCT_NAME: str
    CATEGORY_ID: int
    STATUS_ID: int
    PRODUCT_PRICE: int
    PRODUCT_DOP: str
    PRODUCT_BAND: str
    PRODUCT_SERIALNUMBER: str
    PRODUCT_EQUIPMENTNUMBER: str
    PRODUCT_DESCRIPTION: str
    IMG: str


@app.post('/post.product')
def add_product(data: addProduct):
    cratedate = datetime.now()
    try:
        res = query_post("""INSERT INTO product (PRODUCT_NAME  ,CATEGORY_ID ,STATUS_ID ,PRODUCT_PRICE ,PRODUCT_DOP ,PRODUCT_BAND ,PRODUCT_SERIALNUMBER ,PRODUCT_EQUIPMENTNUMBER ,PRODUCT_DESCRIPTION ,CREATE_DATE ) VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                         (data.PRODUCT_NAME, data.CATEGORY_ID, data.STATUS_ID, data.PRODUCT_PRICE, data.PRODUCT_DOP, data.PRODUCT_BAND, data.PRODUCT_SERIALNUMBER, data.PRODUCT_EQUIPMENTNUMBER, data.PRODUCT_DESCRIPTION, cratedate), 'id')

        res_img = query_post(
            "INSERT INTO img (PRODUCT_ID ,IMG_NAME) VALUES (%s,%s)", (res["ID"], data.IMG,), 'update')

        return {"message": 200, "product_status": res, "image_status": res_img}
    except Exception as err:
        return {"message": err, "status": "somthing went wrong"}

    # borrow


class ProductInfo(BaseModel):
    PRODUCT_ID: int


class addborrow(BaseModel):
    STUDENT_ID: int
    PRODUCT_INFO: List[ProductInfo]


@app.post('/post.borrow')
def add_borrow(data: addborrow):
    create_form = datetime.now()
    res_arr = []
    s_id = data.STUDENT_ID

    for product in data.PRODUCT_INFO:
        p_id = product.PRODUCT_ID

        try:
            # res = query_post("INSERT INTO borrow (STUDENT_ID ,PRODUCT_ID) VALUES (%s,%s)",(s_id,p_id,),'update')
            res = query_post(
                "INSERT INTO borrow (PRODUCT_ID,STUDENT_ID,CREATE_DATE) VALUES (%s,%s,%s)", (p_id, s_id, create_form,), 'id')
            res_2 = query_put(
                "UPDATE product SET STATUS_ID = 7 , on_hold = 'N' WHERE PRODUCT_ID = %s", (p_id,))
            res_arr.append(res["ID"])

            # return {"message": 200, "status": res_arr}

        except Exception as err:
            return {"message": err, "status": "somthing went wrong"}

    return {"message": 200, "status": res_arr}


# Put
    # category


class editCategory(BaseModel):
    CATEGORY_ID: int
    CATEGORY_NAME: str
    CATEGORY_DESCRIPTION: str


@app.put('/put.category')
async def put_category(data: editCategory):
    try:
        res = await query_put("UPDATE category SET  CATEGORY_NAME = %s , CATEGORY_DESCRIPTION = %s WHERE CATEGORY_ID = %s", (data.CATEGORY_NAME, data.CATEGORY_DESCRIPTION, data.CATEGORY_ID,))
        return res
    except Exception as err:
        return {"message": err, "status": "somthing went wrong!!"}
    # stats


class editStatus(BaseModel):
    STATUS_ID: int
    STATUS_NAME: str
    STATUS_DESCRIPTION: str


@app.put('/put.status')
async def put_status(data: editStatus):
    try:
        res = await query_put("UPDATE status SET  STATUS_NAME = %s , STATUS_DESCRIPTION = %s WHERE STATUS_ID = %s", (data.STATUS_NAME, data.STATUS_DESCRIPTION, data.STATUS_ID,))
        return res
    except Exception as err:
        return {"message": err, "status": "somthing went wrong!!"}

    # product


class editProduct(BaseModel):
    PRODUCT_ID: int
    PRODUCT_NAME: str
    PRODUCT_DESCRIPTION: str
    PRODUCT_DOP: str
    PRODUCT_PRICE: int
    PRODUCT_SERIALNUMBER: str
    PRODUCT_EQUIPMENTNUMBER: str
    PRODUCT_BAND: str
    CATEGORY_ID: int
    STATUS_ID: int

    # product  by id


@app.put('/put.product/{id}')
async def put_product_id(data: editProduct):
    try:
        res = await query_put("""UPDATE product SET
        PRODUCT_NAME = %s ,PRODUCT_DESCRIPTION = %s ,PRODUCT_DOP = %s,
        PRODUCT_PRICE =%s ,PRODUCT_SERIALNUMBER = %s, PRODUCT_EQUIPMENTNUMBER = %s,PRODUCT_BAND = %s,
        CATEGORY_ID =%s ,STATUS_ID = %s
        WHERE PRODUCT_ID = %s""", (data.PRODUCT_NAME, data.PRODUCT_DESCRIPTION, data.PRODUCT_DOP, data.PRODUCT_PRICE, data.PRODUCT_SERIALNUMBER, data.PRODUCT_EQUIPMENTNUMBER, data.PRODUCT_BAND, data.CATEGORY_ID, data.STATUS_ID, data.PRODUCT_ID))
        return res
    except Exception as err:
        return {"message": err, "status": "somthing went wrong!!"}

    # borrow back


class borrowBack(BaseModel):
    LIST_ID: int
    PRODUCT_ID: int


@app.put('/put.borrow.back')
def put_borrow_back(data: borrowBack):
    try:
        res_borrow = query_put(
            "UPDATE borrow SET DEL_FRAG = %s WHERE LIST_ID = %s", ('Y', data.LIST_ID,))
        res_product = query_put(
            "UPDATE product SET STATUS_ID = 6 WHERE PRODUCT_ID = %s", (data.PRODUCT_ID,))
        return {"message": 200, "borrow_status": res_borrow, "product_status": res_product}
    except Exception as err:
        return {"message": err, "status": "somthing went wrong!!"}

    # on hold


@app.put('/put.onHold.Product.{onHold}/{id}')
def on_hold(id: int, onHold: str):
    try:
        res = query_put(f"UPDATE product SET on_hold = '{onHold}' WHERE PRODUCT_ID = %s", (id,))
        return {"message": 200, "status": res}
    except Exception as err:
        return {"message": err, "status": "somthing went wrong!!"}


# Delete
    # hybrids Function
@app.put("/delete.{table}/{id}")
async def put_category_delfrag(id: int, table: str):
    try:
        res = await query_put(f"UPDATE {table} SET DEL_FRAG = 'Y' WHERE {table.upper()}_ID = %s", (id,))
        return res
    except Exception as err:
        return {"message": err, "Status": "something went wrong!!"}

    # on hold


@app.put('/put.on_hold/{state}')
def clear_onHold(state: str):
    try:
        res = query_put(
            "UPDATE product SET on_hold ='N' WHERE on_hold = %s", (state,))
        return {"message": 200, "status": "on hold has change!"}
    except Exception as err:
        return {"message": err, "status": "somthing went worng !"}


# count
    # borrow


@app.get('/count.borrow')
def get_count_borrow():

    try:
        res = query_get("""SELECT 
        COUNT(*) AS ทั้งหมด,
        COUNT(CASE WHEN DEL_FRAG = 'Y' THEN 1 END) AS คืนแล้ว,
        COUNT(CASE WHEN DEL_FRAG = 'N' THEN 1 END) AS ยังไม่คืน
        FROM borrow;""")

        return {"message": 200, "data": res}

    except Exception as err:

        return {"message": err, "status": "somthing went wrong!!"}


@app.get('/count.product')
def get_count_product():

    try:
        res = query_get("""SELECT 
    COUNT(CASE WHEN DEL_FRAG = 'N' THEN 1 END) AS ทั้งหมด,
    COUNT(CASE WHEN STATUS_ID = 6 AND DEL_FRAG = 'N' THEN 1 END) AS ว่าง,
    COUNT(CASE WHEN STATUS_ID = 7 AND DEL_FRAG = 'N' THEN 1 END) AS ถูกยืม
FROM product;""")

        return {"message": 200, "data": res}

    except Exception as err:

        return {"message": err, "status": "somthing went wrong!!"}


# getstudent id


@app.get('/get.std/{id}')
def get_std_id(id: int):
    try:
        rows = query_get(
            f"SELECT * FROM student WHERE STUDENT_ID = {id} and DEL_FRAG = 'N' and RECORD_STATUS = 'A'")
        return {"message": 200, "data": rows}
    except Exception as err:
        return {"message": err, "status": "somthing went wrong!!"}


class editStudent(BaseModel):
    STUDENT_ID: int
    STUDENT_NAME: str
    STUDENT_CODE: str
    STUDENT_MAJOR: str
    STUDENT_FACULTY: str


@app.put('/put.student')
def put_studentInfo(data: editStudent):
    try:
        res = query_put("UPDATE student SET  STUDENT_NAME = %s , STUDENT_CODE = %s, STUDENT_MAJOR = %s, STUDENT_FACULTY = %s WHERE STUDENT_ID = %s",
                        (data.STUDENT_NAME, data.STUDENT_CODE, data.STUDENT_MAJOR, data.STUDENT_FACULTY, data.STUDENT_ID,))
        return {"msg": "student info has change", "status": 200}
    except Exception as err:
        return {"message": err, "status": "somthing went wrong!!"}


class CSVFile(BaseModel):
    file: str  # Base64-encoded file content


@app.post("/upload-csv")
async def upload_csv(data: CSVFile):

    try:
        base64_str = data.file.split(",")[1]
        file_bytes = base64.b64decode(base64_str)
        file_like = io.BytesIO(file_bytes)
        encodings = ['utf-8', 'ISO-8859-1', 'latin1']
        csv_data = None
        for encoding in encodings:
            try:
                file_like.seek(0)
                csv_reader = csv.reader(
                    io.TextIOWrapper(file_like, encoding=encoding))
                csv_data = [row for row in csv_reader]
                break
            except UnicodeDecodeError:
                continue

        if csv_data is None:
            return {"error": "Unable to decode the file with available encodings"}

        # for i in range(len(csv_data)):
        #     res = query_post(
        #     "INSERT INTO student (STUDENT_NAME,STUDENT_CODE) VALUES ( %s,%s)", (csv_data[i][2],csv_data[i][1],), 'update')
        # return {"msg": 200 }
        for i in range(len(csv_data)):
            res = query_post(
                "INSERT INTO student (STUDENT_NAME,STUDENT_CODE,STUDENT_MAJOR,STUDENT_FACULTY) VALUES ( %s,%s,%s,%s)", (csv_data[i][2], csv_data[i][1], csv_data[i][3], csv_data[i][4],), 'update')
        return {"msg": 200}

    except Exception as e:
        return {"error": str(e)}


@app.get('/get.borrow.count/{id}')
def get_borrow_count(id : int):

    try:
        res = query_get(f"SELECT COUNT(CASE WHEN PRODUCT_ID = {id} AND DEL_FRAG = 'Y' THEN 1 END) AS ถูกยืมไปแล้ว FROM borrow")
        
        return res
    except Exception as err:
        return err
    
@app.get('/get.borrow/product_id/{id}')
def get_borrow_id(id:int):
    try:
        res = query_get(f"SELECT * FROM borrow WHERE PRODUCT_ID = {id} and DEL_FRAG = 'Y'")
        return res
    except Exception as err :
        return err