# DATA_200_lab_2
Stock tracking application - both  console and GUI (Graphical User Interfaces)

# DATA 200 – Lab 2: Stock Analyzer

## 🔎 Overview  
This project implements a stock-analysis tool for the course DATA 200 (Lab 2). It allows users to maintain a portfolio of stocks, retrieve historical price data (via web-scraping or CSV import), and view price history — either through a console interface or via a simple GUI.  

## 📂 Project Structure  
Here are the key files and their purposes:

| File | Description |
|------|-------------|
| `stock_class.py` | Defines core classes: `Stock`, `DailyData` (to model stock info and daily price data). |  
| `stocks.py` | Entry point / helper to launch the console application. |  
| `stock_console.py` | Console-based interface: menu, user input, portfolio management, data import/retrieval, reports. |  
| `stock_data.py` | Core data logic: scrape data from the web (using Selenium + BeautifulSoup), parse CSVs, store and manage historical data. |  
| `utilities.py` | Utility functions (e.g. clear screen, sorting, chart display helpers). |  
| (Optional) `chromedriver` / config files | Support files for web scraping using Selenium (if applicable). |  
| Sample data (e.g. `aapl_data.csv`) | Example CSV to test CSV-import functionality (if provided). |  

## 🚀 Getting Started / Installation  

### Prerequisites  
- Python 3.x  
- (For web scraping) A compatible Chrome browser + matching `chromedriver` (if you want scraping to work)  
- Python packages:  
  ```bash
  pip install selenium beautifulsoup4 pandas matplotlib

Running the Program

From the project root folder in terminal:

To use via console:

python stock_console.py


or

python stocks.py


(If GUI version implemented) Launch via the GUI script.

🛠️ Features / What It Does

Maintain a list of stocks in a portfolio: add, update, delete.

Retrieve historical daily price data for your stocks via two methods:

Web scraping from Yahoo! Finance (live download through browser automation)

Import from a pre-downloaded CSV file from Yahoo! Finance

Store historical data (date, open/high/low/close price, adj-close, volume) in structured objects.

Generate simple reports, show data history, and (optionally) visualize price history / charts.

Support both console-based interface (text-menu) and GUI (if applicable).

✅ What Works / What to Know

Web scraping: If using Selenium, ensure chromedriver is present and matches your Chrome version.

CSV import: Works with properly formatted CSV files downloaded from Yahoo! Finance (i.e. standard headers).

Data structures: Historical data for each stock is stored in DailyData objects associated with a Stock.

📝 Limitations or To-Do / Known Issues

The GUI version may not support all console features (or vice versa), depending on implementation.

Error handling for malformed CSVs or missing data may be basic.

Data storage is in memory (or simple file), not a database — so data does not persist across sessions unless explicitly saved/exported.

Web scraping depends on page layout — if Yahoo! Finance changes its format, scraping may break.

