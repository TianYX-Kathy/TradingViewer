Stock K-line Chart Visualization Tool
Introduction
This Python script is a stock K-line chart visualization tool built using the matplotlib, pandas, and tkinter libraries. It allows users to view the K-line charts of multiple stocks, including BYDDY, LI, NIO, TSLA, XIACY, and XPEV. Additionally, it supports the display of various technical indicators such as Moving Averages (MA), Bollinger Bands, MACD, RSI, and KDJ, and provides interactive functions like zooming and panning.
Features
1. Multi-stock Support: Users can switch between different stocks to view their respective K-line charts.
2. Technical Indicators: Displays multiple technical indicators, including MA5, MA10, MA20, MA60, Bollinger Bands, MACD, RSI, and KDJ.
3. Interactive Operations: Supports zooming and panning on the chart, allowing users to view details at different scales.
4. Mouse Interaction: When the mouse hovers over a specific date on the chart, it displays the corresponding date, opening price, closing price, high price, low price, and trading volume information.
Prerequisites
Python 3.9 or higher
Required libraries: pandas, matplotlib, mplfinance, tkinter,Pillow
You can install the required libraries using the following command:
bash
pip install pandas matplotlib mplfinance
Usage
1. Prepare Data: Place the stock data CSV files in the same directory as the script. The file names should match the keys in the data_files dictionary in the script.
2. Run the Script: Execute the Python script in the terminal:
bash
main5.py
3. Interact with the Interface:
Stock Selection: Click the stock buttons at the top to switch between different stocks.
Indicator Selection: Click the indicator buttons to display different technical indicators.
Zooming and Panning: Use the mouse scroll wheel to zoom in and out, and hold the left mouse button to pan the chart.
Mouse Hover: Move the mouse over the chart to view the detailed information of a specific date.
File Structure
TradingViewer_DesignedByGroup8/
├── stock_data/
│ ├── BYDDY_2020-2025_Day.csv
│ ├── LI_2020-2025_Day.csv
│ ├── NIO_2020-2025_Day.csv
│ ├── TSLA_2020-2025_Day.csv
│ ├── XIACY_2020-2025_Day.csv
│ └── XPEV_2020-2025_Day.csv
├── image/
└── head_image.jpg
└── main5.py/
Code Structure
Data Loading and Processing: The load_data function is responsible for reading the CSV files and calculating various technical indicators.
Chart Drawing: The matplotlib library is used to draw the K-line chart and technical indicator charts.
Interactive Functions: The tkinter library is used to create the graphical user interface, and event handlers are used to implement interactive operations such as zooming, panning, and mouse hover.
Main Functions
Data Loading: load_data(file_name) is used to read and process stock data files.
Technical Indicator Calculation:
calculate_macd(data): Calculates the MACD indicator.
calculate_bollinger_bands(data): Calculates the Bollinger Bands indicator.
calculate_rsi(data, period=14): Calculates the RSI indicator.
calculate_kdj(data, period=9): Calculates the KDJ indicator.
User Interaction:
select_ma(ma): Handles the click event of the moving average button.
toggle_bollinger(): Handles the click event of the Bollinger Bands button.
select_indicator(indicator): Handles the click event of the indicator button.
update_stock_display(stock_name, price, change, change_ratio, color, chosen_stock_panel): Updates the display information of the selected stock.
show_stock_details(stock): Displays detailed information about the selected stock.
show_under_development(): Displays a pop-up window indicating that the feature is under development.
show_under_development_panel(): Displays a panel indicating that the feature is under development.
show_stock_list_panel(): Displays the stock list panel.
Notes
Ensure that the CSV files exist and the file paths are correct.
The script uses the matplotlib library for chart drawing, and the tkinter library for the graphical user interface. Make sure these libraries are installed correctly.
License
This project is open-source. You can freely use, modify, and distribute it.