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
  
def test_get_items():
  result = get_items()
  
  assert result["Items"]
  assert result["Items"][0]["Item"]["itemName"]
  assert result["Items"][0]["Item"]["itemPrice"]
  

def test_get_item_mix_max_price():
  max, min = get_item_mix_max_price()

  assert max
  assert min
  assert max > min
  
def test_get_items_by_category():
  result = get_items_by_category()
  
  assert result["Items"]
  assert len(result["Items"]) >= 1
  assert result["Items"][0]["Item"]["itemName"]
  assert result["Items"][0]["Item"]["itemPrice"]