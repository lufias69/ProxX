import pandas as pd
from json import load, dump

# Buka JSON file
# try:
#     # returns JSON object as 
#     # a dictionary
#     f = open('data_kategorikal_.json',)
#     data_kategorikal_ = load(f)
# except:
#     data_kategorikal_ = None

# try:
#     f = open('median_data.json',)
#     median_data_ = load(f)
# except:
# #     print("no mediaa")
#     median_data_ = None

def praproses_data_test(data_frame, fill_nan_with_median = True):

    try:
        # returns JSON object as 
        # a dictionary
        f = open('data_kategorikal_.json',)
        data_kategorikal_ = load(f)
    except:
        data_kategorikal_ = None

    try:
        f = open('median_data.json',)
        median_data_ = load(f)
    except:
    #     print("no mediaa")
        median_data_ = None

    data_frame.columns= data_frame.columns.str.strip().str.lower()
    for kolom in data_frame.columns:
        try: #yang diubah hanya data yang bertipe string
            data_frame[kolom] = data_frame[kolom].str.lower()
        except: #jika data bukan bertipe string maka akan dilewati (pass)
            data_frame[kolom] = data_frame[kolom].fillna(median_data_[kolom])

    data_frame = data_frame.fillna("NA")

    #mengubah dataframe menjadi numerical
    for kolom in data_frame.columns:
        if kolom in data_kategorikal_:
            # print(kolom,end=" ")
            for i in data_kategorikal_[kolom]:
                data_frame[kolom] = data_frame[kolom].replace(i, data_kategorikal_[kolom][i])
    return data_frame


def praproses(data_frame, fill_nan_with_median=True, data_training = False):
    # ubah nama kolom menjadi lower
    data_frame.columns= data_frame.columns.str.strip().str.lower()
    
    #membuat mean data dari dataframe
    if data_training == True:
        median_data = data_frame.mean()
        with open('median_data.json', 'w') as f:
            dump(dict(median_data), f)
    
        #proses merubah data menjadi lower
        #dan merubah null data menjadi median
        for kolom in data_frame.columns:
            try: #yang diubah hanya data yang bertipe string
                data_frame[kolom] = data_frame[kolom].str.lower()
            except: #jika data bukan bertipe string maka akan dilewati (pass)
                data_frame[kolom] = data_frame[kolom].fillna(median_data[kolom])#data median diambil dari line 25
        data_frame = data_frame.fillna("NA")
    #membuat dictionary untuk mengubah data Kategorikal menjadi numerical
    # if data_training == True:
        data_kategorikal = dict()
        for nama_kolom in data_frame.columns:
            
            if nama_kolom != 'id':
                set_data = list(set(data_frame[nama_kolom]))
                if type(set_data[0]) == str:
                    if 'NA' in set_data:
                        set_data[set_data.index('NA')], set_data[0] = set_data[0], set_data[set_data.index('NA')]
                        index_set_data = [i for i in range(len(set_data))]
                    else:
                        # print(nama_kolom)
                        set_data.append("NA")
                        index_set_data = [i for i in range(len(set_data))]

                    data_kategorikal[nama_kolom] = dict(zip(set_data,index_set_data))
                else:
                    pass

            #simpan data di hdd (format json)      
            with open('data_kategorikal_.json', 'w') as f:
                dump(data_kategorikal, f)
                
    #mengubah dataframe menjadi numerical    
        for kolom in data_frame.columns:
            if kolom in data_kategorikal:
                for i in data_kategorikal[kolom]:
                    data_frame[kolom] = data_frame[kolom].replace(i, data_kategorikal[kolom][i])     
    else:
        return praproses_data_test(data_frame, fill_nan_with_median = True)
    #     for kolom in data_frame.columns:
    #         if kolom in data_kategorikal_:
    #             for i in data_kategorikal_[kolom]:
    #                 data_frame[kolom] = data_frame[kolom].replace(i, data_kategorikal_[kolom][i])
    return data_frame

def get_key(val, my_dict):
    for key, value in my_dict.items():
         if val == value:
             return key
    #cek data Numerical
def cek_data_Numerical(nama_kolom, angka):

    f = open('data_kategorikal_.json',)
    data_kategorikal_ = load(f)

    if nama_kolom in data_kategorikal_:
        if angka in data_kategorikal_[nama_kolom].values():
            print(str(angka)+":'"+get_key(angka, data_kategorikal_[nama_kolom])+"'")
        else:
            print('angka tidak ada')             
    else:
        print("cek nama kolom")
    print("")
    print("jumlah data", len(data_kategorikal_[nama_kolom]))
#     print(data_kategorikal[nama_kolom][angka])

    