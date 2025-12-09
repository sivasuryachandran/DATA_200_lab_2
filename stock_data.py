import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import csv
import time
from datetime import datetime
from utilities import clear_screen
from utilities import sortDailyData
from stock_class import Stock, DailyData

def create_database():
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    cur = conn.cursor()
    createStockTableCmd = """CREATE TABLE IF NOT EXISTS stocks (
                            symbol TEXT NOT NULL PRIMARY KEY,
                            name TEXT,
                            shares REAL
                        );"""
    createDailyDataTableCmd = """CREATE TABLE IF NOT EXISTS dailyData (
                                symbol TEXT NOT NULL,
                                date TEXT NOT NULL,
                                price REAL NOT NULL,
                                volume REAL NOT NULL,
                                PRIMARY KEY (symbol, date)
                        );"""   
    cur.execute(createStockTableCmd)
    cur.execute(createDailyDataTableCmd)

def save_stock_data(stock_list):
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    cur = conn.cursor()
    insertStockCmd = """INSERT INTO stocks
                            (symbol, name, shares)
                            VALUES
                            (?, ?, ?); """
    insertDailyDataCmd = """INSERT INTO dailyData
                                    (symbol, date, price, volume)
                                    VALUES
                                    (?, ?, ?, ?);"""
    for stock in stock_list:
        insertValues = (stock.symbol, stock.name, stock.shares)
        try:
            cur.execute(insertStockCmd, insertValues)
            cur.execute("COMMIT;")
        except:
            pass
        for daily_data in stock.DataList: 
            insertValues = (stock.symbol,daily_data.date.strftime("%m/%d/%y"),daily_data.close,daily_data.volume)
            try:
                cur.execute(insertDailyDataCmd, insertValues)
                cur.execute("COMMIT;")
            except:
                pass
    
def load_stock_data(stock_list):
    stock_list.clear()
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    stockCur = conn.cursor()
    stockSelectCmd = """SELECT symbol, name, shares
                    FROM stocks; """
    stockCur.execute(stockSelectCmd)
    stockRows = stockCur.fetchall()
    for row in stockRows:
        new_stock = Stock(row[0],row[1],row[2])
        dailyDataCur = conn.cursor()
        dailyDataCmd = """SELECT date, price, volume
                        FROM dailyData
                        WHERE symbol=?; """
        selectValue = (new_stock.symbol)
        dailyDataCur.execute(dailyDataCmd,(selectValue,))
        dailyDataRows = dailyDataCur.fetchall()
        for dailyRow in dailyDataRows:
            daily_data = DailyData(datetime.strptime(dailyRow[0],"%m/%d/%y"),float(dailyRow[1]),float(dailyRow[2]))
            new_stock.add_data(daily_data)
        stock_list.append(new_stock)
    sortDailyData(stock_list)

def retrieve_stock_web(dateStart,dateEnd,stock_list):
    dateFrom = str(int(time.mktime(time.strptime(dateStart,"%m/%d/%y"))))
    dateTo   = str(int(time.mktime(time.strptime(dateEnd,"%m/%d/%y"))))
    recordCount = 0

    for stock in stock_list:
        stockSymbol = stock.symbol

        url = (
            "https://finance.yahoo.com/quote/" + stockSymbol +
            "/history?period1=" + dateFrom +
            "&period2=" + dateTo +
            "&interval=1d&filter=history&frequency=1d"
        )

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        options.add_experimental_option(
            "prefs",
            {'profile.managed_default_content_settings.javascript': 2}
        )

        try:
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(60)
            driver.get(url)
        except:
            raise RuntimeWarning("Chrome Driver Not Found")

        soup = BeautifulSoup(driver.page_source,"html.parser")
        dataRows = soup.find_all('tr')

        for row in dataRows:
            td = row.find_all('td')
            rowList = [i.text for i in td]
            columnCount = len(rowList)

            if columnCount == 7:
                daily_data = DailyData(
                    datetime.strptime(rowList[0],"%b %d, %Y"),
                    float(rowList[5].replace(',','')),
                    float(rowList[6].replace(',',''))
                )
                stock.add_data(daily_data)
                recordCount += 1

        driver.quit()

    return recordCount

def import_stock_web_csv(stock_list, symbol, filename):
    """
    Import historical data for a single stock from a CSV file in
    Nasdaq format:
    "Date","Open","High","Low","Close","Volume"
    "12/01/2025","233.22","238.97","226.8","229.53","202,984,970"
    """
    for stock in stock_list:
        if stock.symbol.upper() == symbol.upper():
            with open(filename, newline='') as stockdata:
                datareader = csv.reader(stockdata, delimiter=',')

                next(datareader)

                for row in datareader:
                    if len(row) < 6:
                        continue
                    raw_date = row[0].strip().strip('"')
                    date_val = None
                    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%m/%d/%y"):
                        try:
                            date_val = datetime.strptime(raw_date, fmt)
                            break
                        except Exception:
                            continue
                    if date_val is None:
                        # couldn't parse date
                        continue

                    raw_close = row[4].strip().strip('"')
                    if raw_close == '' or raw_close.lower() == 'null':
                        continue
                    try:
                        close_val = float(raw_close.replace(',', ''))
                    except Exception:
                        continue

                    raw_vol = row[5].strip().strip('"').replace(",", "")
                    try:
                        volume_val = float(raw_vol) if raw_vol != '' else 0.0
                    except Exception:
                        volume_val = 0.0

                    daily_data = DailyData(date_val, close_val, volume_val)
                    stock.add_data(daily_data)

def main():
    clear_screen()
    print("This module will handle data storage and retrieval.")

if __name__ == "__main__":
    main()