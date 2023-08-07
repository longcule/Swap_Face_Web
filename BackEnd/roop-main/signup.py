
import random
import base64
import io
import PIL.Image
from PIL import Image
from io import BytesIO
from pydantic import BaseModel
from starlette.responses import StreamingResponse
from fastapi import Depends, FastAPI, Header, Request, Body, File, UploadFile
import requests
import shutil
import random
import string
import json
from flask_cors import CORS
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
import uuid

app=FastAPI()

origins = ["*",
            "http://localhost:3000",
        "http://localhost:3002"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#______SONPIPI______
from pickle import FALSE
from tkinter import TRUE
import mysql.connector
import smtplib
import hashlib
import requests 
import threading
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from getpass import getpass
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

config = {
                'user': 'phpmyadmin',
                'password': 'password',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove3'
            } 

cred = firebase_admin.credentials.Certificate('longcule-firebase-adminsdk-do4ij-86278d95a6.json')
firebase_admin.initialize_app(cred)
@app.post('/signup')
async def signupAccount(request: Request):
    email = request.form.get('email')
    full_name = request.form.get('full_name')
    user_name = request.form.get('user_name')
    link_avatar = request.form.get('link_avatar')
    ip_register = request.form.get('ip_register')
    device_register = request.form.get('device_register')
    password = request.form.get('password')

    # email = 'long87755@gmail.com'
    # full_name = 'alo'
    # user_name = 'alo'
    # link_avatar = 'alo'
    # ip_register = 'alo'
    # device_register = 'alo'
    # password = 'longvgndfgdf'
    
    try:
        user = auth.create_user(
            email=email,
            password=password,
            email_verified=True
        )
        print("hallo")
        send_verification_email(email)
        print("allo")
        save_user_to_mysql(email,password,link_avatar,full_name,user_name,ip_register,device_register)
        return {"ketqua" : "Done Account"}
    except firebase_admin.auth.EmailAlreadyExistsError:
        print("Email Exist , Please Change Email")
        return {"ketqua" : "ERROR Email Exist"}
    except Exception as e:
        print("Lỗi: ", e)
        return {"ketqua" : "ERROR"}
    return {"ketqua" : "ERROR"}
	#	Name	Type	Collation	Attributes	Null	Default	Comments	Extra	Action
@app.post('/login')
async def loginAccount(request: Request):
    email = request.form.get('email')
    password = request.form.get('password')
    # email = "long87755@gmail.com"
    # password = "longvgndfgdf"
    connection= mysql.connector.connect(**config)
    mycursor = connection.cursor()
    mycursor.execute(f"SELECT * FROM user where email='{email}'")
    ketquaEmail = mycursor.fetchall()
    phantupro = mycursor.rowcount
    thong_tin = {}
    if phantupro == 0:
        return {"ketqua":"email not register account"}
    for i in range(0, phantupro):
        if ketquaEmail[i][6] != password:
            return  {"ketqua":"password wrong,please try again"}
        thong_tin["id_user"] = ketquaEmail[i][0]
        print(ketquaEmail[i][0])
        thong_tin["link_avatar"] = ketquaEmail[i][5]
        thong_tin["full_name"] = ketquaEmail[i][4]
        thong_tin["user_name"] = ketquaEmail[i][1]
        thong_tin["ip_register"] = ketquaEmail[i][6]
        thong_tin["device_register"] = ketquaEmail[i][7]
        thong_tin["password"] = ketquaEmail[i][2]
        thong_tin["email"] = ketquaEmail[i][3]
    return thong_tin
# Gửi email xác minh
def send_verification_email(email):
    #day la gmail mac dinh de gui den tat ca gmail khac va can phai bat xac thuc 2 yeu to
    from_address = "qn2012198@gmail.com" 
    password = "jvflstyftdgyszim"  

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = email
    msg['Subject'] = "Social Thinkdiff Company"
    linkverify = firebase_admin.auth.generate_email_verification_link(email, action_code_settings=None, app=None)
    body = """
    Thank You
    We appreciate your interest in connecting with us at, you can find related resources mentioned during the presentation on the session resources page.
    Devsenior Thinkdiff Company
    """ + linkverify

    msg.attach(MIMEText(body.format(email), 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_address, password)
        server.sendmail(from_address, email, msg.as_string())


def save_user_to_mysql(email , password, link_avatar,full_name,user_name,ip_register,device_register ):
        try:
            connection= mysql.connector.connect(**config)
            if connection.is_connected():
                print("Connected to MySQL database")
                cursor = connection.cursor(buffered=True)
                cursor.execute("SELECT DATABASE();")
                db_name = cursor.fetchone()[0]
                print(f"You are connected to database: {db_name}")
                mycursor = connection.cursor(buffered=True)
                mycursor.execute(f"SELECT MAX(id_user) from user")
                max_id_user = mycursor.fetchone()[0]
                id_user = max_id_user + 1
                sql = f"INSERT INTO user (id_user , user_name , password, email, full_name ,link_avatar , ip_register , device_register) VALUES ( {id_user} , %s, %s, %s, %s, %s, %s , %s )"
                val = (user_name, password, email, full_name, link_avatar, ip_register, device_register)
                mycursor.execute(sql, val)
                connection.commit()
        except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
        finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")
  
@app.post('/reset')
async def reset_password(request: Request):
    # email = request.form.get('email')
    email = "20021388@vnu.edu.vn"
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = "SELECT email FROM user WHERE email = %s"
    values = (email,)
    
    cursor.execute(query, values)
    result = cursor.fetchone()

    if result is not None:
        email = result[0]
        new_uuid = uuid.uuid4()

        # Chuyển đổi giá trị UUID sang chuỗi
        uuid_str = str(new_uuid)
        print(uuid_str)
        new_password = uuid_str

        update_query = "UPDATE user SET password = %s WHERE email = %s"
        update_values = (new_password, email)
        cursor.execute(update_query, update_values)
        connection.commit()

        send_email(email, new_password)

        print('Đã reset mật khẩu thành công và gửi email!')
    else:
        print('Không tìm thấy người dùng có tên email', email)

    cursor.close()
    connection.close()

def send_email(email, new_password):
    smtp_host = 'smpt.gmail.com'  
    smtp_port = 587  
    smtp_username = 'qn2012198@gmail.com' 
    smtp_password = 'jvflstyftdgyszim' 

    sender = 'qn2012198@gmail.com' 
    receiver = email

    subject = 'Reset mật khẩu'
    body = f'Mật khẩu mới của bạn là: {new_password}'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        

