        # while (True):
        #     get_id = {}
        #     try:
        #         mycursor = get_mycursor(config)
        #         cursor = connection.cursor
        #         random_sukien = ['skchiatay', 'skdamcuoi', 'skhanhphuc', 'skkethon', 'skmuasam', 'sklyhon']
        #         print(random_sukien[index_demo])

        #         Item_Su_Kien = Random_Su_Kien(random_sukien, index_demo, mycursor)
        #         print("thongtin ne", Item_Su_Kien["image husband"])

        #         choose_case = choose_case_ne(Item_Su_Kien, filename3, filename4)
        #         print("choose_Case ", choose_case)


        #         if choose_case == 1:
        #             link_img = Link_Img_Swap_1_Face(filename2, filename4, list_API_KEY, "output1")
        #             print("Link ne", link_img[2])
        #             Item_Su_Kien["Link_img"] = link_img[2]
        #             print("Link2 ne", Item_Su_Kien["Link_img"])          
        #         if choose_case == 2:
        #             link_img = Link_Img_Swap_1_Face(filename1, filename3, list_API_KEY, "output1")
        #             print("Link ne", link_img[2])
        #             Item_Su_Kien["Link_img"] = link_img[2]
        #             print("Link2 ne", Item_Su_Kien["Link_img"])
        #         if choose_case == 3:
        #             if Item_Su_Kien["vtrinam"] == "namsau":
        #                 link_img = Link_Img_Swap_2_Face(filename1, filename2, filename3, filename4, list_API_KEY)
        #                 print("Link ne", link_img)
        #                 Item_Su_Kien["Link_img"] = link_img
        #                 print("Link2 ne", Item_Su_Kien["Link_img"])
        #             else:
                        
        #                 link_img = Link_Img_Swap_2_Face(filename1, filename2, filename3, filename4, list_API_KEY)
        #                 print("Link ne", link_img)   
        #                 Item_Su_Kien["Link_img"] = link_img    
        #                 print("Link2 ne", Item_Su_Kien["Link_img"])                
        #         if choose_case == 4:
        #             result_img = 'results/output.jpg'

        #             api_key = "9011a7cfd693ed788a0a98814fc7a118"
        #             direct_link = upload_image_to_imgbb(result_img, api_key)
        #             Item_Su_Kien["Link_img"] = direct_link

        #         list_return_data.append(Item_Su_Kien)
        #         # Lưu các thay đổi vào database
        #         connection.commit()
        #         print(mycursor.rowcount, "record inserted.")

        #     except mysql.connector.Error as error:
        #         print(f"Failed to connect to MySQL database: {error}")
        #     finally:
        #         if 'connection' in locals() and connection.is_connected():
        #             cursor.close()
        #             connection.close()
        #             print("MySQL connection closed")
        #     print("index_demo: ", index_demo)
        #     index_demo += 1
        #     if index_demo == 2:
        #         break

        # try:
        #     if connection.is_connected():
        #         print("Connected to MySQL database")
        #         cursor = connection.cursor()
        #         cursor.execute("SELECT DATABASE();")
        #         db_name = cursor.fetchone()[0]
        #         print(f"You are connected to database: {db_name}")
        #     index_vs2 = 0
        #     mycursor = connection.cursor()
        #     mycursor.execute(f"SELECT MAX(id_toan_bo_su_kien) from saved_sukien")
        #     result_id_sk = mycursor.fetchall()

        #     while True:
        #         mycursor.execute(f"SELECT MAX(id_saved) from saved_sukien")
        #         result2 = mycursor.fetchall()

        #         date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        #         get_id["id_toan_bo_su_kien"] = result_id_sk[0][0] + 1
        #         get_id["real_time"] = date
        #         print(list_return_data[index_vs2]["Link_img"])
        #         print("hallooooooo")
        #         sql = f"INSERT INTO saved_sukien (id_saved ,link_nam_goc , link_nu_goc ,link_nam_chua_swap , link_nu_chua_swap, link_da_swap , thoigian_swap , ten_su_kien , noidung_su_kien , id_toan_bo_su_kien ,so_thu_tu_su_kien) VALUES ( {result2[0][0] + 1} ,%s, %s , %s ,%s ,%s  , %s  ,%s,%s,{result_id_sk[0][0] + 1},{index_vs2})"
        #         val = (link_full1, link_full2, list_return_data[index_vs2]["image husband"],
        #                list_return_data[index_vs2]["image wife"], list_return_data[index_vs2]["Link_img"],
        #                get_id["real_time"], list_return_data[index_vs2]["tensukien"],
        #                list_return_data[index_vs2]["thongtin"])
        #         print("val ne: ", val)
        #         mycursor.execute(sql, val)
        #         index_vs2 += 1
        #         if index_vs2 == 2:
        #             break

        #     get_id_js.append(get_id)

        #     # Lưu các thay đổi vào database
        #     connection.commit()
        #     # mycursor.execute("SELECT thongtin from skhanhphuc")
        #     print(mycursor.rowcount, "aloooo record inserted.")
        # except mysql.connector.Error as error:
        #     print(f"Failed to connect to MySQL database: {error}")
        # finally:
        #     if 'connection' in locals() and connection.is_connected():
        #         cursor.close()
        #         connection.close()
        #         print("MySQL connection closed")
        # return jsonify(json1=list_return_data, json2=get_id_js)