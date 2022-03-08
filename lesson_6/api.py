import requests
import pandas as pd
import datetime

APP_ID = "1081675625476532194"

def get_datetime():
  dt_now = datetime.datetime.now()
  return dt_now.strftime('%Y%m%d')
  
def get_api(url, params: dict):
  result = requests.get(url, params=params)
  return result.json()

def get_items():
  url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
  
  params = {
    "format": "json",
    "keyword": "Python",
    "applicationId": APP_ID
  }
  result = get_api(url, params=params)
  
  print(result["Items"][0]["Item"]["itemName"])
  print(result["Items"][0]["Item"]["itemPrice"])
  return result

def get_item_mix_max_price():
  url = "https://app.rakuten.co.jp/services/api/Product/Search/20170426"
  params = {
    "format": "json",
    "productId": "6de7af896684b9e71647d70ddcaec07f",
    "applicationId": APP_ID
  }

  result = get_api(url, params=params)
  #print(json.dumps(result, indent=4))
  #print(result["items"][0]["itemName"])
  
  max = result["Products"][0]["Product"]["maxPrice"]
  min = result["Products"][0]["Product"]["minPrice"]
  print(max)
  print(min)
  return max, min
  
def get_items_by_category():
  url = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628"
  genreid = 558929
  
  params = {
    "format": "json",
    "genreId": genreid,
    "applicationId": APP_ID
  }

  result = get_api(url, params=params)
  
  csv_list = []
  column = ["rank", "itemName", "itemPrice"]
  for i in result["Items"]:
    item = i["Item"]
    csv_list.append([item["rank"],item["itemName"],item["itemPrice"]])
    
  df = pd.DataFrame(csv_list, columns=column)
  df.to_csv(f"{genreid}_{get_datetime()}.csv")
  return result

if __name__ == '__main__':
  get_items()
  get_item_mix_max_price()
  get_items_by_category()
