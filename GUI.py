import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk

import requests
import json
from datetime import date
from datetime import timedelta


all_currencies = {
    "AUD": "Australian dollar",
    "BDT": "Bangladeshi taka", "BGN": "Bulgarian lev", "BYN": "Belarusian new rouble", "BRL": "Brazilian real",
    "CAD": " Canadian dollar", "CHF": "Swiss franc", "CNY": "Chinese yuan", "CZK": "Czech koruna",
    "DKK": "Danish krone",
    "EUR": "Euro",
    "GBP": "Pound sterling",
    "HKD": "Hong Kong dollar", "HRK": "Croatian kuna", "HUF": "Hungarian forint",
    "IDR": "Indonesian rupiah", "ILS": "Israeli new shekel", "INR": "Indian rupee", "ISK": "Icelandic krona", "I44": "Import-weighted krone exchange rate",
    "JPY": "Japanese yen",
    "KRW": "South Korean won",
    "MMK": "Myanmar kyat", "MYR": "Malaysian ringgit", "MXN": "Mexican peso",
    "NZD": "New Zealand dollar",
    "PHP": "Philippine peso", "PLN": "Polish zloty", "PKR": "Pakistani rupee",
    "RON": "New Romanian leu", "RUB": "Russian rouble",
    "SEK": "Swedish krona", "SGD": "Singapore dollar",
    "THB": "Thai baht", "TRY": "Turkish lira", "TWD": "New Taiwan dollar", "TWI": "Trade-weighted krone exchange rate",
    "USD": "US dollar",
    "VND": "Vietnamese dong",
    "XDR": "IMF, special drawing rights",
    "ZAR": "South African rand"
}


root = tk.Tk()
root.geometry("500x500")
root.title("Currency Converter")


class GUI:

    txt_amount = None


    def __init__(self):
        values = []
        for cur in all_currencies:
            values.append(cur + " (" + all_currencies[cur] + ")")

        self.box_cur1 = ttk.Combobox(root, values=values)
        self.box_cur2 = ttk.Combobox(root, values=values)

        self.draw()

    def draw(self):

        # Top frame:

        frame_entry = Frame(root)
        frame_entry.grid()

        self.txt_amount = Entry(frame_entry, text="Enter amount: ")
        self.txt_amount.grid(row=0, column=0)

        btn_enter = Button(frame_entry, text="Enter", command=self.entered)
        btn_enter.grid(row=0, column=1)

        root.grid_columnconfigure(0, weight=1)

        # Currency Drop downs:

        style = ttk.Style(root)  # If you dont have a class, put your root in the()
        style.configure('TCombobox', arrowsize=30)
        style.configure('Vertical.TScrollbar', arrowsize=28)

        self.box_cur1.grid()
        self.box_cur2.grid()

        root.mainloop()

    def entered(self):
        today = date.today()
        yesterday = today - timedelta(days=1)

        cur_1 = self.box_cur1.get().split(" ", 1)[0]
        cur_2 = self.box_cur2.get().split(" ", 1)[0]

        currencies = cur_1 + "+" + cur_2
        url = "https://data.norges-bank.no/api/data/EXR/B.{}.NOK.SP?format=sdmx-json&startPeriod={}" \
              "&endPeriod={}&locale=en".format(currencies, yesterday, today)
        rates = requests.get(url)
        data = rates.content.decode()

        data = json.loads(data)
        data_series = data["data"]["dataSets"][0]["series"]

        data_cur1_key = "0:0:0:0"
        data_cur2_key = "0:1:0:0"
        if cur_1 > cur_2:
            data_cur1_key = "0:1:0:0"
            data_cur2_key = "0:0:0:0"
        data_cur1 = data_series[data_cur1_key]["observations"]["0"]
        data_cur2 = data_series[data_cur2_key]["observations"]["0"]

        rate1 = data_cur1[len(data_cur1) - 1]
        rate2 = data_cur2[len(data_cur2) - 1]

        print(rate1, rate2)


GUI()

