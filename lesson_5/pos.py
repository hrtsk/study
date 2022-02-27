import pandas as pd
import datetime
import os

RECEIPT_FOLDER="./receipt"
os.makedirs(RECEIPT_FOLDER, exist_ok=True)

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price,stock):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
        self.stock=stock

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_count_list=[]
        self.item_master=item_master

    def add_item_order(self,item_code,item_count):
        self.item_order_list.append(item_code)
        self.item_count_list.append(item_count)
        
    def view_item_list(self):
        for item in self.item_order_list:
            print(f"商品コード:{item}")
            
    def get_item_data(self,item_code):
        for m in self.item_master:
            if item_code==m.item_code:
                return m.item_name,m.price,m.stock
    
    @staticmethod
    def write_receipt(text):
        with open(RECEIPT_FOLDER + "/" + f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.csv' , mode="a", encoding="utf-8_sig") as f: # type: ignore
            f.write(text) 
                
    # マスタ登録(課題３)
    @staticmethod
    def add_item_master_by_csv(csv_path):
        item_master=[]
        try:
            item_master_df=pd.read_csv(csv_path,dtype={"item_code":object}) # CSVでは先頭の0が削除されるためこれを保持するための設定
            for item_code,item_name,price,stock in zip(list(item_master_df["item_code"]),list(item_master_df["item_name"]),list(item_master_df["price"]),list(item_master_df["stock"])):
                item_master.append(Item(item_code,item_name,price,stock))
            return item_master
        except:
            return item_master
