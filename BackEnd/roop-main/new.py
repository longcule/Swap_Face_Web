import argparse
import secrets
from socket import socket
import cv2
from flask import request, jsonify
import mysql.connector
from numpy import random
from clean import randomGenData
import datetime
import time
import random
from PIL import Image
from datetime import datetime
from tqdm import tqdm
import base64
import json
import shutil
from  checkImgbb import check_imgbb_update,check_imgbb_api_key
import requests
from flask import Flask
from flask_cors import CORS
import socket
from datetime import datetime
import os
import glob
import pytz
from itsdangerous import URLSafeTimedSerializer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import uuid
import re
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, request, session, jsonify, redirect, url_for, Response
app = Flask(__name__)
app.app_context().push()
app.config["SECURITY_PASSWORD_SALT"] = "d5e6d7g8h9w6rq5w6r7z8x7z8x9c"
app.config["JWT_SECRET_KEY"] = "1ac4d5e6d5e2s6d7g8h9w63d49c"
app.secret_key = "d5e6d7g8h9z1a2b3c4g8h9z1a2b3c4d5e6d5e6d7g8h9z"

secret = URLSafeTimedSerializer(app.config["SECRET_KEY"])

# Config database mysql
config = {
                'user': 'phpmyadmin',
                'password': 'password',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove4'
            }      
connection = mysql.connector.connect(**config)

def get_ip_address():
    # Lấy tên máy chủ của máy tính hiện tại
    hostname = socket.gethostname()

    # Lấy địa chỉ IP tương ứng với tên máy chủ
    ip_address = socket.gethostbyname(hostname)

    return ip_address

def get_api_ip(api_url):
    try:
        ip = socket.gethostbyname(api_url)
        return ip
    except socket.gaierror:
        return None


app = Flask(__name__)
cors = CORS(app)



def generateData(link_full1, link_full2, index):
    random_case = random.randint(0, 5)
    sukien_lists = [
    ['skkethon', 'skchiatay', 'skConLapGiaDinh', 'skchaunoi', 'skhanhphuc', 'skGapNhau', 'skchaunoi', 'sklyhon', 'skConLapGiaDinh', 'skmuasam'],
    ['skSinhConDauLong', 'skmuasam', 'sknym', 'skmaymua', 'sklyhon', 'skngoaitinh', 'skSinhConDauLong', 'skmuasam', 'skSinhConDauLong', 'skngoaitinh'],
    ['skchaunoi', 'skToTinh', 'skkethon', 'skchiatay', 'sklyhon', 'skSinhConThuHai', 'skchaunoi', 'sknym', 'skConLapGiaDinh', 'skkethon'],
    ['skToTinh', 'skhanhphuc', 'skGapNhau', 'skmuasam', 'skkethon', 'skngoaitinh', 'skhanhphuc', 'skGapNhau', 'skToTinh', 'skmuasam'],
    ['skchiatay', 'skConLapGiaDinh', 'sknym', 'skToTinh', 'skGapNhau', 'skngoaitinh', 'skmuasam', 'skGapNhau', 'skConLapGiaDinh', 'skchiatay'],
    ['skhanhphuc', 'skmuasam', 'sklyhon', 'skToTinh', 'skchaunoi', 'skGapNhau', 'skmuasam', 'skSinhConThuHai', 'skkethon', 'skToTinh']
]

    for i, sukien_list in enumerate(sukien_lists):
        if random_case == i:
            save_sk = "saved_sukien"
            
            if index == 1:
                json = randomGenData(random_case, sukien_list, link_full1, link_full2, save_sk, index)
            elif index == 7:
                json = randomGenData(random_case, sukien_list, link_full1, link_full2, save_sk, index)
            
            return json

@app.route('/getdata', methods=['GET', 'POST'])
def createdata():
    link_full1 = request.headers.get('Link1')
    link_full2 = request.headers.get('Link2')


    return generateData(link_full1,link_full2, 1)

    
@app.route('/getdatangam', methods=['GET', 'POST'])
def createdatangam():
    link_full1 = request.headers.get('Link1')
    link_full2 = request.headers.get('Link2')
    return generateData(link_full1,link_full2, 7)


# tim theo id Love
@app.route('/lovehistory/<string:idlove>', methods=['GET'])
def getDataLoveHistory(idlove):

    thong_tin = {}
    list_thong_tin = []
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        mycursor.execute(f"SELECT * from saved_sukien where id_toan_bo_su_kien={idlove}")
        result2 = mycursor.fetchall()

        phantupro = mycursor.rowcount
        for i in range(0, phantupro):
            thong_tin["id"] = int(result2[i][0])
            thong_tin["link_nam_goc"] = result2[i][1]
            thong_tin["link_nu_goc"] = result2[i][2]
            thong_tin["link_nam_chua_swap"] = result2[i][3]
            thong_tin["link_nu_chua_swap"] = result2[i][4]
            thong_tin["link_da_swap"] = result2[i][5]
            thong_tin["real_time"] = result2[i][6]
            thong_tin["ten_su_kien"] = result2[i][15].replace('\r\n', '') 
            thong_tin["noi_dung_su_kien"] = result2[i][8]
            thong_tin["so_thu_tu_su_kien"] = int(result2[i][10])
            thong_tin["id_user"] = result2[i][14]
            thong_tin["phantram_loading"] = result2[i][21]
            thong_tin["count_comment"] = int(result2[i][18])
            thong_tin["count_view"] = int(result2[i][19])    
            thong_tin["ten_nam"] = result2[i][16]
            thong_tin["ten_nu"] = result2[i][17] 
            thong_tin["id_template"] = int(result2[i][20])         
            list_thong_tin.append(thong_tin)
            thong_tin = {}
            # Lưu các thay đổi vào database
        
        print(mycursor.rowcount, "record inserted.")

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return {"sukien":list_thong_tin}



# tim theo id user
@app.route('/lovehistory/user/<string:id_user>', methods=['GET'])
def getDataLoveHistoryUser(id_user):

    thong_tin = {}
    list_toan_bo_sukien_saved = []
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        mycursor.execute(f"SELECT DISTINCT id_toan_bo_su_kien from saved_sukien where id_user = {id_user}")
        PhanTuMax = mycursor.fetchall()

        new_list = [item[0] for item in PhanTuMax]

        for id_sukien in reversed(new_list):
            Mot_LanQuerryData = []
            mycursor.execute(f"SELECT * from saved_sukien where id_toan_bo_su_kien={id_sukien}")
            result2 = mycursor.fetchall()
            thong_tin = {}
            phantupro = mycursor.rowcount
            for i in range(0, phantupro):
                thong_tin["id"] = int(result2[i][0])
                thong_tin["link_nam_goc"] = result2[i][1]
                thong_tin["link_nu_goc"] = result2[i][2]
                thong_tin["link_nam_chua_swap"] = result2[i][3]
                thong_tin["link_nu_chua_swap"] = result2[i][4]
                thong_tin["link_da_swap"] = result2[i][5]
                thong_tin["real_time"] = result2[i][6]
                thong_tin["ten_su_kien"] = result2[i][15].replace('\r\n', '') 
                thong_tin["noi_dung_su_kien"] = result2[i][8]
                thong_tin["so_thu_tu_su_kien"] = int(result2[i][10])
                thong_tin["id_user"] = int(result2[i][14])
                thong_tin["phantram_loading"] = result2[i][21]
                thong_tin["count_comment"] = int(result2[i][18])
                thong_tin["count_view"] = int(result2[i][19])    
                thong_tin["ten_nam"] = result2[i][16]
                thong_tin["ten_nu"] = result2[i][17] 
                thong_tin["id_template"] = int(result2[i][20])      
                Mot_LanQuerryData.append(thong_tin)

                thong_tin = {}
            list_toan_bo_sukien_saved.append({'sukien':Mot_LanQuerryData})


        print(mycursor.rowcount, "record inserted.")

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return {"list_su_kien":list_toan_bo_sukien_saved}

# create comment
@app.route('/lovehistory/comment', methods=['POST'])
def createcomment():
    noi_dung = request.form.get('noi_dung_cmt')
    device_cmt = request.form.get('device_cmt') 
    id_toan_bo_su_kien = request.form.get('id_toan_bo_su_kien') 
    so_thu_tu_su_kien = request.form.get('so_thu_tu_su_kien')
    ipComment =  request.form.get('ipComment')  
    imageattach = request.form.get('imageattach')  
    id_user = request.form.get('id_user')
    location = request.form.get('location')
    if id_user:
        id_user = id_user
    else:
        id_user = 0
    thong_tin={}

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        mycursor.execute(f"SELECT MAX(id_Comment) from comment")
        result_id_sk = mycursor.fetchall()
        idNext = result_id_sk[0][0]+1
        print("hallo")
        mycursor.execute(f"SELECT * FROM saved_sukien where id_toan_bo_su_kien={id_toan_bo_su_kien}")
        saved_sukien = mycursor.fetchall()
        print("hallo2")
        dt_utc = datetime.now()
        tz = pytz.timezone('Asia/Bangkok')
        dt_local = dt_utc.astimezone(tz)
        datetimenow = dt_local.strftime('%Y-%m-%d %H:%M:%S')
        mycursor.execute(f"SELECT * FROM user where id_user={id_user}")
        user_name = mycursor.fetchall()
        print(user_name)
        print("hallo3")
        thong_tin["device_cmt"] = device_cmt
        thong_tin["dia_chi_ip"] = ipComment
        thong_tin["id_comment"] = int(idNext)
        thong_tin["id_toan_bo_su_kien"] = int(id_toan_bo_su_kien)
        thong_tin["so_thu_tu_su_kien"] = int(so_thu_tu_su_kien)
        thong_tin["imageattach"] = imageattach
        thong_tin["link_nam_goc"] = saved_sukien[0][1]
        thong_tin["link_nu_goc"] = saved_sukien[0][2]
        thong_tin["noi_dung_cmt"] = noi_dung
        thong_tin["thoi_gian_release"] = datetimenow
        thong_tin["location"] = location
        thong_tin["user_name"] = None
        thong_tin["avatar_user"] = None
        
        if user_name:
            thong_tin["user_name"] = user_name[0][2]
            thong_tin["avatar_user"] = user_name[0][1]
        
        thong_tin["id_user"] = int(id_user)



        lenhquery = f"INSERT INTO comment(id_Comment,noi_dung_Comment,IP_Comment,device_Comment,id_toan_bo_su_kien,imageattach, thoi_gian_release, id_user, user_name, avatar_user, so_thu_tu_su_kien, location) VALUES ( {idNext} ,%s,%s,%s, {id_toan_bo_su_kien} ,%s , %s, {id_user}, %s, %s,{so_thu_tu_su_kien}, %s )"
        val = (noi_dung ,ipComment , device_cmt,imageattach,datetimenow, thong_tin["user_name"], thong_tin["avatar_user"], location)
        mycursor.execute(lenhquery, val)
        result1 = mycursor.fetchall()
        connection.commit()


        mycursor.execute("SELECT COUNT(id_Comment) FROM comment WHERE id_toan_bo_su_kien = {} and so_thu_tu_su_kien = {}".format(id_toan_bo_su_kien,so_thu_tu_su_kien ))
        # lấy kết quả
        results1 = mycursor.fetchone()[0]
        update_query = "UPDATE saved_sukien SET count_comment = {} WHERE id_toan_bo_su_kien = {} and so_thu_tu_su_kien = {}".format(results1, id_toan_bo_su_kien, so_thu_tu_su_kien)
        cursor.execute(update_query)
        connection.commit()
        # luu cac thay doi vao trong database
        print(mycursor.rowcount, "record inserted.")

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
        return {"error":f"Failed to connect to MySQL database: {error}"}
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return {"comment":thong_tin}
        
# create page for event history
@app.route('/lovehistory/page/<int:trang>', methods=['GET'])
def getPageLoveHistory(trang):
    list_toan_bo_sukien_saved = []

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        mycursor.execute(f"SELECT MAX(id_toan_bo_su_kien) from saved_sukien")
        PhanTuMax = mycursor.fetchall()
        soPhanTu = PhanTuMax[0][0]  + 1 
        print(soPhanTu)
        if trang < 1:
            return {"messages" : "page start from 1"}
        for idItemPhanTu in reversed(range(soPhanTu - ((trang - 1) * 25) - 25, soPhanTu - ((trang - 1) * 25))):
            Mot_LanQuerryData = []
            mycursor.execute(f"SELECT * from saved_sukien where id_toan_bo_su_kien={idItemPhanTu}")
            result2 = mycursor.fetchall()
            thong_tin = {}
            phantupro = mycursor.rowcount
            for i in range(0, phantupro):
                thong_tin["id"] = int(result2[i][0])
                thong_tin["link_nam_goc"] = result2[i][1]
                thong_tin["link_nu_goc"] = result2[i][2]
                thong_tin["link_nam_chua_swap"] = result2[i][3]
                thong_tin["link_nu_chua_swap"] = result2[i][4]
                thong_tin["link_da_swap"] = result2[i][5]
                thong_tin["real_time"] = result2[i][6]
                thong_tin["ten_su_kien"] = result2[i][15].replace('\r\n', '') 
                thong_tin["noi_dung_su_kien"] = result2[i][8]
                thong_tin["id_toan_bo_su_kien"] = int(result2[i][9])                
                thong_tin["so_thu_tu_su_kien"] = int(result2[i][10])
                thong_tin["id_user"] = int(result2[i][14])
                thong_tin["phantram_loading"] = result2[i][21]
                thong_tin["count_comment"] = int(result2[i][18])
                thong_tin["count_view"] = int(result2[i][19])    
                thong_tin["ten_nam"] = result2[i][16]
                thong_tin["ten_nu"] = result2[i][17] 
                thong_tin["id_template"] = int(result2[i][20]) 
                Mot_LanQuerryData.append(thong_tin)

                thong_tin = {}
            list_toan_bo_sukien_saved.append({"sukien":Mot_LanQuerryData})
            
            # Lưu các thay đổi vào database

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return {"list_sukien":list_toan_bo_sukien_saved}


@app.route('/saveimage/<string:user_name>', methods=['POST', 'GET'])
def save_image(user_name):
    print("hello")
    results1 = []
    list_img=[]
    if request.method == "POST":
        image_urls = request.json
        list_image = []

        try:
            connection= mysql.connector.connect(**config)
            if connection.is_connected():
                print("Connected to MySQL database")
                cursor = connection.cursor(buffered=True)
                cursor.execute("SELECT DATABASE();")
                db_name = cursor.fetchone()[0]
                print(f"You are connected to database: {db_name}")
                mycursor = connection.cursor(buffered=True)
            json_str = json.dumps(image_urls)    
            json_obj = json.loads(json_str)
            for key in json_obj:

                mycursor.execute("SELECT MAX(id) FROM saved_image")
                max_id_user = mycursor.fetchone()[0]
                id_img = max_id_user + 1
                dt_utc = datetime.now()
                tz = pytz.timezone('Asia/Bangkok')
                dt_local = dt_utc.astimezone(tz)
                print(id_img)
                date = dt_local.strftime('%Y-%m-%d %H:%M:%S')
                # Thêm một dict mới vào list_image
                image_dict = {'id': id_img, 'image_url': json_obj[key], 'date': date}
                list_image.append(image_dict)

            for image in list_image:
                mycursor.execute("INSERT INTO saved_image (id, user_name ,link_image, thoigian) VALUES ( %s , %s , %s, %s)", (image['id'], user_name, image['image_url'], image['date']))
                connection.commit()
        
            mycursor.execute(f"SELECT * FROM saved_image WHERE user_name='{user_name}'")
            # lấy kết quả
            results1 = mycursor.fetchall()
            phantupro = mycursor.rowcount
            
            for i in range(0, phantupro):
                list_img.append(results1[i][2])

        except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")
        return {"list_img":list_img} 
    
    else: 
        try:
            connection= mysql.connector.connect(**config)
            if connection.is_connected():
                print("Connected to MySQL database")
                cursor = connection.cursor(buffered=True)
                cursor.execute("SELECT DATABASE();")
                db_name = cursor.fetchone()[0]
                print(f"You are connected to database: {db_name}")
                mycursor = connection.cursor(buffered=True)

            mycursor.execute(f"SELECT * FROM saved_image WHERE user_name='{user_name}'")
            # lấy kết quả
            results1 = mycursor.fetchall()
            phantupro = mycursor.rowcount
            
            for i in range(0, phantupro):
                list_img.append(results1[i][2])

        except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed") 
    
        return {"list_img":list_img}

@app.route('/changeavatar/<int:id_user>', methods=['POST'])
def change_avatar(id_user):
    link_image = request.form.get("link_img")
    # check: upload
    check = request.form.get("check_img")  
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    mycursor = connection.cursor()
    update_query = "UPDATE user SET link_avatar = %s WHERE id_user = %s"
    update_values = (link_image, id_user)
    cursor.execute(update_query, update_values)
    connection.commit()

    if check == "upload":
        print("heloooo")
        mycursor.execute(f"SELECT user_name FROM user WHERE id_user='{id_user}'")
        ketqua = mycursor.fetchone()
        print(ketqua)
        ketqua_list = list(ketqua)
        mycursor.execute("SELECT MAX(id) FROM saved_image")
        max_id_user = mycursor.fetchone()[0]
        id_img = max_id_user + 1
        dt_utc = datetime.now()
        tz = pytz.timezone('Asia/Bangkok')
        dt_local = dt_utc.astimezone(tz)
        date = dt_local.strftime('%Y-%m-%d %H:%M:%S')
        mycursor.execute("INSERT INTO saved_image (id, user_name, link_image, thoigian) VALUES (%s, %s, %s, %s)", (id_img, ketqua_list[0], link_image, date))
        connection.commit()

    return {"link_img":link_image}

@app.route('/search', methods=['GET'])
def search_word():
    search_word = request.args.get('word')
    list_toan_bo_sukien_saved = []
    id_sukien = []
    stt_sukien = []

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        sql_query = f"SELECT * FROM comment WHERE UPPER(noi_dung_Comment) LIKE UPPER('%{search_word}%')"
        mycursor.execute(sql_query)
        search_results = mycursor.fetchall()

        sql_query = f"SELECT * FROM add_sukien WHERE UPPER(noidung_su_kien) LIKE UPPER('%{search_word}%')"
        mycursor.execute(sql_query)
        search_results2 = mycursor.fetchall()

        for row in search_results:
            id_sukien.append(row[4])
            stt_sukien.append(row[10])

        for row in search_results2:
            id_sukien.append(row[2])
            stt_sukien.append(row[13])

        for i in range(len(id_sukien)):
            Mot_LanQuerryData = []
            mycursor.execute(f"SELECT * from saved_sukien where id_toan_bo_su_kien = {id_sukien[i]} and so_thu_tu_su_kien = {stt_sukien[i]}")
            result2 = mycursor.fetchall()
            thong_tin = {}
            phantupro = mycursor.rowcount
            for i in range(0, phantupro):
                thong_tin["id"] = int(result2[i][0])
                thong_tin["link_nam_goc"] = result2[i][1]
                thong_tin["link_nu_goc"] = result2[i][2]
                thong_tin["link_nam_chua_swap"] = result2[i][3]
                thong_tin["link_nu_chua_swap"] = result2[i][4]
                thong_tin["link_da_swap"] = result2[i][5]
                thong_tin["real_time"] = result2[i][6]
                thong_tin["ten_su_kien"] = result2[i][15].replace('\r\n', '') 
                thong_tin["noi_dung_su_kien"] = result2[i][8]
                thong_tin["id_toan_bo_su_kien"] = int(result2[i][9])                
                thong_tin["so_thu_tu_su_kien"] = int(result2[i][10])
                thong_tin["id_user"] = int(result2[i][14])
                thong_tin["phantram_loading"] = result2[i][21]
                thong_tin["count_comment"] = int(result2[i][18])
                thong_tin["count_view"] = int(result2[i][19])    
                thong_tin["ten_nam"] = result2[i][16]
                thong_tin["ten_nu"] = result2[i][17] 
                thong_tin["id_template"] = int(result2[i][20]) 
                Mot_LanQuerryData.append(thong_tin)

                thong_tin = {}
            list_toan_bo_sukien_saved.append({'sukien':Mot_LanQuerryData})

        print(mycursor.rowcount, "record inserted.")

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return {"list_sukien":list_toan_bo_sukien_saved}



# create page for comment history
@app.route('/lovehistory/pageComment/<int:trang>', methods=['GET'])
def getPageCommentHistory(trang):
    thong_tin = {}
    list_thong_tin = []
    config = {
                'user': 'phpmyadmin',
                'password': 'password',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove4'
            }     
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        mycursor.execute(f"SELECT MAX(id_Comment) from comment")
        result_id_sk = mycursor.fetchall()
        tongsophantu = result_id_sk[0][0]
        tongsotrang = tongsophantu / 50 
        print(tongsotrang)
        if trang < 1:
            return {"messages" : "page start from 1"} 
        phantunguoc = (trang-1) *50 
        mycursor = connection.cursor()
        mycursor.execute(f"SELECT * FROM comment ORDER BY id_Comment DESC LIMIT { phantunguoc } ,50 ")
        result2 = mycursor.fetchall()
       
        sophantu = mycursor.rowcount
        for i in range(0, sophantu):
            thong_tin["id_toan_bo_su_kien"] = int(result2[i][4])
            if result2[i][10] is None:
                thong_tin["so_thu_tu_su_kien"] = 0
            else:
                thong_tin["so_thu_tu_su_kien"] = int(result2[i][10])
            thong_tin["noi_dung_cmt"] = result2[i][1]
            thong_tin["dia_chi_ip"] = result2[i][2]
            thong_tin["device_cmt"] = result2[i][3]
            thong_tin["id_comment"] = int(result2[i][0])
            thong_tin["imageattach"]= result2[i][5] 
            thong_tin["thoi_gian_release"]= result2[i][6] 
            thong_tin["user_name"] = result2[0][8]
            thong_tin["id_user"] = int(result2[0][7])
            thong_tin["avatar_user"] = result2[0][9]
            thong_tin["location"] = result2[i][11]
            mycursor.execute(f"SELECT * from saved_sukien where id_toan_bo_su_kien={result2[i][4]}")
            saved_sukien = mycursor.fetchall()
            thong_tin["link_nam_goc"] = saved_sukien[0][1]
            thong_tin["link_nu_goc"] = saved_sukien[0][2]
            list_thong_tin.append(thong_tin)
            thong_tin = {}



    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    
    return {"comment":list_thong_tin,
            "sophantu" : tongsophantu,
            "sotrang": tongsotrang}


@app.route("/lovehistory/comment/<int:so_thu_tu_su_kien>")
def getCommentHistory(so_thu_tu_su_kien):

    thong_tin = {}
    list_thong_tin = []
    id_toan_bo_su_kien =  request.args.get('id_toan_bo_su_kien')
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        mycursor.execute(f"SELECT * FROM comment where id_toan_bo_su_kien={id_toan_bo_su_kien} and so_thu_tu_su_kien={so_thu_tu_su_kien}")
        result2 = mycursor.fetchall()
        mycursor.execute(f"SELECT COUNT(*) FROM comment where id_toan_bo_su_kien={id_toan_bo_su_kien} and so_thu_tu_su_kien={so_thu_tu_su_kien}")
        result_toan_bo_su_kien = mycursor.fetchall()
        print(result_toan_bo_su_kien[0][0])
        for i in range(0 , result_toan_bo_su_kien[0][0]):
            thong_tin["id_toan_bo_su_kien"] = int(result2[i][4])
            thong_tin["noi_dung_cmt"] = result2[i][1]
            thong_tin["dia_chi_ip"] = result2[i][2]
            thong_tin["device_cmt"] = result2[i][3]
            thong_tin["id_comment"] = int(result2[i][0])
            thong_tin["imageattach"]= result2[i][5] 
            thong_tin["thoi_gian_release"] = result2[i][6]
            thong_tin["user_name"] = result2[i][8]
            thong_tin["id_user"] = int(result2[i][7])
            thong_tin["avatar_user"] = result2[i][9]
            thong_tin["so_thu_tu_su_kien"] = so_thu_tu_su_kien
            thong_tin["location"] = result2[i][11]
            mycursor.execute(f"SELECT * from saved_sukien where id_toan_bo_su_kien={result2[i][4]}")
            saved_sukien = mycursor.fetchall()
            thong_tin["link_nam_goc"] = saved_sukien[0][1]
            thong_tin["link_nu_goc"] = saved_sukien[0][2]
            list_thong_tin.append(thong_tin)
            thong_tin = {}
        # Lưu các thay đổi vào database
        connection.commit()

        print(mycursor.rowcount, "record inserted.")


    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return {"comment":list_thong_tin}


@app.route('/countview', methods=['POST'])
def count_view():
    id_sk = request.form.get('id_toan_bo_su_kien')
    stt_sk = request.form.get('so_thu_tu_su_kien')

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(f"SELECT count_view from saved_sukien where id_toan_bo_su_kien = {id_sk} and so_thu_tu_su_kien = {stt_sk}")
    result = cursor.fetchone()
    result = int(result[0])
    print(result)
    result = result + 1

    cursor.execute(f"UPDATE saved_sukien SET count_view = {result} where id_toan_bo_su_kien = {id_sk} and so_thu_tu_su_kien = {stt_sk}")

    connection.commit()
    return jsonify({'count_view': result}), 200

@app.route("/lovehistory/comment/user/<int:id_user>")
def getCommentHistoryUser(id_user):

    thong_tin = {}
    list_thong_tin = []

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()

        mycursor.execute(f"SELECT * FROM comment where id_user={id_user}")
        result2 = mycursor.fetchall()
        mycursor.execute(f"SELECT COUNT(*) FROM comment where id_user={id_user}")
        result_toan_bo_comment = mycursor.fetchall()
        print(result_toan_bo_comment[0][0])
        for i in range(0 , result_toan_bo_comment[0][0]):
            thong_tin["id_toan_bo_su_kien"] = int(result2[i][4])
            thong_tin["noi_dung_cmt"] = result2[i][1]
            thong_tin["dia_chi_ip"] = result2[i][2]
            thong_tin["device_cmt"] = result2[i][3]
            thong_tin["id_comment"] = int(result2[i][0])
            thong_tin["imageattach"]= result2[i][5] 
            thong_tin["thoi_gian_release"] = result2[i][6]
            thong_tin["user_name"] = result2[0][8]
            thong_tin["id_user"] = int(result2[0][7])
            thong_tin["avatar_user"] = result2[i][9]
            thong_tin["so_thu_tu_su_kien"] = int(result2[i][10])
            mycursor.execute(f"SELECT * from saved_sukien where id_toan_bo_su_kien={result2[i][4]}")
            saved_sukien = mycursor.fetchall()
            thong_tin["link_nam_goc"] = saved_sukien[0][1]
            thong_tin["link_nu_goc"] = saved_sukien[0][2]
            list_thong_tin.append(thong_tin)
            thong_tin = {}

        # Lưu các thay đổi vào database


        print(mycursor.rowcount, "record inserted.")


    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return {"comment_user":list_thong_tin}

@app.route("/lovehistory/add/<int:id_toan_bo_su_kien>" , methods=['POST'])
def addThemSuKienTinhYeu(id_toan_bo_su_kien):
    link_full1 = request.headers.get('Link1')
    link_full2 = request.headers.get('Link2')
    ten_sukien = request.form.get('ten_sukien')

    noidung_su_kien = request.form.get('noidung_su_kien')
    ten_nam = request.form.get('ten_nam')
    ten_nu = request.form.get('ten_nu')   
    device_them_su_kien = request.form.get('device_them_su_kien') 
    ip_them_su_kien =  request.form.get('ip_them_su_kien') 
    link_img = request.form.get('link_img')
    link_video = request.form.get('link_video')
    id_user = request.form.get('id_user')
    id_template = request.form.get("id_template")

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor = connection.cursor()
        mycursor.execute(f"SELECT MAX(id_add) from add_sukien")
        max_sql_id_saved = mycursor.fetchall()
        if max_sql_id_saved[0][0] is None:
            id_add_max = 1
        else:
            id_add_max = max_sql_id_saved[0][0] + 1
        date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        mycursor.execute(f"SELECT MAX(so_thu_tu_su_kien) from saved_sukien where id_toan_bo_su_kien={id_toan_bo_su_kien}")
        max_stt_skien = mycursor.fetchall()
        so_thu_tu_sk = max_stt_skien[0][0] + 1
        count_comment = 0
        count_view = 0
        lenhquery = f"INSERT INTO add_sukien(id_add,id_user,id_toan_bo_su_kien,ten_sukien,noidung_su_kien ,ten_nam, ten_nu, device_them_su_kien, ip_them_su_kien, link_img, link_video, id_template, thoigian_themsk, so_thu_tu_su_kien, count_comment, count_view) VALUES ( {id_add_max}, {id_user},{id_toan_bo_su_kien},%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, {so_thu_tu_sk},{count_comment}, {count_view} )"
        val = (ten_sukien, noidung_su_kien , ten_nam, ten_nu, device_them_su_kien, ip_them_su_kien, link_img, link_video, id_template, date)
        mycursor.execute(lenhquery, val)
        connection.commit()

        mycursor.execute(f"SELECT MAX(id_saved) from saved_sukien")
        result2 = mycursor.fetchall()
        print(result2[0][0])
        link_nam_chua_swap = 'abc'  
        link_nu_chua_swap = 'abc'
        if link_img is None:
            link_swap = link_video
        else:
            link_swap = link_img
        print(link_swap)
        phantram_loading = 0
        sql2 = f"INSERT INTO saved_sukien (id_saved ,link_nam_goc , link_nu_goc ,link_nam_chua_swap , link_nu_chua_swap, link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , id_toan_bo_su_kien ,so_thu_tu_su_kien, thoigian_sukien, device_them_su_kien, ip_them_su_kien, id_user, tomLuocText, ten_nam, ten_nu, count_comment, count_view, id_template, phantram_loading) VALUES ( {result2[0][0] + 1}  ,%s  , %s  ,%s, %s, %s, %s, %s, %s, {id_toan_bo_su_kien},{so_thu_tu_sk}, %s, %s, %s, {id_user}, %s, %s, %s, {count_comment}, {count_view}, {id_template}, {phantram_loading})"
        val2 = (link_full1, link_full2, link_nam_chua_swap, link_nu_chua_swap, link_swap, date, ten_sukien, noidung_su_kien, date, device_them_su_kien, ip_them_su_kien, noidung_su_kien, ten_nam, ten_nu)
        mycursor.execute(sql2, val2)
        connection.commit()

        print(mycursor.rowcount, "record inserted.")
    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
        return {"ketqua":"Failed to connect to MySQL database: " + str(error)}
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    return jsonify(message="add thanh cong sukien")


@app.route("/register", methods=["POST"])
def register():
    from_address = "qn2012198@gmail.com" 
    password_mail = "xoqjazdjndjzlkur"  

    email = request.form.get("email")
    password = request.form.get("password")
    user_name = request.form.get("user_name")
    link_avatar = request.form.get("link_avatar")
    ip_register = request.form.get("ip_register")
    device_register = request.form.get("device_register")

    if email is None and password is None and user_name is None:
        return jsonify(message="Please enter your email and password and user name!")
    elif email is None:
        return jsonify(message="Please enter your email!")
    elif password is None:
        return jsonify(message="Please enter your password!")
    elif email is None and password is None:
        return jsonify(message="Please enter your email and password!")
    elif user_name is None:
        return jsonify(message="Please enter your user name!")
    elif password is None and user_name is None:
        return jsonify(message="Please enter your password and user name!")
    elif email is None and user_name is None:
        return jsonify(message="Please enter your email and user name!")

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE email = %s", [email])
    account = cursor.fetchone()
    print(account)
    cursor.close()
    if account:
        return jsonify(message="Account already exists!")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify(message="Invalid email address!")
    elif not password or not email:
        return jsonify(message="Incorrect email/password!")
    elif len(password) < 8:
        return jsonify(message="Password must be at least 8 characters.")
    else:
        data = {"email": email, "password": password, "user_name":user_name,
                "link_avatar":link_avatar, "ip_register":ip_register, "device_register":device_register}
        token = secret.dumps(data, salt='d5e6d7g8h9w6rq5w6r7z8x7z8x9c')
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = email
        msg['Subject'] = "Social Thinkdiff Company"
        link = url_for("register_confirm", token=token, _external=True)
        body = """
    Thank You
    We appreciate your interest in connecting with us at, you can find related resources mentioned during the presentation on the session resources page.
    Devsenior Thinkdiff Company
    """ + link

        msg.attach(MIMEText(body.format(email), 'html'))
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_address, password_mail)
            server.sendmail(from_address, email, msg.as_string())
        return jsonify(message="Please check your email or spam", account={"email": email})
    


@app.route("/register/confirm/<token>")
def register_confirm(token):
   
	try:
		confirmed_email = secret.loads(token, salt='d5e6d7g8h9w6rq5w6r7z8x7z8x9c')
		print(confirmed_email["email"])
		connection = mysql.connector.connect(**config)        
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM user WHERE email = %s", [confirmed_email["email"]])
		account = cursor.fetchone()
		cursor.close()   
		if account:
			return jsonify(message="Your account was already confirm")
		else:
			save_user_to_mysql(confirmed_email["user_name"],confirmed_email["password"],confirmed_email["email"], confirmed_email["link_avatar"],confirmed_email["ip_register"],confirmed_email["device_register"])      
	except Exception:
		return {"message": "Your link was expired. Try again"}

	return {"message": "Confirm successfully. Try to login"}



@app.route('/login', methods=['POST'])
def login_account():
    email_or_username = request.form.get('email_or_username')
    password = request.form.get('password')

    connection = mysql.connector.connect(**config)
    mycursor = connection.cursor()
    mycursor.execute(f"SELECT * FROM user WHERE email='{email_or_username}' OR user_name='{email_or_username}'")
    ketqua = mycursor.fetchall()
    num_rows = mycursor.rowcount
    thong_tin = {}
    if num_rows == 0:
        return jsonify({"ketqua":"Email or username is not registered."})
    for i in range(0, num_rows):
        if ketqua[i][5] != password:
            return  jsonify({"ketqua":"Wrong password. Please try again."})
        thong_tin["id_user"] = int(ketqua[i][0])
        thong_tin["link_avatar"] = ketqua[i][1]
        thong_tin["user_name"] = ketqua[i][2]
        thong_tin["ip_register"] = ketqua[i][3]
        thong_tin["device_register"] = ketqua[i][4]
        thong_tin["email"] = ketqua[i][6]
        thong_tin["count_sukien"] = int(ketqua[i][7])
        thong_tin["count_comment"] = int(ketqua[i][8])
        thong_tin["count_view"] = int(ketqua[i][9])
    return jsonify(thong_tin)



def save_user_to_mysql(user_name , password, email,link_avatar,ip_register,device_register ):
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
                count_sk = 0
                count_view = 0
                count_comment = 0
                sql = f"INSERT INTO user (id_user , user_name , password, email ,link_avatar , ip_register , device_register, count_sukien, count_comment, count_view) VALUES ( {id_user} , %s, %s, %s, %s, %s , %s, {count_sk}, {count_view}, {count_comment} )"
                val = (user_name, password, email, link_avatar, ip_register, device_register)
                mycursor.execute(sql, val)
                connection.commit()
        except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
        finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")




@app.route('/reset', methods=['POST'])
def reset_password():
    email = request.form.get('email')

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
        new_password = "abc"
        update_query = "UPDATE user SET password = %s WHERE email = %s"
        update_values = (new_password, email)
        cursor.execute(update_query, update_values)
        connection.commit()

        send_email(email, new_password)

        return jsonify({'message': 'Đã reset mật khẩu thành công và gửi email!'})
    else:
        return jsonify({'message': 'Không tìm thấy người dùng có tên đăng nhập {}'.format(email)})




@app.route('/changepassword/<string:id_user>', methods=['POST'])
def change_password(id_user):
    old_password = request.form.get('oldPassword')
    new_password = request.form.get('newPassword')
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    mycursor = connection.cursor()
    mycursor.execute(f"SELECT * FROM user WHERE id_user='{id_user}' AND password='{old_password}'")
    ketqua = mycursor.fetchall()
    num_rows = mycursor.rowcount
    thong_tin = {}
    if num_rows == 0:
        return jsonify({"ketqua":"Wrong user ID or old password."})
    for i in range(0, num_rows):
        update_query = "UPDATE user SET password = %s WHERE id_user = %s"
        update_values = (new_password, id_user)
        cursor.execute(update_query, update_values)
        connection.commit()
        thong_tin["id_user"] = ketqua[i][0]
        thong_tin["link_avatar"] = ketqua[i][1]
        thong_tin["user_name"] = ketqua[i][2]
        thong_tin["ip_register"] = ketqua[i][3]
        thong_tin["device_register"] = ketqua[i][4]
        thong_tin["email"] = ketqua[i][6]
        thong_tin["count_sukien"] = int(ketqua[i][7])
        thong_tin["count_comment"] = int(ketqua[i][8])
        thong_tin["count_view"] = int(ketqua[i][8])
    return jsonify(thong_tin)




@app.route('/profile/<string:id_user>', methods=['GET'])
def info_user(id_user):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    mycursor = connection.cursor()
    mycursor.execute(f"SELECT * FROM user where id_user='{id_user}'")
    ketquaEmail = mycursor.fetchall()
    phantupro = mycursor.rowcount


    mycursor.execute("SELECT COUNT(id_Comment) FROM comment WHERE id_user = {}".format(id_user))
        # lấy kết quả
    results = mycursor.fetchone()[0]
    update_query = "UPDATE user SET count_comment = {} WHERE id_user = {}".format(results, id_user)
    cursor.execute(update_query)
    connection.commit()


    # update count_sukien vao user
    mycursor.execute("SELECT COUNT(DISTINCT id_toan_bo_su_kien) FROM saved_sukien WHERE id_user = {}".format(id_user))
    count_sk = mycursor.fetchone()[0]
    update_query = "UPDATE user SET count_sukien = {} WHERE id_user = {}".format(count_sk, id_user)
    cursor.execute(update_query)
    connection.commit()    
    thong_tin = {}
    if phantupro == 0:
        return jsonify({"ketqua":"khong co user nay"})
    for i in range(0, phantupro):
        
        thong_tin["id_user"] = int(ketquaEmail[i][0])
        thong_tin["link_avatar"] = ketquaEmail[i][1]
        thong_tin["user_name"] = ketquaEmail[i][2]
        thong_tin["ip_register"] = ketquaEmail[i][3]
        thong_tin["device_register"] = ketquaEmail[i][4]
        thong_tin["email"] = ketquaEmail[i][6]
        thong_tin["count_sukien"] = int(ketquaEmail[i][7])
        thong_tin["count_comment"] = int(ketquaEmail[i][8])
        thong_tin["count_view"] = int(ketquaEmail[i][8])
    return jsonify(thong_tin)

def send_email(email, new_password):
    #day la gmail mac dinh de gui den tat ca gmail khac va can phai bat xac thuc 2 yeu to
    from_address = "qn2012198@gmail.com" 
    password = "xoqjazdjndjzlkur"  

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = email
    msg['Subject'] = "Social Thinkdiff Company reset password"

    body = f'Your new password is: {new_password}'
    msg.attach(MIMEText(body.format(email), 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_address, password)
        server.sendmail(from_address, email, msg.as_string())


if __name__ == '__main__':
    with app.app_context():
        app.run(host='0.0.0.0', port=8888)