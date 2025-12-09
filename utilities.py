#Helper Functions

from os import system, name

# Function to Clear the Screen
def clear_screen():
    if name == "nt": # User is running Windows
        _ = system('cls')
    else: # User is running Linux or Mac
        _ = system('clear')

# Function to sort the stock list (alphabetical)
def sortStocks(stock_list):
    ## Sort the stock list
    try:
        stock_list.sort(key=lambda s: s.symbol.upper())
    except Exception:
        # If objects are simple dicts or tuples, attempt a fallback
        try:
            stock_list.sort(key=lambda s: s[0])
        except Exception:
            return


# Function to sort the daily stock data (oldest to newest) for all stocks
def sortDailyData(stock_list):
    # Ensure each stock's DataList is sorted from oldest to newest by date
    for stock in stock_list:
        try:
            stock.DataList.sort(key=lambda d: d.date)
        except Exception:
            # If DataList contains raw tuples, attempt to sort by first element
            try:
                stock.DataList.sort(key=lambda d: d[0])
            except Exception:
                continue

# Function to create stock chart
def display_stock_chart(stock_list,symbol):
    # Find the stock
    target = None
    for stock in stock_list:
        if stock.symbol == symbol:
            target = stock
            break
    if target is None:
        print("Stock not found: ", symbol)
        return

    if not target.DataList:
        print("No data to display for:", symbol)
        return

    dates = [d.date for d in target.DataList]
    prices = [d.close for d in target.DataList]
    # import matplotlib only when charting to avoid heavy imports at module import time
    try:
        import matplotlib.pyplot as plt
    except Exception as e:
        print("Plotting unavailable (matplotlib not installed or import failed):", e)
        return

    plt.figure(figsize=(8,4))
    plt.plot(dates, prices, marker='o')
    plt.title(f"{target.symbol} - {target.name}")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    plt.tight_layout()
    plt.show()