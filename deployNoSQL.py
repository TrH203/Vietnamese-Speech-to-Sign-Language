import numpy as np
import pymongo
from pymongo.server_api import ServerApi
import json

uri = "mongodb+srv://hienne:Hoangtrhien@cluster0.6kb7cuk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def insert_intoDatabase(word, numpy_arr):

    matrix_3d = numpy_arr

    matrix_list = matrix_3d.tolist()

    # init connect to MongoDB
    try:
        client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
        db = client["hand_database"]
        collection = db["hand_collection"]
        print("Kết nối thành công!!!")
    except Exception as e:
        print(e)
        
    # create document to save ({key: value} = word : datapoint)
    matrix_document = {
        word: matrix_list
    }

    # saving
    collection.insert_one(matrix_document)

    print("Ma trận đã được lưu trữ thành công!")
