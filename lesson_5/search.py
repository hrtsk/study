import pandas as pd
import eel
import os
import sys

### デスクトップアプリ作成課題
def kimetsu_search(word, path, file_name):
    # 検索対象取得
    file_dir = os.path.dirname(sys.argv[0])
    dir = os.path.dirname(file_dir)
    df=pd.read_csv(os.path.join(dir, file_name))
    source=list(df["name"]) #type: ignore
    # 検索
    if word in source:
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
    