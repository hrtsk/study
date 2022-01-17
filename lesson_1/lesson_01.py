#課題１：簡単な検索ツールの作成

#コメント
#列方向ではなく、行方向に追加していくかたちにしたのですが
#これでよかったでしょうか？

import csv

def search():
  source_list = csv_to_list()
  
  word = input("鬼滅の登場人物の名前を入力してください >>> ")
          
  if word in source_list:
    print("{}が見つかりました".format(word))
  else:
    print("{}は鬼滅には出てきません".format(word))
    print("Listに{}を追加しますか？".format(word))
    ans = input("追加する場合 Y を入力してください >>> ")
    if ans == "Y":
      source_list.append(word)     
      list_to_csv(source_list)     
      print("追加しました")
    else:
      print("追加せず終了します")

def csv_to_list():
  arr = []
  with open('source.csv', 'r', newline='') as f:
    for row in csv.reader(f):
      arr.extend(row)
  return arr
      
def list_to_csv(arr):
  with open('source.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(arr)
    
if __name__ == "__main__":
  search()
