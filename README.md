# 股票K线图可视化工具 / Stock K-line Chart Visualization Tool

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)](https://www.microsoft.com/windows)

[English](#english) | [中文](#中文)

</div>

---
## ✨ 共创者
- [@Yize]([https://github.com/zhangsan](https://github.com/tuyize0))
- [@Yuhang]([https://github.com/lisi](https://github.com/yetsoclose260))

## 中文

### 项目介绍

这是一个基于Python开发的股票K线图可视化工具，使用matplotlib、pandas和tkinter库构建。该工具支持查看多只股票的K线图，包括BYDDY、LI、NIO、TSLA、XIACY和XPEV，并提供多种技术指标显示功能，如移动平均线（MA）、布林带、MACD、RSI和KDJ，同时支持缩放和平移等交互操作。

### 功能特性

- **🏢 多股票支持**: 用户可以切换不同股票查看其对应的K线图
- **📊 技术指标**: 显示多种技术指标，包括MA5、MA10、MA20、MA60、布林带、MACD、RSI和KDJ
- **🖱️ 交互操作**: 支持图表的缩放和平移，方便用户查看不同尺度的细节
- **💡 鼠标悬停**: 鼠标悬停在图表特定日期时，显示相应的日期、开盘价、收盘价、最高价、最低价和成交量信息

### 系统要求

- Python 3.9 或更高版本
- 必要的库：pandas、matplotlib、mplfinance、tkinter、Pillow

### 安装依赖

```bash
pip install pandas matplotlib mplfinance pillow
```

### 使用方法

1. **准备数据**: 将股票数据CSV文件放置在脚本同一目录下，文件名应与脚本中data_files字典的键对应

2. **运行脚本**: 在终端中执行Python脚本：
   ```bash
   python main5.py
   ```

3. **界面交互**:
   - **股票选择**: 点击顶部的股票按钮切换不同股票
   - **指标选择**: 点击指标按钮显示不同的技术指标
   - **缩放和平移**: 使用鼠标滚轮进行缩放，按住鼠标左键进行平移
   - **鼠标悬停**: 将鼠标移动到图表上查看特定日期的详细信息

### 文件结构

```
TradingViewer_DesignedByGroup8/
├── stock_data/
│   ├── BYDDY_2020-2025_Day.csv
│   ├── LI_2020-2025_Day.csv
│   ├── NIO_2020-2025_Day.csv
│   ├── TSLA_2020-2025_Day.csv
│   ├── XIACY_2020-2025_Day.csv
│   └── XPEV_2020-2025_Day.csv
├── image/
│   └── head_image.jpg
├── main5.py
└── README.md
```

### 主要功能函数

- **数据加载**: `load_data(file_name)` - 读取和处理股票数据文件
- **技术指标计算**:
  - `calculate_macd(data)`: 计算MACD指标
  - `calculate_bollinger_bands(data)`: 计算布林带指标
  - `calculate_rsi(data, period=14)`: 计算RSI指标
  - `calculate_kdj(data, period=9)`: 计算KDJ指标
- **用户交互功能**:
  - `select_ma(ma)`: 处理移动平均线按钮点击事件
  - `toggle_bollinger()`: 处理布林带按钮点击事件
  - `select_indicator(indicator)`: 处理指标按钮点击事件

### 注意事项

- 确保CSV文件存在且文件路径正确
- 脚本使用matplotlib库进行图表绘制，tkinter库进行图形界面构建，请确保这些库正确安装
- 程序为Group 8团队设计开发

### 许可证

本项目为开源项目，您可以自由使用、修改和分发。

---

## English

### Project Introduction

This is a stock K-line chart visualization tool developed in Python using matplotlib, pandas, and tkinter libraries. It allows users to view K-line charts of multiple stocks including BYDDY, LI, NIO, TSLA, XIACY, and XPEV. The tool supports various technical indicators such as Moving Averages (MA), Bollinger Bands, MACD, RSI, and KDJ, and provides interactive features like zooming and panning.

### Features

- **🏢 Multi-stock Support**: Users can switch between different stocks to view their respective K-line charts
- **📊 Technical Indicators**: Displays multiple technical indicators including MA5, MA10, MA20, MA60, Bollinger Bands, MACD, RSI, and KDJ
- **🖱️ Interactive Operations**: Supports zooming and panning on charts for viewing details at different scales
- **💡 Mouse Interaction**: Displays corresponding date, opening price, closing price, high price, low price, and trading volume information when hovering over specific dates

### Prerequisites

- Python 3.9 or higher
- Required libraries: pandas, matplotlib, mplfinance, tkinter, Pillow

### Installation

```bash
pip install pandas matplotlib mplfinance pillow
```

### Usage

1. **Prepare Data**: Place stock data CSV files in the same directory as the script. File names should match the keys in the data_files dictionary in the script

2. **Run the Script**: Execute the Python script in terminal:
   ```bash
   python main5.py
   ```

3. **Interface Interaction**:
   - **Stock Selection**: Click stock buttons at the top to switch between different stocks
   - **Indicator Selection**: Click indicator buttons to display different technical indicators
   - **Zooming and Panning**: Use mouse scroll wheel to zoom, hold left mouse button to pan
   - **Mouse Hover**: Move mouse over chart to view detailed information for specific dates

### File Structure

```
TradingViewer_DesignedByGroup8/
├── stock_data/
│   ├── BYDDY_2020-2025_Day.csv
│   ├── LI_2020-2025_Day.csv
│   ├── NIO_2020-2025_Day.csv
│   ├── TSLA_2020-2025_Day.csv
│   ├── XIACY_2020-2025_Day.csv
│   └── XPEV_2020-2025_Day.csv
├── image/
│   └── head_image.jpg
├── main5.py
└── README.md
```

### Main Functions

- **Data Loading**: `load_data(file_name)` - Reads and processes stock data files
- **Technical Indicator Calculation**:
  - `calculate_macd(data)`: Calculates MACD indicator
  - `calculate_bollinger_bands(data)`: Calculates Bollinger Bands indicator
  - `calculate_rsi(data, period=14)`: Calculates RSI indicator
  - `calculate_kdj(data, period=9)`: Calculates KDJ indicator
- **User Interaction**:
  - `select_ma(ma)`: Handles moving average button click events
  - `toggle_bollinger()`: Handles Bollinger Bands button click events
  - `select_indicator(indicator)`: Handles indicator button click events

### Notes

- Ensure CSV files exist and file paths are correct
- The script uses matplotlib for chart drawing and tkinter for GUI. Make sure these libraries are installed correctly
- Program designed and developed by Group 8

### License

This project is open-source. You can freely use, modify, and distribute it.

---

<div align="center">

**Designed by Group 8** 

*Advanced Topics in Electrical and Electronic Engineering - ELEC7078*

</div> 
