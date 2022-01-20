from fileinput import lineno
import os,sys 
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import urllib.parse

# Selenium4対応済

def set_driver(hidden_chrome: bool=False):
  '''
  Chromeを自動操作するためのChromeDriverを起動してobjectを取得する
  '''
  USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
  options = ChromeOptions()

  # ヘッドレスモード（画面非表示モード）をの設定
  if hidden_chrome:
      options.add_argument('--headless')

  # 起動オプションの設定
  options.add_argument(f'--user-agent={USER_AGENT}') # ブラウザの種類を特定するための文字列
  options.add_argument('log-level=3') # 不要なログを非表示にする
  options.add_argument('--ignore-certificate-errors') # 不要なログを非表示にする
  options.add_argument('--ignore-ssl-errors') # 不要なログを非表示にする
  options.add_experimental_option('excludeSwitches', ['enable-logging']) # 不要なログを非表示にする
  options.add_argument('--incognito') # シークレットモードの設定を付与
  
  # ChromeのWebDriverオブジェクトを作成する。
  service=Service(ChromeDriverManager().install())
  return Chrome(service=service, options=options) #type: ignore
  #動作に問題はないのですが、Pycharmから警告が出てしまいます。

def main():
    '''
    main処理
    '''
    search_keyword = input("検索キーワードを入力してください >> ")
    
    # driverを起動
    driver = set_driver()
    
    # 空のDataFrame作成
    df = pd.DataFrame()
    
    try:
      # Webサイトを開く
      driver.get("https://tenshoku.mynavi.jp/")
      time.sleep(5)
      
      '''
      ポップアップを閉じる
      ※余計なポップアップが操作の邪魔になる場合がある
        モーダルのようなポップアップ画面は、通常のclick操作では処理できない場合があるため
        excute_scriptで直接Javascriptを実行することで対処する
      '''
      driver.execute_script('document.querySelector(".karte-close").click()')
      time.sleep(5)
      # ポップアップを閉じる
      driver.execute_script('document.querySelector(".karte-close").click()')

      '''
      find_elementでHTML要素(WebElement)を取得する
      byで、要素を特定する属性を指定するBy.CLASS_NAMEの他、By.NAME、By.ID、By.CSS_SELECTORなどがある
      特定した要素に対して、send_keysで入力、clickでクリック、textでデータ取得が可能
      '''
      
      driver.get(f"https://tenshoku.mynavi.jp/list/kw{search_keyword}")
      # 検索窓に入力
      #driver.find_element(by=By.CLASS_NAME, value="topSearch__text").send_keys(search_keyword)
      # 検索ボタンクリック
      #driver.find_element(by=By.CLASS_NAME, value="topSearch__button").click()

      while True:
        '''
        find_elements(※複数形)を使用すると複数のデータがListで取得できる
        一覧から同一条件で複数のデータを取得する場合は、こちらを使用する
        '''
        name_elms = driver.find_elements(by=By.CLASS_NAME, value="cassetteRecruit__name")
        title_elms = driver.find_elements(by=By.XPATH, value="//p[@class='cassetteRecruit__copy boxAdjust']/a" ) 
      
        # 1ページ分繰り返し
        # print(len(name_elms))
        '''
        name_elmsには１ページ分の情報が格納されているのでforでループさせて１つづつ取り出して、Dataframeに格納する
        '''
        for i in range(len(name_elms)):            
          # DataFrameに対して辞書形式でデータを追加する
          df = df.append(
            {"会社名": name_elms[i].text, 
            "タイトル": title_elms[i].text, 
            "項目C": ""}, 
            ignore_index=True
          )
        
        next_page_btns = driver.find_elements(by=By.CLASS_NAME, value='iconFont--arrowLeft')
        if len(next_page_btns) > 0:
          next_page_btn = driver.find_element(by=By.CLASS_NAME, value='iconFont--arrowLeft')
          next_page_btn.location_once_scrolled_into_view
          next_page_btn.click()
          time.sleep(5)
        else:
          print("最後のページです")
          driver.quit()
          break
        df.to_csv('mynavi.csv', index=True, encoding='utf-8_sig')
    except Exception as e:
      save_log(e)
      driver.quit()    

def save_log(e):
  with open('debug.log', 'a', encoding='utf-8_sig') as f:
    if os.path.getsize('debug.log') == 3:
      data = f'[0][{str(time.time())}][{str(e)}]\n'
      f.writelines(data)
    else:
      data = f'[{sum([1 for _ in open("debug.log")])}][{str(time.time())}][{str(e)}]\n'
      f.writelines(data)

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()