# Summary: This module contains the user interface and logic for a graphical user interface version of the stock manager program.

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import csv
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData

class StockApp:
    def __init__(self):
        self.stock_list = []
        #check for database, create if not exists
        if path.exists("stocks.db") == False:
            stock_data.create_database()
        else:
            # Load existing data from database on startup
            try:
                stock_data.load_stock_data(self.stock_list)
                sortStocks(self.stock_list)
            except Exception:
                # If load fails, continue with empty list
                pass

        # Create Window
        self.root = Tk()
        self.root.title("Stock Manager")
        self.root.geometry("900x600")

        # Add Menubar
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        # File Menu
        file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load", command=self.load)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Web Menu
        web_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Web", menu=web_menu)
        web_menu.add_command(label="Scrape Yahoo Finance", command=self.scrape_web_data)
        web_menu.add_command(label="Import CSV", command=self.importCSV_web_data)

        # Chart Menu
        chart_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Chart", menu=chart_menu)
        chart_menu.add_command(label="Display Chart", command=self.display_chart)

        # Add heading information
        heading_frame = Frame(self.root)
        heading_frame.pack(pady=10)
        self.headingLabel = Label(heading_frame, text="Stock Manager", font=("Arial", 14, "bold"))
        self.headingLabel.pack()

        # Main content frame
        content_frame = Frame(self.root)
        content_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Left panel: Stock list
        left_frame = Frame(content_frame)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True)

        Label(left_frame, text="Stocks:", font=("Arial", 10, "bold")).pack()
        self.stockList = Listbox(left_frame, height=15)
        self.stockList.pack(fill=BOTH, expand=True)
        self.stockList.bind("<<ListboxSelect>>", self.update_data)
        
        # Populate listbox with loaded stocks
        for stock in self.stock_list:
            self.stockList.insert(END, stock.symbol)

        # Right panel: Tabs for data entry and display
        right_frame = Frame(content_frame)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))

        # Tabs
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=BOTH, expand=True)

        # Main Tab
        self.main_tab = Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Main")
        
        Label(self.main_tab, text="Add New Stock", font=("Arial", 10, "bold")).pack(pady=5)
        
        Label(self.main_tab, text="Symbol:").pack()
        self.addSymbolEntry = Entry(self.main_tab, width=20)
        self.addSymbolEntry.pack()
        
        Label(self.main_tab, text="Name:").pack()
        self.addNameEntry = Entry(self.main_tab, width=20)
        self.addNameEntry.pack()
        
        Label(self.main_tab, text="Shares:").pack()
        self.addSharesEntry = Entry(self.main_tab, width=20)
        self.addSharesEntry.pack()
        
        Button(self.main_tab, text="Add Stock", command=self.add_stock).pack(pady=10)

        Label(self.main_tab, text="Update Shares", font=("Arial", 10, "bold")).pack(pady=5)
        
        Label(self.main_tab, text="Shares to Buy/Sell:").pack()
        self.updateSharesEntry = Entry(self.main_tab, width=20)
        self.updateSharesEntry.pack()
        
        button_frame = Frame(self.main_tab)
        button_frame.pack(pady=5)
        Button(button_frame, text="Buy", command=self.buy_shares).pack(side=LEFT, padx=5)
        Button(button_frame, text="Sell", command=self.sell_shares).pack(side=LEFT, padx=5)
        Button(button_frame, text="Delete Stock", command=self.delete_stock).pack(side=LEFT, padx=5)
        Button(button_frame, text="Add Daily Data", command=self.add_daily_data).pack(side=LEFT, padx=5)

        # History Tab
        self.history_tab = Frame(self.notebook)
        self.notebook.add(self.history_tab, text="History")
        
        Label(self.history_tab, text="Daily Stock Data", font=("Arial", 10, "bold")).pack(pady=5)
        self.dailyDataList = Text(self.history_tab, height=20, width=50)
        self.dailyDataList.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Report Tab
        self.report_tab = Frame(self.notebook)
        self.notebook.add(self.report_tab, text="Report")
        
        Label(self.report_tab, text="Stock Report", font=("Arial", 10, "bold")).pack(pady=5)
        self.stockReport = Text(self.report_tab, height=20, width=50)
        self.stockReport.pack(fill=BOTH, expand=True, padx=5, pady=5)

        ## Call MainLoop
        self.root.mainloop()
       
    # Load stocks and history from database.
    def load(self):
        self.stockList.delete(0,END)
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END,stock.symbol)
        messagebox.showinfo("Load Data","Data Loaded")

    # Save stocks and history to database.
    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data","Data Saved")

    # Refresh history and report tabs
    def update_data(self, evt):
        self.display_stock_data()

    # Display stock price and volume history.
    def display_stock_data(self):
        try:
            symbol = self.stockList.get(self.stockList.curselection())
        except Exception:
            # nothing selected
            return
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                self.dailyDataList.delete("1.0",END)
                self.stockReport.delete("1.0",END)
                self.dailyDataList.insert(END,"- Date -   - Price -   - Volume -\n")
                self.dailyDataList.insert(END,"=================================\n")
                for daily_data in stock.DataList:
                    # show trading date and the entry timestamp
                    trade_date = daily_data.date.strftime("%m/%d/%y")
                    entered = ''
                    if getattr(daily_data, 'entered', None):
                        try:
                            entered = daily_data.entered.strftime("%m/%d/%y %H:%M:%S")
                        except Exception:
                            entered = str(daily_data.entered)
                    row = f"{trade_date}   ${daily_data.close:0,.2f}   {daily_data.volume}   (entered: {entered})\n"
                    self.dailyDataList.insert(END, row)

                # Display report
                if stock.DataList:
                    prices = [d.close for d in stock.DataList]
                    volumes = [d.volume for d in stock.DataList]
                    avg_price = sum(prices) / len(prices)
                    min_price = min(prices)
                    max_price = max(prices)
                    total_volume = sum(volumes)
                    self.stockReport.insert(END, f"Symbol: {stock.symbol}\n")
                    self.stockReport.insert(END, f"Name: {stock.name}\n")
                    self.stockReport.insert(END, f"Shares: {stock.shares}\n")
                    # show last entry timestamp if available
                    last_entered = ''
                    try:
                        last_entered = stock.DataList[-1].entered.strftime("%m/%d/%y %H:%M:%S")
                    except Exception:
                        last_entered = ''
                    if last_entered:
                        self.stockReport.insert(END, f"Last Entry: {last_entered}\n")
                    self.stockReport.insert(END, f"\nPrice Statistics:\n")
                    self.stockReport.insert(END, f"Average Price: ${avg_price:0.2f}\n")
                    self.stockReport.insert(END, f"Min Price: ${min_price:0.2f}\n")
                    self.stockReport.insert(END, f"Max Price: ${max_price:0.2f}\n")
                    self.stockReport.insert(END, f"Total Volume: {total_volume:0.0f}\n")
                else:
                    self.stockReport.insert(END, f"Symbol: {stock.symbol}\n")
                    self.stockReport.insert(END, f"Name: {stock.name}\n")
                    self.stockReport.insert(END, f"Shares: {stock.shares}\n")
                    self.stockReport.insert(END, f"\nNo data available\n")


                    

    
    # Add new stock to track.
    def add_stock(self):
        try:
            shares_val = float(str(self.addSharesEntry.get()))
        except Exception:
            messagebox.showerror("Invalid Input","Shares must be a number")
            return
        symbol = self.addSymbolEntry.get().strip().upper()
        name = self.addNameEntry.get().strip()
        if not symbol:
            messagebox.showerror("Invalid Input","Symbol is required")
            return
        new_stock = Stock(symbol, name, shares_val)
        self.stock_list.append(new_stock)
        idx = self.stockList.size()
        self.stockList.insert(END, symbol)
        # clear entries
        self.addSymbolEntry.delete(0,END)
        self.addNameEntry.delete(0,END)
        self.addSharesEntry.delete(0,END)
        # select the newly added stock and refresh display
        self.stockList.selection_clear(0, END)
        self.stockList.selection_set(idx)
        self.stockList.activate(idx)
        self.display_stock_data()

    # Buy shares of stock.
    def buy_shares(self):
        try:
            symbol = self.stockList.get(self.stockList.curselection())
        except Exception:
            messagebox.showwarning("Buy Shares","No stock selected")
            return
        try:
            qty = float(self.updateSharesEntry.get())
        except Exception:
            messagebox.showerror("Invalid Input","Shares must be a number")
            return
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(qty)
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                break
        messagebox.showinfo("Buy Shares","Shares Purchased")
        self.updateSharesEntry.delete(0,END)
        self.display_stock_data()

    # Sell shares of stock.
    def sell_shares(self):
        try:
            symbol = self.stockList.get(self.stockList.curselection())
        except Exception:
            messagebox.showwarning("Sell Shares","No stock selected")
            return
        try:
            qty = float(self.updateSharesEntry.get())
        except Exception:
            messagebox.showerror("Invalid Input","Shares must be a number")
            return
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.sell(qty)
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                break
        messagebox.showinfo("Sell Shares","Shares Sold")
        self.updateSharesEntry.delete(0,END)
        self.display_stock_data()

    # Remove stock and all history from being tracked.
    def delete_stock(self):
       try:
           symbol = self.stockList.get(self.stockList.curselection())
       except Exception:
           messagebox.showwarning("Delete Stock","No stock selected")
           return
       for i,stock in enumerate(self.stock_list):
           if stock.symbol == symbol:
               del self.stock_list[i]
               self.stockList.delete(i)
               self.dailyDataList.delete("1.0",END)
               self.stockReport.delete("1.0",END)
               self.headingLabel['text'] = ""
               messagebox.showinfo("Delete Stock","Stock deleted")
               # after deletion, select next item if available
               size = self.stockList.size()
               if size > 0:
                   sel = i if i < size else size-1
                   self.stockList.selection_set(sel)
                   self.stockList.activate(sel)
                   self.display_stock_data()
               return
       messagebox.showwarning("Delete Stock","Stock not found")

    # Get data from web scraping.
    def scrape_web_data(self):
        try:
            symbol = self.stockList.get(self.stockList.curselection())
        except Exception:
            messagebox.showwarning("Web Scrape","No stock selected")
            return
        dateFrom = simpledialog.askstring("Starting Date","Enter Starting Date (m/d/yy)")
        dateTo = simpledialog.askstring("Ending Date","Enter Ending Date (m/d/yy)")
        if not dateFrom or not dateTo:
            return
        try:
            stock_data.retrieve_stock_web(dateFrom,dateTo,self.stock_list)
        except Exception as e:
            messagebox.showerror("Cannot Get Data from Web","Error: " + str(e))
            return
        self.display_stock_data()
        messagebox.showinfo("Get Data From Web","Data Retrieved")

    # Import CSV stock history file.
    def importCSV_web_data(self):
        try:
            symbol = self.stockList.get(self.stockList.curselection())
        except Exception:
            messagebox.showwarning("Import CSV","No stock selected")
            return
        filename = filedialog.askopenfilename(title="Select " + symbol + " File to Import",filetypes=[('Yahoo Finance! CSV','*.csv')])
        if filename != "":
            try:
                stock_data.import_stock_web_csv(self.stock_list,symbol,filename)
                self.display_stock_data()
                messagebox.showinfo("Import Complete",symbol + " Import Complete")
            except Exception as e:
                messagebox.showerror("Import Error","Error importing CSV: " + str(e))   
    
    # Display stock price chart.
    def display_chart(self):
        try:
            symbol = self.stockList.get(self.stockList.curselection())
        except Exception:
            messagebox.showwarning("Display Chart","No stock selected")
            return
        try:
            display_stock_chart(self.stock_list,symbol)
        except Exception as e:
            messagebox.showerror("Chart Error","Error displaying chart: " + str(e))

    # Add a daily data point for the selected stock using simple dialogs
    def add_daily_data(self):
        try:
            symbol = self.stockList.get(self.stockList.curselection())
        except Exception:
            messagebox.showwarning("Add Daily Data","No stock selected")
            return
        date_str = simpledialog.askstring("Date","Enter date (m/d/yy)")
        if not date_str:
            return
        try:
            date = datetime.strptime(date_str, "%m/%d/%y")
        except Exception:
            messagebox.showerror("Invalid Date","Date must be in m/d/yy format")
            return
        try:
            price = float(simpledialog.askstring("Price","Enter closing price"))
            volume = float(simpledialog.askstring("Volume","Enter volume"))
        except Exception:
            messagebox.showerror("Invalid Input","Price and Volume must be numbers")
            return
        # find stock and append data
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.add_data(DailyData(date, price, volume))
                # ensure data sorted
                sortDailyData(self.stock_list)
                self.display_stock_data()
                messagebox.showinfo("Add Daily Data","Daily data added")
                return


def main():
        app = StockApp()
        

if __name__ == "__main__":
    # execute only if run as a script
    main()