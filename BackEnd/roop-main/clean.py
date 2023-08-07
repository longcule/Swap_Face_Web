import argparse
from socket import socket
import cv2
from flask import request, jsonify
import mysql.connector
from numpy import random
import datetime
import random
from PIL import Image
from datetime import datetime
import base64
import json
import shutil
from  checkImgbb import check_imgbb_update,check_imgbb_api_key
import requests
from datetime import datetime
import numpy as np
from roop import core
import roop.globals
from flask import Flask, stream_with_context, Response
# Config database mysql
config = {
                'user': 'phpmyadmin',
                'password': 'password',
                'host': 'localhost',
                'port': 3306,
                'database': 'futureLove4'
            }    

connection = mysql.connector.connect(**config)


def download_image(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
        # print(response.raw ,"****")
    del response

def upload_image_to_imgbb(image_path, api_key):
    # Tải dữ liệu ảnh
    with open(image_path, "rb") as file:
        payload = {
            "key": api_key,
            "image": base64.b64encode(file.read()),
        }
    # Gửi yêu cầu POST tải lên ảnh đến API của ImgBB
    response = requests.post("https://api.imgbb.com/1/upload", payload)

    # Trích xuất đường dẫn trực tiếp đến ảnh từ JSON response
    json_data = json.loads(response.text)
    direct_link = json_data["data"]["url"]

    # Trả về đường dẫn trực tiếp đến ảnh
    return direct_link
 
def get_mycursor(config):
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
            return cursor
        
def Random_Su_Kien(random_sukien, index_demo, mycursor):
    
    Item_Su_Kien = {}
    Item_Su_Kien["tensukien"] = random_sukien[index_demo]
    index_sk = [random.randint(1, 25), random.randint(1, 25), random.randint(1, 25), random.randint(1, 25),
            random.randint(1, 25), random.randint(1, 25), random.randint(1, 25), random.randint(1, 25),
            random.randint(1, 25), random.randint(1, 25)]    
    print("index  sk ", random_sukien[index_demo])
    mycursor.execute(f"SELECT thongtin FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
    thongtin_sql = mycursor.fetchall()
    print('thongtin_sql', thongtin_sql[0])
    thongtin = ', '.join(thongtin_sql[0])
    print('thong tin ', thongtin)
    Item_Su_Kien["thongtin"] = thongtin


    mycursor.execute(f"SELECT image FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
    image_sql = mycursor.fetchall()
    print('image_sql', image_sql[0])
    image = ', '.join(image_sql[0])
    print('image_full ', image)
    Item_Su_Kien["image couple"] = image

    mycursor.execute(f"SELECT vtrinam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
    vtrinam_sql = mycursor.fetchall()
    print('vtrinam_sql', vtrinam_sql[0])
    vtrinam = ', '.join(vtrinam_sql[0])
    print('vtrinam ', vtrinam)
    Item_Su_Kien["vtrinam"] = vtrinam


    mycursor.execute(f"SELECT nam FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
    img_nam_sql = mycursor.fetchall()
    print('img_nam_sql', img_nam_sql[0])
    print("***")
    img_nam = ', '.join(img_nam_sql[0])
    print('img_nam', img_nam)
    Item_Su_Kien["image husband"] = img_nam

    mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
    img_nu_sql = mycursor.fetchall()
    print('img_nu_sql', img_nu_sql[0])
    print("***")
    img_nu = ', '.join(img_nu_sql[0])
    print('img_nu', img_nu)
    Item_Su_Kien["image wife"] = img_nu

    mycursor.execute(f"SELECT tomLuocText FROM {random_sukien[index_demo]} where id={index_sk[index_demo]}")
    tom_luoc_text = mycursor.fetchall()
    print('tom luoc text', tom_luoc_text[0])
    print("***")
    tom_luoc = ', '.join(tom_luoc_text[0])
    print('tom luoc text', tom_luoc)
    Item_Su_Kien["tom luoc"] = tom_luoc

    return Item_Su_Kien

def choose_case_ne(Item, filename3, filename4):
    choose_case_func = 0
    if Item["image husband"] == "0" and Item["image wife"] == "0" and Item["image couple"] != "0":
        choose_case_func = 4
        download_image(Item["image couple"], "results/output_no.jpg")
    elif Item["image husband"] == "0" and Item["image wife"] != "0":
        choose_case_func = 1
        download_image(Item["image wife"], filename4)
        download_image(Item["image wife"], "results/output_single_nu.jpg")
    elif Item["image wife"] == "0" and Item["image husband"] != "0":
        choose_case_func = 2
        download_image(Item["image husband"], filename3)
        download_image(Item["image husband"], "results/output_single_nam.jpg")
    else:
        choose_case_func = 3
        download_image(Item["image husband"], filename3)
        download_image(Item["image wife"], filename4)

        download_image(Item["image husband"], "results/out_img_nam.jpg")
        download_image(Item["image wife"], "results/out_img_nu.jpg")
        
    return choose_case_func

def Link_Img_Swap_1_Face(src_img, dst_img, out_img, list_API_KEY):

    out_file = out_img
    args = argparse.Namespace(
        src=src_img,
        dst=dst_img,
        out="results/" + out_file + ".jpg",
        warp_2d=False,
        correct_color=False,
        no_debug_window=True,
    )

    roop.globals.source_path = args.src
    roop.globals.target_path = args.dst
    roop.globals.output_path = args.out

    core.run()

    output_path = "results/" + out_file + ".jpg"

    for i in range(0, 11):
        if check_imgbb_api_key(list_API_KEY[i]) == True:
            api_key = list_API_KEY[i]
    direct_link = upload_image_to_imgbb(output_path, api_key)
    print("api key: ", api_key)

    return output_path, direct_link




def Link_Img_Swap_2_Face(src_nam, src_nu, dst_nam, dst_nu, list_API_KEY ):
    
    output1 = "out_img_nam"
    output2 = "out_img_nu"
    
    # swap_face nam
    Link_Img_Swap_1_Face(src_nam, dst_nam, output1, list_API_KEY)
    #swap_face nu
    Link_Img_Swap_1_Face(src_nu, dst_nu, output2, list_API_KEY)

    image1 = Image.open("results/" + output1 + ".jpg")
    image2 = Image.open("results/" + output2 + ".jpg")

    width1, height1 = image1.size
    width2, height2 = image2.size
    max_width = max(width1, width2)
    max_height = max(height1, height2)
    new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
    new_image.paste(image2, (0, 0))
    new_image.paste(image1, (max_width, 0))
    new_image.save('results/output_full.jpg')

    result_img = 'results/output_full.jpg'

    for i in range(0, 11):
        if (check_imgbb_api_key(list_API_KEY[i]) == True):
              api_key = list_API_KEY[i]

    direct_link = upload_image_to_imgbb(result_img, api_key)
    print("api key: ", api_key)

    return direct_link

def randomGenData(random_case,random_sukien, link_full1, link_full2, save_sk, num):

    print("link1:",link_full1)
    print("link2:",link_full2)

    list_API_KEY = [
                    '0648864ce249f9b501bb3ff7735eb1cd', 'ddc51a8c2a1ed5ef16a9faf321c6821a',
                    '9011a7cfd693ed788a0a98814fc7a118', 'ef1cb4ba4157f0abf53fa17447f10fe7',
                    '31aef57415d034fdb2489d3bedf5d6a4', '6374d7c9cfa9f0cb372098bdf76d806e',
                    '21778d638b0d33c5d855729746deba81', '0cb8df6d364699a53973c9a6ce3c4466',
                    'e3a75062a4e22018ad8c3ab8f24eee5c', '7239a119b60707f567ebd17c097f5696',
                    '92cd47cbd5c08f5465d6f5d465bf4f8d']
    index_demo = 0
    list_return_data = []
    src_nam = 'imgs/anhtam1.jpg'
    src_nu = 'imgs/anhtam2.jpg'
    dst_nam = 'imgs/anhtam3.jpg'
    dst_nu = 'imgs/anhtam4.jpg'

        # Tải ảnh từ Link trong header
    download_image(link_full1, src_nam)
    download_image(link_full2, src_nu)   
    print("random_case", random_case)
    device_them_su_kien = request.args.get('device_them_su_kien') 
    ip_them_su_kien =  request.args.get('ip_them_su_kien')
    id_user =  request.args.get('id_user')    
    ten_nam = request.args.get('ten_nam')
    ten_nu = request.args.get('ten_nu')  
    count_comment = 0
    count_view = 0


    while (True):
            get_id = {}
            try:
                mycursor = get_mycursor(config)
                cursor = connection.cursor
                Item_Su_Kien = Random_Su_Kien(random_sukien, index_demo, mycursor)
                choose_case = choose_case_ne(Item_Su_Kien, dst_nam, dst_nu)
                print("choose_Case ", choose_case)


                if choose_case == 1:
                    output = "output_single_nu"
                    link_img = Link_Img_Swap_1_Face(src_nu, dst_nu, output, list_API_KEY)
                    print("Link ne", link_img[1])
                    Item_Su_Kien["Link_img"] = link_img[1]
                     

                if choose_case == 2:
                    output = "output_single_nam"
                    link_img = Link_Img_Swap_1_Face(src_nam, dst_nam, output, list_API_KEY)
                    print("Link ne", link_img[1])
                    Item_Su_Kien["Link_img"] = link_img[1]
                   


                if choose_case == 3:
                    if Item_Su_Kien["vtrinam"] == "namsau":
                        link_img = Link_Img_Swap_2_Face(src_nam, src_nu, dst_nam, dst_nu, list_API_KEY)
                        print("Link ne", link_img)
                        Item_Su_Kien["Link_img"] = link_img
                        
                    else:
                        
                        link_img = Link_Img_Swap_2_Face(src_nu, src_nam, dst_nu, dst_nam, list_API_KEY)
                        print("Link ne", link_img)   
                        Item_Su_Kien["Link_img"] = link_img    
                              


                if choose_case == 4:
                    Item_Su_Kien["Link_img"] = Item_Su_Kien["image couple"]


                date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                Item_Su_Kien["thoi gian"] = date
                Item_Su_Kien["so_thu_tu_su_kien"] = index_demo + 1
                list_return_data.append(Item_Su_Kien)
                mycursor.execute(f"SELECT MAX(id_toan_bo_su_kien) from {save_sk}")
                result_id_sk = mycursor.fetchall()


                if index_demo == 5:
                    for index_vs2 in range(6):
                        phantram_loading = (index_demo + 1) * 10
                        list_return_data[index_vs2]["phantram_loading"] = phantram_loading
                        mycursor.execute(f"SELECT MAX(id_saved) from {save_sk}")
                        result2 = mycursor.fetchall()      
                        date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                        get_id["id_toan_bo_su_kien"] = result_id_sk[0][0] + 1
                        get_id["real_time"] = date
                        list_return_data[index_vs2]["id_user"] = id_user
                        list_return_data[index_vs2]["id_toan_bo_su_kien"] = result_id_sk[0][0] + 1
                        id_template = random.randint(1, 4)
                        list_return_data[index_vs2]["id_template"] = id_template

                        print(list_return_data[index_vs2]["Link_img"])
                        print("hallooooooo")
                        sql = f"INSERT INTO {save_sk} (id_saved ,link_nam_goc , link_nu_goc ,link_nam_chua_swap , link_nu_chua_swap, link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , id_toan_bo_su_kien ,so_thu_tu_su_kien, thoigian_sukien, device_them_su_kien, ip_them_su_kien, id_user, tomLuocText, ten_nam, ten_nu, count_comment, count_view, id_template, phantram_loading) VALUES ( {result2[0][0] + 1}  ,%s  , %s  ,%s, %s, %s, %s, %s, %s, {result_id_sk[0][0] + 1},{ list_return_data[index_vs2]['so_thu_tu_su_kien'] }, %s, %s, %s, {id_user}, %s, %s, %s, {count_comment}, {count_view}, { list_return_data[index_vs2]['id_template'] }, {phantram_loading})"
                        val = (link_full1, link_full2, list_return_data[index_vs2]["image husband"], list_return_data[index_vs2]["image wife"], list_return_data[index_vs2]["Link_img"], list_return_data[index_vs2]["thoi gian"], list_return_data[index_vs2]["tensukien"], list_return_data[index_vs2]["thongtin"], date, device_them_su_kien, ip_them_su_kien, list_return_data[index_vs2]["tom luoc"], ten_nam, ten_nu)
                        mycursor.execute(sql, val)
                        connection.commit()
                        index_vs2 += 1    

                    return jsonify(sukien=list_return_data)              
                
                if num == 7:
                        if index_demo <= 3:
                            mycursor.execute(f"SELECT MAX(id_saved) from {save_sk}")
                            result2 = mycursor.fetchall()   
                            phantram_loading = (index_demo + 7) * 10
                            id_template = random.randint(1, 4)
                            Item_Su_Kien["id_template"] = id_template
                            Item_Su_Kien["phantram_loading"] = phantram_loading
                            sql = f"INSERT INTO saved_sukien_ngam (id_saved ,link_nam_goc , link_nu_goc ,link_nam_chua_swap , link_nu_chua_swap, link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , id_toan_bo_su_kien ,so_thu_tu_su_kien, thoigian_sukien, device_them_su_kien, ip_them_su_kien, phantram_loading, tomLuocText) VALUES ( {result2[0][0] + 1}  ,%s  , %s  ,%s, %s, %s, %s, %s, %s, {result_id_sk[0][0]},{index_demo + 7}, %s, %s, %s, %s, %s)"
                            val = (link_full1, link_full2, Item_Su_Kien["image husband"], Item_Su_Kien["image wife"], Item_Su_Kien["Link_img"], Item_Su_Kien["thoi gian"], Item_Su_Kien["tensukien"], Item_Su_Kien["thongtin"], date, device_them_su_kien, ip_them_su_kien, phantram_loading, Item_Su_Kien["tom luoc"])
                            mycursor.execute(sql, val)
                            connection.commit()

                            sql2 = f"INSERT INTO saved_sukien (id_saved ,link_nam_goc , link_nu_goc ,link_nam_chua_swap , link_nu_chua_swap, link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , id_toan_bo_su_kien ,so_thu_tu_su_kien, thoigian_sukien, device_them_su_kien, ip_them_su_kien, id_user, tomLuocText, ten_nam, ten_nu, count_comment, count_view, id_template, phantram_loading) VALUES ( {result2[0][0] + 1}  ,%s  , %s  ,%s, %s, %s, %s, %s, %s, {result_id_sk[0][0]},{index_demo + 7}, %s, %s, %s, {id_user}, %s, %s, %s, {count_comment}, {count_view}, {Item_Su_Kien['id_template']}, {phantram_loading})"
                            val2 = (link_full1, link_full2, Item_Su_Kien["image husband"], Item_Su_Kien["image wife"], Item_Su_Kien["Link_img"], Item_Su_Kien["thoi gian"], Item_Su_Kien["tensukien"], Item_Su_Kien["thongtin"], date, device_them_su_kien, ip_them_su_kien, Item_Su_Kien["tom luoc"], ten_nam, ten_nu)
                            mycursor.execute(sql2, val2)
                            connection.commit()
                        else:
                            return jsonify(sukien=list_return_data)
                # Lưu các thay đổi vào database
                print(mycursor.rowcount, "record inserted.")
            except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")
            print("index_demo: ", index_demo)
            index_demo += 1


            if index_demo == 10:
                break

    return jsonify(sukien=list_return_data)
