import eel
import desktop
import pos
import sys
import re

app_name="html"
end_point="index.html"
size=(710,540)

total_price = 0
bought_items = ""
receipt = ""
ERROR = "最初からやり直してください"

@eel.expose
def print_cart_by_py(input_file, code, num):
    # 商品登録
    item_master = pos.add_item_master_by_csv(input_file)
    if item_master == []:
        eel.erorrMessage(f"マスタ登録失敗\n{ERROR}") #type:ignore
        sys.exit()
    order = pos.Order(item_master)
    try:
        re.fullmatch(r'[1-9][0-9]*', num).group() #type:ignore
    except:
        eel.errorMessage("購入数は1以上の整数を入力してください") #type: ignore
    code_list = []
    for i in item_master:
        code_list.append(i.item_code)
        
    if code in code_list:
        item_data = order.get_item_data(code)
        order.add_item_order(code, num)
    
        item = f'商品:{item_data[0]} 価格:{item_data[1]} 個数:{num}' #type: ignore
        global total_price
        total_price += int(item_data[1]) * int(num) #type: ignore
        global bought_items
        bought_items += item + "\n"
        global receipt
        receipt = bought_items + f"合計金額:{total_price}円"
        eel.printReceiptByJs(receipt) #type: ignore
    else:
        eel.errorMessage("商品コードエラー") #type: ignore

@eel.expose       
def calculate_change_by_py(deposit):
    global total_price
    change = int(deposit) - total_price
    if change < 0:
        eel.errorMessage("支払金不足") #type: ignore
    global receipt
    result = receipt + f'\n\nお預かり:{deposit}円\n' + f'お釣り:{change}円'
    pos.Order.write_receipt(result) #type: ignore
    eel.printReceiptByJs(result) #type: ignore

desktop.start(app_name,end_point,size)
#desktop.start(size=size,appName=app_name,endPoint=end_point)
