from turtle import width
import pandas as pd
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc
import tkinter as tk
from tkinter import ANCHOR, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.figure import Figure
from tkinter import messagebox
from PIL import Image, ImageTk

# Solve the problem of displaying negative signs
import matplotlib
matplotlib.use("TkAgg")
matplotlib.rcParams['axes.unicode_minus'] = False

# Create Tkinter window
root = tk.Tk()
root.geometry("1280x900")  # Set the window size
root.configure(bg="#272E3A")  # Darker background

# Global variable to track if the under development panel is being displayed
is_under_development = False

# Define all stock data files
data_files = {
    'BYD': r'stock_data\BYDDY_2020-2025_Day.csv',
    'Li Xiang': r'stock_data\LI_2020-2025_Day.csv',
    'Wei Lai': r'stock_data\NIO_2020-2025_Day.csv',
    'Tesla': r'stock_data\TSLA_2020-2025_Day.csv',
    'Xiao Mi': r'stock_data\XIACY_2020-2025_Day.csv',
    'Xiao Peng': r'stock_data\XPEV_2020-2025_Day.csv'
}

# Function to read and process data
def load_data(file_name):
    try:
        df = pd.read_csv(file_name, header=1)
        df = df[2:]
        df = df.reset_index(drop=True)
        df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
        df['Date'] = pd.to_datetime(df['Date'])
        df['Date'] = df['Date'].map(mdates.date2num)
        ohlc = df[['Date', 'Open', 'High', 'Low', 'Close']]
        df['MA5'] = df['Close'].rolling(window=5).mean()
        df['MA10'] = df['Close'].rolling(window=10).mean()
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA60'] = df['Close'].rolling(window=60).mean()
        df = calculate_macd(df)
        df = calculate_bollinger_bands(df)
        df = calculate_rsi(df)
        df = calculate_kdj(df)
        return df, ohlc
    except FileNotFoundError:
        print(f"FileNotFoundError ：{file_name}")
        return None, None
    except Exception as e:
        print(f"fileReadError：{str(e)}")
        return None, None

# Function to calculate MACD indicator
def calculate_macd(data):
    short_window = 12
    long_window = 26
    signal_window = 9
    data['ema_short'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['ema_long'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['macd'] = data['ema_short'] - data['ema_long']
    data['signal'] = data['macd'].ewm(span=signal_window, adjust=False).mean()
    data['histogram'] = data['macd'] - data['signal']
    return data

# Function to calculate Bollinger Bands indicator
def calculate_bollinger_bands(data):
    period = 20
    std_dev = 2
    data['MB'] = data['Close'].rolling(window=period).mean()
    data['STD'] = data['Close'].rolling(window=period).std()
    data['UB'] = data['MB'] + std_dev * data['STD']
    data['LB'] = data['MB'] - std_dev * data['STD']
    return data

# Function to calculate RSI indicator
def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    avg_gain = up.rolling(window=period).mean()
    avg_loss = down.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data

# Function to calculate KDJ indicator
def calculate_kdj(data, period=9):
    low_min = data['Low'].rolling(window=period).min()
    high_max = data['High'].rolling(window=period).max()
    data['RSV'] = (data['Close'] - low_min) / (high_max - low_min) * 100
    data['K'] = data['RSV'].ewm(span=3, adjust=False).mean()
    data['D'] = data['K'].ewm(span=3, adjust=False).mean()
    data['J'] = 3 * data['K'] - 2 * data['D']
    return data

# Function to handle indicator button clicks
def select_indicator(indicator):
    global selected_indicator
    selected_indicator = indicator
    update_chart()

def update_stock_display(stock_name, price, change, change_ratio, color, chosen_stock_panel):
    # Update the stock name label
    stock_name_label.config(text=stock_name)

    # Update the price label
    price_label.config(text=price, fg=color)

    # Update the change label
    change_label.config(text=change, fg=color)

    # Update the change rato label
    change_Ratio_label.config(text=change_ratio, fg=color)

# Function to show stock details
def show_stock_details(stock):

    change_str = stock[2]  # Get the change string
    change_value = float(change_str.replace("%", ""))  # Remove "%" and convert to float
    if change_value >= 0:
        color = "green"  # Change color with rise or drop of the stock
    else:
        color = "red"

    stock_name = stock[3]
    price = stock[1]
    change_ratio = stock[2]
    change = stock[4]

    # Update the stock details in the chosen_stock_label
    update_stock_display(stock_name, price, change, change_ratio, color, chosen_stock_panel)

    global current_stock, df, ohlc
    current_stock = stock[0]
    df, ohlc = load_data(data_files[current_stock])
    update_chart()

# Function to create a popup window
def show_under_development():
    popup = tk.Toplevel(root)
    popup.title("Warning")

    # Calculate the center position relative to the main window
    window_width = 400
    window_height = 150
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    x = root_x + (root_width / 2) - (window_width / 2)
    y = root_y + (root_height / 2) - (window_height / 2)
    popup.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')

    label = tk.Label(popup, text="This function is under development", font=("Arial", 10))
    label.pack(pady=20)

    close_button = tk.Button(popup, text="Exit", command=popup.destroy)
    close_button.pack(pady=10)

    # Make the popup modal (grab all events)
    popup.grab_set()
    popup.focus_set()  # Ensure the popup has focus

    # Function to blink the popup
    def blink(count=0):
        if count < 6:  # Blink 3 times (on/off)
            try:
                if count % 2 == 0:
                    popup.config(bg="red")  # Or any color you want to use for the blink
                else:
                    popup.config(bg="#F0F0F0")  # Restore original background - use default Tkinter background

                root.after(400, blink, count + 1)  # Blink every 200 ms

            except tk.TclError:
                pass  # The popup has been destroyed

    # Bind click event to the root window to trigger the blink
    def on_main_window_click(event):
        if popup.winfo_exists():  # Check if the popup still exists
            blink()

    root.bind("<Button-1>", on_main_window_click)

# "Please confirming the exit" pop up window
def confirm_exit():
    # Creating custom dialogues
    dialog = tk.Toplevel(root)
    dialog.title("Confirmation of exit")
    dialog.geometry("300x150")
    dialog.resizable(False, False)

    # Calculate the center position relative to the main window
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    x = root_x + (root_width / 2) - 150  # 150 is half of the dialog width
    y = root_y + (root_height / 2) - 75  # 75 is half of the dialog height
    dialog.geometry(f"+{int(x)}+{int(y)}")

    # Displaying alert messages
    label = tk.Label(dialog, text="Are you sure you want to exit the programme?", padx=20, pady=20)
    label.pack()

    def on_yes():
        root.destroy()
        dialog.destroy()

    def on_no():
        dialog.destroy()

    # Create Yes and No buttons
    button_frame = tk.Frame(dialog)
    button_frame.pack()
    yes_button = tk.Button(button_frame, text="Yes", command=on_yes)
    yes_button.pack(side=tk.LEFT, padx=10)
    no_button = tk.Button(button_frame, text="No", command=on_no)
    no_button.pack(side=tk.LEFT, padx=10)

    # Making Dialogs Modal
    dialog.grab_set()
    dialog.focus_set()
    dialog.wait_window()

# Initialize current stock data
current_stock = 'BYD'

# Global variables to track selected options
selected_ma = []  # Now a list to store multiple selected MAs
show_bollinger = tk.IntVar()  # Checkbox variable for Bollinger Bands
selected_indicator = "Volume"  # Default to "Volume"

# Load initial data
df, ohlc = load_data(data_files[current_stock])


# Upper Buttons
button_data = [
    ("Optional", 10, 130),  # (text, x, y)
    ("Market", 10, 190),
    ("Account", 10, 250),
    ("Finding", 10, 310),
    ("Message", 10, 770),
    ("Chat", 10, 830)
]

# Stocks Button Styling
stock_button_style = {
    "bg": "#111316",
    "fg": "white",
    "font": ("Arial", 13),
    "anchor": "nw",
    "relief": "flat",
    "bd": 0,
    "highlightthickness": 0,
    "width": 20,  # Width in text units
    "height": 10
}

# Currently selected button
selected_button = None

# Stock Information
stocks = [
    ("Li Xiang", "19.790", "-8.00%", "LI", "-1.650"),
    ("Xiao Peng", "16.420", "-7.44%", "XPEV", "-1.320"),
    ("Xiao Mi", "24.100", "+3.66%", "XIACY", "+0.460"),
    ("Wei Lai", "3.140", "-6.55%", "NIO", "-1.252"),
    ("Tesla", "221.860", "-4.90%", "TSLA", "-0.780"),
    ("BYD", "67.900", "+1.93%", "BYDDY", "+0.250"),
]

# 1. Top Panel
content_frame = tk.Frame(root, bg="#111316", width=1148, height=30)
content_frame.place(x=132, y=0)
content_label = tk.Label(content_frame, text="Self Selected Stock Data Analysis Dashboard", bg="#111316", fg="white", font=("Arial", 12))
content_label.place(x=0, y=0, width=1148, height=30)

# 2. Left Sidebar Frame
sidebar = tk.Frame(root, bg="#272E3A", width=130, height=900)
sidebar.place(x=0, y=0)

# 3. Stock List Frame
stock_list_frame = tk.Frame(root, bg="#111316", width=246, height=868)
stock_list_frame.place(x=132, y=32)

# Initialize global variables
buttons = {}  # Initialize the buttons dictionary

# Function display Label
stock_label = tk.Label(stock_list_frame, text="Optional", bg="#111316", fg="white", font=("Arial", 15, "bold"))
stock_label.place(x=1, y=10, width=120, height=30)

# Chosen display Label
stock_Ins = tk.Label(stock_list_frame, text="Symbol", bg="#111316", fg="white", font=("Arial", 10))
stock_Ins.place(x=8, y=140)
Price = tk.Label(stock_list_frame, text="Price", bg="#111316", fg="white", font=("Arial", 10))
Price.place(x=80, y=140)
Chg = tk.Label(stock_list_frame, text="Chg", bg="#111316", fg="white", font=("Arial", 10))
Chg.place(x=135, y=140)
Rate_of_Chg = tk.Label(stock_list_frame, text="%Chg", bg="#111316", fg="white", font=("Arial", 10))
Rate_of_Chg.place(x=184, y=140)

# Lines
Line= tk.Frame(stock_list_frame, bg="#272E3A")
Line.place(x=0, y=124,width=246, height=2)

Line_2= tk.Frame(stock_list_frame, bg="#272E3A")
Line_2.place(x=0, y=166,width=246, height=2)

# My Choice display
function_display = tk.Label(stock_list_frame, text="My choice", bg="#111316", fg="white", font=("Arial", 10))
function_display.place(x=8, y=95)

# 4. Chosen Stock Panel on the right
chosen_stock_panel = tk.Frame(root, bg="#111316", width=900, height=60)
chosen_stock_panel.place(x=380, y=32)

# 5. Chosen Index Panel on the right
chosen_index_panel = tk.Frame(root, bg="#111316", width=900, height=40)
chosen_index_panel.place(x=380, y=158)
interrupt = tk.Frame(chosen_index_panel, bg="#272E3A")
interrupt.place(x=570, y=0, width=2, height=40)

# 6. Instruction Pannel on the right
Ins_pannel = tk.Frame(root,bg="#111316", width=900, height=62)
Ins_pannel.place(x=380, y=94)
Ins_label = tk.Label(Ins_pannel, text="Main Chart", bg="#111316", fg="white", font=("Arial", 10))
Ins_label.place(x=15, y=35)
Ins_label_2 = tk.Label(Ins_pannel, text="Sub Chart", bg="#111316", fg="white", font=("Arial", 10))
Ins_label_2.place(x=580, y=35)
Ins_label_3 = tk.Label(Ins_pannel, text="Indicators", bg="#111316", fg="white", font=("Arial", 13))
Ins_label_3.place(x=17, y=4)


# Region 1: Stock Name Label
stock_name_label = tk.Label(chosen_stock_panel, text="BYDDY", bg="#141414", fg="white", font=("Arial", 17))
stock_name_label.place(x=8, y=7)  # Use place for stock name label

# Region 2: Price Label
price_label = tk.Label(chosen_stock_panel, text="67.900", bg="#141414", fg="green", font=("Arial", 14) )
price_label.place(x=138, y=10)

# Region 3: Change Label
change_label = tk.Label(chosen_stock_panel, text="+0.250", bg="#141414", fg="green", font=("Arial", 14))
change_label.place(x=238, y=10)

# Region 4: Change Ratio Label
change_Ratio_label = tk.Label(chosen_stock_panel, text="+1.90%", bg="#141414", fg="green", font=("Arial", 14))
change_Ratio_label.place(x=338, y=10)



# Keep track of stock buttons
stock_buttons = []

selected_frame = None

def on_frame_click(frame, stock):
    global selected_frame
    if selected_frame is not None:
        # Check if the selected_frame still exists
        if tk.Toplevel.winfo_exists(selected_frame):
            selected_frame.config(relief="flat", bd=0, highlightbackground=selected_frame.original_bg, highlightthickness=0)
        else:
            selected_frame = None  # Reset selected_frame if it doesn't exist

    frame.config(relief="solid", bd=1, highlightbackground="#FCCA00", highlightthickness=1)
    selected_frame = frame
    show_stock_details(stock)

selected_button = None

def on_button_click(button):
    global selected_button

    # Restore the previous button's appearance
    if selected_button is not None:
        selected_button.config(bg=selected_button.original_bg, relief="flat", bd=1, highlightthickness=0)

    # Apply the "selected" effect to the clicked button
    button.config(bg="#4A4D4C", relief="sunken", bd=1, highlightthickness=0)  # Change background to gray and add sunken effect
    selected_button = button

def show_under_development_panel():
    global is_under_development
    is_under_development = True  # Set the state to indicate the panel is shown

    # Clear the stock list frame
    for widget in stock_list_frame.winfo_children():
        widget.destroy()

    # Create a new label in the original location
    under_dev_label = tk.Label(stock_list_frame, text="Under development", bg="#111316", fg="white", font=("Arial", 12, "bold"))
    under_dev_label.place(x=45, y=418, width=150, height=30)  # Center the label in the frame

def show_stock_list_panel():
    global is_under_development
    is_under_development = False  # Reset the state

    # Clear the stock list frame
    for widget in stock_list_frame.winfo_children():
        widget.destroy()

    stock_label = tk.Label(stock_list_frame, text="Optional", bg="#111316", fg="white", font=("Arial", 15, "bold"))
    stock_label.place(x=1, y=10, width=120, height=30)

    # My Choice display
    function_display = tk.Label(stock_list_frame, text="My choice", bg="#111316", fg="white", font=("Arial", 10))
    function_display.place(x=8, y=95)

    stock_y_offset = 170

    # Recreate the stock buttons
    for stock in stocks:
        change_str_s = stock[2]  # Get the change string
        change_value_k = float(change_str_s.replace("%", ""))  # Remove "%" and convert to float
        if change_value_k >= 0:
            color = "green"  # Change color with rise or drop of the stock
        else:
            color = "red"

        # Create a Frame to act like a button
        button_frame = tk.Frame(stock_list_frame, bg="#111316", width=232, height=70)
        button_frame.place(x=8, y=stock_y_offset)

        # Chosen display Label
        stock_Ins = tk.Label(stock_list_frame, text="Symbol", bg="#111316", fg="white", font=("Arial", 10))
        stock_Ins.place(x=8, y=140)
        Price = tk.Label(stock_list_frame, text="Price", bg="#111316", fg="white", font=("Arial", 10))
        Price.place(x=80, y=140)
        Chg = tk.Label(stock_list_frame, text="Chg", bg="#111316", fg="white", font=("Arial", 10))
        Chg.place(x=135, y=140)
        Rate_of_Chg = tk.Label(stock_list_frame, text="%Chg", bg="#111316", fg="white", font=("Arial", 10))
        Rate_of_Chg.place(x=184, y=140)

        # Lines
        Line= tk.Frame(stock_list_frame, bg="#272E3A")
        Line.place(x=0, y=124,width=246, height=2)

        Line_2= tk.Frame(stock_list_frame, bg="#272E3A")
        Line_2.place(x=0, y=166,width=246, height=2)

        button_frame.original_bg = "#111316"

        # Create labels for each stock attribute
        label_name = tk.Label(button_frame, text=stock[0], bg="#111316", fg="white", anchor="w",  highlightthickness= 0, font=("Arial", 13, "bold"))  # Stock name
        label_name.place(x=3, y=6)  

        label_info_1 = tk.Label(button_frame, text=stock[3], bg="#111316", fg="white", anchor="w", highlightthickness= 0, font=("Arial", 10))  
        label_info_1.place(x=3, y=32)  

        label_info_2 = tk.Label(button_frame, text=stock[1], bg="#111316", anchor="w", fg=color, highlightthickness= 0, font=("Arial", 10))  # Price
        label_info_2.place(x=65, y=32)

        label_info_3 = tk.Label(button_frame, text=stock[4], bg="#111316", anchor="w", fg=color, highlightthickness= 0, font=("Arial", 10))  # Change
        label_info_3.place(x=118, y=32)

        label_info_4 = tk.Label(button_frame, text=stock[2], bg="#111316", anchor="w", fg=color, highlightthickness= 0, font=("Arial", 10))  # Change ratio
        label_info_4.place(x=171, y=32) 

        # Bind a click event to the entire frame to simulate button behavior
        button_frame.bind("<Button-1>", lambda e, f=button_frame, s=stock: on_frame_click(f, s))

        # Also bind the click event to labels to ensure they trigger the same action
        for label in [label_name, label_info_1, label_info_2, label_info_3, label_info_4]:
            label.bind("<Button-1>", lambda e, f=button_frame, s=stock: on_frame_click(f, s))

        stock_y_offset += 80  # The interval between buttons 

stock_y_offset = 170  # Height of the whole buttons on this pannel

# Create buttons for stock choosing
for stock in stocks:
    change_str_s = stock[2]  # Get the change string
    change_value_k = float(change_str_s.replace("%", ""))  # Remove "%" and convert to float
    if change_value_k >= 0:
        color = "green"  # Change color with rise or drop of the stock
    else:
        color = "red"

    # Create a Frame to act like a button
    button_frame = tk.Frame(stock_list_frame, bg="#111316", width=232, height=70)
    button_frame.place(x=8, y=stock_y_offset)
    
    button_frame.original_bg = "#111316"

    # Create labels for each stock attribute
    label_name = tk.Label(button_frame, text=stock[0], bg="#111316", fg="white", anchor="w",  highlightthickness= 0, font=("Arial", 13, "bold"))  # Stock name
    label_name.place(x=3, y=5)  

    label_info_1 = tk.Label(button_frame, text=stock[3], bg="#111316", fg="white", anchor="w", highlightthickness= 0, font=("Arial", 10))  
    label_info_1.place(x=3, y=32)  

    label_info_2 = tk.Label(button_frame, text=stock[1], bg="#111316", anchor="w", fg=color, highlightthickness= 0, font=("Arial", 10))  # Price
    label_info_2.place(x=65, y=32)

    label_info_3 = tk.Label(button_frame, text=stock[4], bg="#111316", anchor="w", fg=color, highlightthickness= 0, font=("Arial", 10))  # Change
    label_info_3.place(x=118, y=32)

    label_info_4 = tk.Label(button_frame, text=stock[2], bg="#111316", anchor="w", fg=color, highlightthickness= 0, font=("Arial", 10))  # Change ratio
    label_info_4.place(x=171, y=32) 

    # Bind a click event to the entire frame to simulate button behavior
    button_frame.bind("<Button-1>", lambda e, f=button_frame, s=stock: on_frame_click(f, s))

    # Also bind the click event to labels to ensure they trigger the same action
    for label in [label_name, label_info_1, label_info_2, label_info_3, label_info_4]:
        label.bind("<Button-1>", lambda e, f=button_frame, s=stock: on_frame_click(f, s))

    stock_y_offset += 80  # The interval between buttons 

# Clicking "Message", "Chat" buttons would generate pop up window, Creat all buttons on the siderbar
buttons = {}

# Create buttons on the sidebar
for text, x, y in button_data:
    btn = tk.Button(sidebar, text=text, bg= "#272E3A",  # Dark gray button color
    fg= "white",  # White characteristics
    font= ("Arial", 14),  # Font size
    anchor= "c",  # Center the text
    relief= "flat",  # Add a raised effect
    bd= 1,  # No border by default
    highlightthickness= 0,
    width= 8,  # Fixed width for buttons (in text units)
    height= 1,
    highlightbackground="#FCCA00", highlightcolor="#FCCA00")

    btn.original_bg = "#272E3A" # Store the original background color

    def button_command(b=btn, text=text): # Added text=text to capture the current text value
        on_button_click(b)
        if text == "Message":
            show_under_development()
        elif text == "Chat":
            show_under_development()
        elif text in ("Market", "Account", "Finding"):
            show_under_development_panel()
        elif text == "Optional":
            show_stock_list_panel()

    btn.config(command=button_command)
    btn.place(x=x, y=y, width=110, height=40)
    buttons[text] = btn

# Preset the button to at "Optional"
optional_btn = buttons["Optional"]
on_button_click(optional_btn) 

# Header
header_frame = tk.Frame(sidebar, bg="#4f4f4f", width=67, height=67)
header_frame.place(x=13, y=17)

# Load the image
image = Image.open(r"image\head_image.jpg")
image = image.resize((67, 67), Image.LANCZOS)  # Resize the image to adapt the size of the frame
photo = ImageTk.PhotoImage(image)

# Create a label to hold the image
if photo:
    image_label = tk.Label(header_frame, image=photo, bg="#4f4f4f")
    image_label.image = photo  # Keep a reference to the image
    image_label.place(x=0, y=0)

# Create matplotlib figure and subplots with adjusted heights(The figure shouold be embedded in a pannel)
fig = Figure(figsize=(9, 7), facecolor='#111317')
ax1 = fig.add_subplot(211, facecolor='black')  # Upper plot
ax2 = fig.add_subplot(212, facecolor='black')  # Lower plot
ax1.set_position([0.08, 0.32, 0.9, 0.65])  # [left, bottom, width, height]
ax2.set_position([0.08, 0.04, 0.9, 0.25])  # [left, bottom, width, height]

# Set up the canvas for embedding matplotlib figure
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x=380, y=200)  # Set the position of the canvas

# New: Information tab, set initial position near the top left corner of the K chart
info_label = tk.Label(root, text="", fg="white", bg="black")
info_label.place(x=380, y=200)  # The initial position is near the top left corner of the canvas

# Functions to display last day's data
def show_last_day_data():
    if df is not None and len(df) > 0:
        last_index = len(df) - 1
        date = mdates.num2date(df['Date'][last_index])
        open_price = df['Open'][last_index]
        high_price = df['High'][last_index]
        low_price = df['Low'][last_index]
        close_price = df['Close'][last_index]
        volume = df['Volume'][last_index]
        info = f"Date: {date.strftime('%Y-%m-%d')}, Open: {open_price:.2f}, High: {high_price:.2f}, Low: {low_price:.2f}, Close: {close_price:.2f}, Volume: {volume}"
        info_label.config(text=info)

# Mouse movement event handler
def on_mouse_move(event):
    if event.inaxes == ax1:
        xdate = event.xdata
        ind = np.searchsorted(df['Date'], xdate)
        if 0 <= ind < len(df):
            date = mdates.num2date(df['Date'][ind])
            open_price = df['Open'][ind]
            high_price = df['High'][ind]
            low_price = df['Low'][ind]
            close_price = df['Close'][ind]
            volume = df['Volume'][ind]
            info = f"Date: {date.strftime('%Y-%m-%d')}, Open: {open_price:.2f}, High: {high_price:.2f}, Low: {low_price:.2f}, Close: {close_price:.2f}, Volume: {volume}"
            info_label.config(text=info)
        else:
            show_last_day_data()
    else:
        show_last_day_data()

# Function to update the main chart
def update_chart():
    ax1.clear()
    ax2.clear()
    ax1.set_facecolor('#111317')
    ax2.set_facecolor('#111317')
    ax1.tick_params(axis='y', colors='white')
    ax2.tick_params(axis='both', colors='white')
    ax1.title.set_color('white')
    ax1.set_ylabel('Price', color='white')
    ax1.tick_params(axis='x', colors='#111317')

    last_20_days_df = df.iloc[-30:]
    last_20_days_ohlc = ohlc.iloc[-30:]

    # Plot candlestick chart
    if df is not None and ohlc is not None:
        candlestick_ohlc(ax1, last_20_days_ohlc.values, width=0.6, colorup='g', colordown='r')
        show_last_day_data()

    # Plot moving averages if selected
    ma_colors = {'MA5': 'orange', 'MA10': '#00BFFF', 'MA20': '#BA55D3', 'MA60': '#98FB98'}
    for ma in selected_ma:
        if ma in ma_colors:
            ax1.plot(last_20_days_df['Date'], last_20_days_df[ma], color=ma_colors[ma])

    # Plot Bollinger Bands if selected
    if show_bollinger.get():
        ax1.plot(last_20_days_df['Date'], last_20_days_df['UB'], color='cyan')
        ax1.plot(last_20_days_df['Date'], last_20_days_df['MB'], color='magenta')
        ax1.plot(last_20_days_df['Date'], last_20_days_df['LB'], color='cyan')

    # Plot indicators in the second subplot if selected
    if selected_indicator == 'Volume':
        colors = ['g' if close >= open_ else 'r' for close, open_ in zip(last_20_days_df['Close'], last_20_days_df['Open'])]
        ax2.bar(last_20_days_df['Date'], last_20_days_df['Volume'], color=colors, label='Volume')
        ax2.set_ylabel('Volume', color='white')
    elif selected_indicator == 'MACD':
        ax2.plot(last_20_days_df['Date'], last_20_days_df['macd'], label='MACD', color='cyan')
        ax2.plot(last_20_days_df['Date'], last_20_days_df['signal'], label='Signal', color='orange')
        bar_r = np.where(last_20_days_df['histogram'] > 0, last_20_days_df['histogram'], 0)
        bar_g = np.where(last_20_days_df['histogram'] <= 0, last_20_days_df['histogram'], 0)
        ax2.bar(last_20_days_df['Date'], bar_r, color='red', label='Histogram (Positive)')
        ax2.bar(last_20_days_df['Date'], bar_g, color='green', label='Histogram (Negative)')
        ax2.set_ylabel('MACD', color='white')
    elif selected_indicator == 'RSI':
        ax2.plot(last_20_days_df['Date'], last_20_days_df['RSI'], label='RSI', color='cyan')
        ax2.axhline(y=70, color='red', linestyle='--', label='Overbought')
        ax2.axhline(y=30, color='green', linestyle='--', label='Oversold')
        ax2.set_ylabel('RSI', color='white')
    elif selected_indicator == 'KDJ':
        ax2.plot(last_20_days_df['Date'], last_20_days_df['K'], label='K', color='orange')
        ax2.plot(last_20_days_df['Date'], last_20_days_df['D'], label='D', color='blue')
        ax2.plot(last_20_days_df['Date'], last_20_days_df['J'], label='J', color='magenta')
        ax2.set_ylabel('KDJ', color='white')

    # Filter out MA and Bollinger Bands labels for the first subplot
    handles1, labels1 = ax1.get_legend_handles_labels()
    filtered_handles1 = []
    filtered_labels1 = []
    exclude_labels = ['MA5', 'MA10', 'MA20', 'MA60', 'Upper Band', 'Middle Band', 'Lower Band']
    for handle, label in zip(handles1, labels1):
        if label not in exclude_labels:
            filtered_handles1.append(handle)
            filtered_labels1.append(label)

    # Add legends if any labels are present
    if filtered_labels1:
        ax1.legend(handles=filtered_handles1, labels=filtered_labels1, loc='upper left', fontsize=8)
    handles2, labels2 = ax2.get_legend_handles_labels()
    if handles2:
        ax2.legend(handles=handles2, labels=labels2, loc='upper left',bbox_to_anchor=(0.05, 1.15), 
                   fontsize=8, ncol=len(handles2),facecolor='#272E3A',frameon=False, labelcolor='white')


    ax1.xaxis_date()
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax2.xaxis_date()
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    canvas.draw()

# Function to handle MA checkboxes
def toggle_ma(ma):
    if ma in selected_ma:
        selected_ma.remove(ma)
    else:
        selected_ma.append(ma)
    update_chart()

# Create moving average checkboxes (Row 2)
ma_checkbox_frame = tk.Frame(chosen_index_panel, bg="#111316")
ma_checkbox_frame.place(x=15, y=10)  # Adjust position below the stock buttons

# MA5 Checkbox
ma5_var = tk.IntVar()
ma5_checkbox = tk.Checkbutton(
    ma_checkbox_frame,
    text="MA5",
    variable=ma5_var,
    command=lambda: toggle_ma('MA5'),
    bg="#111316",
    fg="orange",
    selectcolor="#111316",
    font=("Arial", 11)
)
ma5_checkbox.pack(side=tk.LEFT, padx=5)

# MA10 Checkbox
ma10_var = tk.IntVar()
ma10_checkbox = tk.Checkbutton(
    ma_checkbox_frame,
    text="MA10",
    variable=ma10_var,
    command=lambda: toggle_ma('MA10'),
    bg="#111316",
    fg="#00BFFF",
    selectcolor="#111316",
    font=("Arial", 11)
)
ma10_checkbox.pack(side=tk.LEFT, padx=5)

# MA20 Checkbox
ma20_var = tk.IntVar()
ma20_checkbox = tk.Checkbutton(
    ma_checkbox_frame,
    text="MA20",
    variable=ma20_var,
    command=lambda: toggle_ma('MA20'),
    bg="#111316",
    fg="#BA55D3",
    selectcolor="#111316",
    font=("Arial", 11)
)
ma20_checkbox.pack(side=tk.LEFT, padx=5)

# MA60 Checkbox
ma60_var = tk.IntVar()
ma60_checkbox = tk.Checkbutton(
    ma_checkbox_frame,
    text="MA60",
    variable=ma60_var,
    command=lambda: toggle_ma('MA60'),
    bg="#111316",
    fg="#98FB98",
    selectcolor="#111316",
    font=("Arial", 11)
)
ma60_checkbox.pack(side=tk.LEFT, padx=5)

# Bollinger Bands Checkbox
bollinger_checkbox = tk.Checkbutton(
    ma_checkbox_frame,
    text="Bollinger Bands",
    variable=show_bollinger,
    command=update_chart,
    bg="#111316",
    fg="white",
    selectcolor="#111316",
    font=("Arial", 11)
)
bollinger_checkbox.pack(side=tk.LEFT, padx=5)

# Create indicator buttons (Row 3)
indicator_button_frame = tk.Frame(chosen_index_panel, bg="#111316")
indicator_button_frame.place(x=580, y=10)  # Adjust position below the moving average buttons

# New indicator tick box variables
indicator_vars = {
    'Volume': tk.IntVar(),
    'MACD': tk.IntVar(),
    'RSI': tk.IntVar(),
    'KDJ': tk.IntVar()
}

# Ensure that Show Volume is ticked by default
indicator_vars['Volume'].set(1)

# Logic for selecting only one indicator
def select_single_indicator(indicator):
    for ind, var in indicator_vars.items():
        if ind == indicator:
            var.set(1)
            select_indicator(indicator)
        else:
            var.set(0)

# Create Indicator Tickbox
for indicator, var in indicator_vars.items():
    tk.Checkbutton(
        indicator_button_frame,
        text=indicator,
        variable=var,
        command=lambda ind=indicator: select_single_indicator(ind),
        bg="#111316",
        fg="white",
        selectcolor="#111316",
        font=("Arial", 11)
    ).pack(side=tk.LEFT, padx=5)

# Initial chart update
update_chart()

# Initialisation to show last day's data
show_last_day_data()
# Bind mouse movement events to ax1
canvas.mpl_connect('motion_notify_event', on_mouse_move)

# Create an exit button and add it to the existing main window.
exit_button = tk.Button(root, text=" X ", command=confirm_exit)
exit_button.place(x=1250, y=0)
    
# Run Tkinter main loop
root.mainloop()