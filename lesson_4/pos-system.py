import pandas as pd
import datetime as dt

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

### オーダークラス
class Order(Item):
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_master=item_master
        self.receipt_list=[]
    
    def add_item_order(self,item_code, order_num):
        self.item_order_list.append([item_code, int(order_num)])

    def calculate_change(self, sum):
        while True:
            deposit = input("お預かり金は >>")
            change = int(deposit) - sum
            if change < 0:
                print("お金が不足しています。")
                continue
            else:
                break
        self.receipt_list.append(f"お預かり金: {deposit}")
        print(f'{change}円のお返しになります。')
        self.receipt_list.append(f"お釣り: {change}")
        
    def get_receipt(self, list):
        df = pd.DataFrame(list)
        time = dt.datetime.now().strftime('%Y%m%d%H%M%S')
        df.to_csv(f"{time}.csv", sep=",", index=False, header=False)
        
    def view_item_list(self):
        total_price = 0
        total_number = 0
        for item in self.item_order_list:
            num = int(item[0].lstrip(r'0*')) - 1
            i_ = self.item_master[num]
            print(f"商品名:{i_.item_name} 価格:{i_.price} 個数:{item[1]}")
            self.receipt_list.append(f"商品名:{i_.item_name} 価格:{i_.price} 個数:{item[1]}")
            total_price += int(i_.price) * item[1]
            total_number += item[1]
        print(f"合計金額: {total_price} 合計個数: {total_number}")
        self.receipt_list.append(f"合計金額: {total_price} 合計個数: {total_number}")
        self.calculate_change(total_price)
        self.get_receipt(self.receipt_list)

### メイン処理
def main():
    # マスタ登録
    item_master=[]
    
    CSV_PATH = './item_master.csv'
    df = pd.read_csv(CSV_PATH, dtype=str, encoding='utf_8_sig') #type: ignore
    for i in df.values:
        item_master.append(Item(i[0],i[1],i[2]))
    #print(item_master)
    #item_master.append(Item("001","りんご",100))
    #item_master.append(Item("002","なし",120))
    #item_master.append(Item("003","みかん",150))
    
    # オーダー登録
    order=Order(item_master)
    while True:
        order_code = input("オーダーしたい商品のコードを入力してください >> ")
        if int(order_code) > len(item_master) or int(order_code) == 0:
            print("そのコードの商品は登録されておりません。")
            continue
        order_num = input("オーダーしたい個数を入力してください >> ")
        order.add_item_order(order_code, order_num)
        next_order = input("さらにオーダーしますか?\nオーダーする場合、9を入力してください >> ")
        if next_order != "9":
            break
    #order.add_item_order("001")
    #order.add_item_order("002")
    #order.add_item_order("003")
    
    # オーダー表示
    order.view_item_list()
    
if __name__ == "__main__":
    main()