import schedule
import time
from disney_line_bot import job  # 替換為您的實際模組和函數

def main():
  # 設定每週五晚上8點執行任務
  # schedule.every().friday.at("20:00").do(job)

  # print("排程已啟動，任務每週五晚上 8 點執行。")

  # # 持續檢查是否有排程任務需執行
  # while True:
  #     schedule.run_pending()
  #     time.sleep(1)
  job()
  print("任務執行完畢。")

if __name__ == "__main__":
    main()