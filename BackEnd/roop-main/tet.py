import random
sukien_lists = ['skGapNhau','skhanhphuc', 'skkethon', 'skSinhConDauLong', 'sktuoigia']
sukien_lists1 = ['skngoaitinh', 'skDuDoanMatCon','skmuasam', 'skmaymua', 'skToTinh', 'skchiatay']
sukien_lists2 = ['skConLapGiaDinh', 'skkhongphaiconde', 'skSinhConThuHai', 'sknym']
sukien_lists3 = ['sklyhon', 'skmuasam','skDuDoanMatCon', 'skmaymua', 'skchiatay', 'skngoaitinh'  ]
sukien_lists4 = ['skvohoacchongchettruoc', 'skchaunoi']
list_gen_sk = []
list_gen_sk.append(sukien_lists[0])
random_sk1 = random.sample(sukien_lists1, 2)
list_gen_sk.append(random_sk1[0])
list_gen_sk.append(sukien_lists[1])
list_gen_sk.append(random_sk1[1])
list_gen_sk.append(sukien_lists[2])
while True:
    sk = random.choice(sukien_lists3)
    if sk not in list_gen_sk:
        list_gen_sk.append(sk)
        break

list_gen_sk.append(sukien_lists[3])
random_sk2 = random.choice(sukien_lists2)
list_gen_sk.append(random_sk2)
list_gen_sk.append(sukien_lists[4])
random_sk3 = random.choice(sukien_lists4)
list_gen_sk.append(random_sk3)
print(list_gen_sk)