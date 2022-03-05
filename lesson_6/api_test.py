from api import *

def test_get_datetime():
  assert get_datetime()

def test_get_api():
  url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
  appid = "1081675625476532194"
  
  # 正常系 → うまくいった時の処理
  params = {
    "format": "json",
    "keyword": "Python",
    "applicationId": appid
  }
  res = get_api(url, params=params)

  assert len(res["Items"]) >= 1
  assert res["Items"][0]["Item"]["itemCode"]

  # 異常系 → 失敗時の処理
  url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
  params = {
    "format": "json",
    "keyword": "하히후헤호",
    "applicationId": appid
  }
  res = get_api(url, params=params)
  
  assert len(res["Items"]) == 0
  
def test_task2():
  result = task2()
  
  assert result["Items"]
  assert result["Items"][0]["Item"]["itemName"]
  assert result["Items"][0]["Item"]["itemPrice"]
  

def test_task3():
  max, min = task3()

  assert max
  assert min
  assert max > min
  
def test_task4():
  result = task4()
  
  assert result["Items"]
  assert len(result["Items"]) >= 1
  assert result["Items"][0]["Item"]["itemName"]
  assert result["Items"][0]["Item"]["itemPrice"]