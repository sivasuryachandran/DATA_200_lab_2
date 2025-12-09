# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart
from os import path
import stock_data


# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")

# Manage Stocks
def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")

# Add new stock to track
def add_stock(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Add Stock ---")
        symbol = input("Enter Stock Symbol (or 0 to cancel): ")
        if symbol == "0":
            return
        name = input("Enter Company Name: ")
        try:
            shares = float(input("Enter number of shares: "))
        except:
            print("Invalid shares value. Cancelling.")
            return
        new_stock = Stock(symbol.upper(), name, shares)
        stock_list.append(new_stock)
        print(f"Added {symbol}.")
        input("Press Enter to continue...")
        return
        
# Buy or Sell Shares Menu
def update_shares(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Update Shares ---")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Return")
        option = input("Enter Option: ")
        if option == "1":
            buy_stock(stock_list)
        elif option == "2":
            sell_stock(stock_list)
        elif option == "0":
            return
        else:
            print("Invalid option")
            input("Press Enter to continue...")


# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---")
    print("Stock List: [",end="")
    print(','.join([s.symbol for s in stock_list]) + "]")
    symbol = input("Enter symbol to buy (or 0 to cancel): ").upper()
    if symbol == "0":
        return
    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            try:
                qty = float(input("Enter shares to buy: "))
            except:
                print("Invalid share amount")
                input("Enter to continue...")
                return
            stock.buy(qty)
            print(f"Bought {qty} shares of {symbol}.")
            found = True
            break
    if not found:
        print("Symbol not found")
    input("Press Enter to continue...")

# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    print("Sell Shares ---")
    print("Stock List: [",end="")
    print(','.join([s.symbol for s in stock_list]) + "]")
    symbol = input("Enter symbol to sell (or 0 to cancel): ").upper()
    if symbol == "0":
        return
    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            try:
                qty = float(input("Enter shares to sell: "))
            except:
                print("Invalid share amount")
                input("Enter to continue...")
                return
            stock.sell(qty)
            print(f"Sold {qty} shares of {symbol}.")
            found = True
            break
    if not found:
        print("Symbol not found")
    input("Press Enter to continue...")

# Remove stock and all daily data
def delete_stock(stock_list):
    clear_screen()
    print("Delete Stock ---")
    symbol = input("Enter symbol to delete (or 0 to cancel): ").upper()
    if symbol == "0":
        return
    for i,stock in enumerate(stock_list):
        if stock.symbol == symbol:
            del stock_list[i]
            print(f"Deleted {symbol}.")
            input("Press Enter to continue...")
            return
    print("Symbol not found")
    input("Press Enter to continue...")


# List stocks being tracked
def list_stocks(stock_list):
    clear_screen()
    print("Tracked Stocks ---")
    if not stock_list:
        print("No stocks currently tracked.")
    for stock in stock_list:
        print(f"{stock.symbol} - {stock.name} - {stock.shares} shares")
    input("Press Enter to continue...")

# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    print("Add Daily Stock Data ---")
    symbol = input("Enter symbol (or 0 to cancel): ").upper()
    if symbol == "0":
        return
    target = None
    for stock in stock_list:
        if stock.symbol == symbol:
            target = stock
            break
    if target is None:
        print("Symbol not found")
        input("Press Enter to continue...")
        return
    date_str = input("Enter Date (m/d/yy): ")
    try:
        date = datetime.strptime(date_str, "%m/%d/%y")
    except:
        print("Invalid date format")
        input("Press Enter to continue...")
        return
    try:
        price = float(input("Enter closing price: "))
        volume = float(input("Enter volume: "))
    except:
        print("Invalid numeric input")
        input("Press Enter to continue...")
        return
    daily = DailyData(date, price, volume)
    target.add_data(daily)
    print("Daily data added.")
    input("Press Enter to continue...")

# Display Report for All Stocks
def display_report(stock_data):
    clear_screen()
    print("Stock Report ---")
    for stock in stock_data:
        print(f"{stock.symbol} - {stock.name} - {stock.shares} shares - {len(stock.DataList)} data points")
        # Optionally show most recent price
        if stock.DataList:
            last = stock.DataList[-1]
            print(f"   Last: {last.date.strftime('%m/%d/%y')} - ${last.close:0.2f} - Vol: {last.volume}")
    input("Press Enter to continue...")


  


# Display Chart
def display_chart(stock_list):
    print("Stock List: [",end="")
    for stock in stock_list:
        print(stock.symbol + ",",end="")
    print("]")
    symbol = input("Enter symbol to chart (or 0 to cancel): ").upper()
    if symbol == "0":
        return
    display_stock_chart(stock_list,symbol)
    input("Press Enter to continue...")

# Manage Data Menu
def manage_data(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Data ---")
        print("1 - Save Data")
        print("2 - Load Data")
        print("3 - Retrieve From Web")
        print("4 - Import CSV")
        print("0 - Return")
        option = input("Enter Option: ")
        if option == "1":
            stock_data.save_stock_data(stock_list)
            print("Data saved.")
            input("Press Enter to continue...")
        elif option == "2":
            stock_data.load_stock_data(stock_list)
            print("Data loaded.")
            input("Press Enter to continue...")
        elif option == "3":
            retrieve_from_web(stock_list)
        elif option == "4":
            import_csv(stock_list)
        elif option == "0":
            return
        else:
            print("Invalid option")
            input("Press Enter to continue...")


# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    print("Retrieve From Web ---")
    dateFrom = input("Enter start date (m/d/yy): ")
    dateTo = input("Enter end date (m/d/yy): ")
    try:
        count = stock_data.retrieve_stock_web(dateFrom, dateTo, stock_list)
        print(f"Retrieved {count} records.")
    except Exception as e:
        print("Error retrieving data:", e)
    input("Press Enter to continue...")

# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    print("Import CSV ---")
    symbol = input("Enter symbol to import for (or 0 to cancel): ").upper()
    if symbol == "0":
        return
    filename = input("Enter CSV filename (path): ")
    if not filename:
        return
    try:
        stock_data.import_stock_web_csv(stock_list, symbol, filename)
        print("Import complete.")
    except Exception as e:
        print("Import failed:", e)
    input("Press Enter to continue...")

# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()