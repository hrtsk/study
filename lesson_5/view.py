import eel
import desktop
import pos
import pandas as pd
import re

app_name="html"
end_point="index.html"
size=(710,540)

total_price = 0
bought_items = ""
receipt = ""
count_dic = {}
first_loop = True
item_master = []

@eel.expose
def print_cart_by_py(input_file, code, num):
    # 商品登録
    global item_master
    item_master = pos.Order.add_item_master_by_csv(input_file) #type:ignore
    # 入力CHECK(マスタ登録)
    if item_master == []:
        eel.errorMessage("マスタ登録失敗") #type:ignore
        return
    order = pos.Order(item_master)
    
    # 入力CHECK(購入数)
    try:
        re.fullmatch(r'[1-9][0-9]*', num).group() #type:ignore
    except:
        eel.errorMessage("購入数は1以上の整数を入力してください") #type: ignore
        return
    
    code_list = []
    global count_dic
    global first_loop
    for i in item_master:
        if first_loop:
            code_list.append(i.item_code)
            count_dic[i.item_code] = 0
        else:
            code_list.append(i.item_code)
    first_loop =False
    
    if code in code_list:
        item_data = order.get_item_data(code)
        order.add_item_order(code, num)
        count_dic[code] += int(num)  #type: ignore
        
        # 入力CHECK(在庫数)
        if item_data[2] - count_dic[code] < 0: #type: ignore
            eel.errorMessage("在庫不足") #type: ignore
            return
        
        item = f'商品:{item_data[0]} 価格:{item_data[1]} 個数:{num} 在庫:{item_data[2] - count_dic[code]}' #type: ignore
        global total_price
        total_price += int(item_data[1]) * int(num) #type: ignore
        global bought_items
        bought_items += item + "\n"
        global receipt
        receipt = bought_items + f"合計金額:{total_price}円"
        eel.printReceiptByJs(receipt) #type: ignore
    else:
        # 入力CHECK(商品コード)
        eel.errorMessage("商品コードエラー") #type: ignore
        return

@eel.expose       
def calculate_change_by_py(input_file,deposit):
    global total_price
    change = int(deposit) - total_price
    
    # 入力CHECK(支払い金)
    if change < 0:
        eel.errorMessage("支払金不足") #type: ignore
        return
    
    global receipt
    result = receipt + f'\n\nお預かり:{deposit}円\n' + f'お釣り:{change}円'
    pos.Order.write_receipt(result) #type: ignore
    eel.printReceiptByJs(result) #type: ignore
    
    # 在庫管理/CSV上書き
    overwrite_list = []
    for item in item_master:
        item.stock -= count_dic[item.item_code]
        overwrite_list.append([item.item_code,item.item_name,item.price,str(item.stock)])
    df = pd.DataFrame(overwrite_list)
    df.columns=["item_code","item_name","price","stock"]
    df.to_csv(input_file, sep=",", index=False)
    
        
    
    #df = pd.DataFrame(item_master)
    
    #df.to_csv(input_file)

desktop.start(app_name,end_point,size)
#desktop.start(size=size,appName=app_name,endPoint=end_point)
