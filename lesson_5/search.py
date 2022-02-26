import pandas as pd
import eel
import os
import sys

#def kimetsu_search(word, path, file_name):
def main():
    
    # 検索対象取得
    """"
    file_dir = os.path.dirname(sys.argv[0])
    dir = os.path.dirname(file_dir)
    df=pd.read_csv(os.path.join(dir, file_name))
    source=list(df["name"]) #type: ignore
    """
    CSV_PATH = './item_master.csv'
    df = pd.read_csv(CSV_PATH, dtype=str, encoding='utf_8_sig') #type: ignore
    code_list = list(df["item_code"])
    
    code_num = eel.codeNumByJs() #type: ignore
    
    # 検索
    if code_num in code_list:
        msg_1 = "『{}』はあります。\n".format(word)
        print(msg_1)
        eel.view_log_js(msg_1) #type: ignore
    else:
        msg_2 = "『{}』はありません。\n".format(word)
        print(msg_2)
        eel.view_log_js(msg_2) #type: ignore
        # 追加
        #add_flg=input("追加登録しますか？(0:しない 1:する)　＞＞　")
        #if add_flg=="1":
        source.append(word)
        msg_3 = "『{}』をリストに追加しました。\n".format(word)
        print(msg_3)
        eel.view_log_js(msg_3) #type: ignore
    
    # CSV書き込み
    df=pd.DataFrame(source,columns=["name"])
    df.to_csv(path, encoding="utf_8-sig")
    print(source)
    
if __name__ == "__main__":
    main()