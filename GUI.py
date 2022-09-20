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

str_digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]


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

        # Numbers frame:

        frame_numbers = Frame(root)
        frame_numbers.grid()

        btn_1 = Button(frame_numbers, text="1", command=lambda: self.number_clicked("1"))
        btn_2 = Button(frame_numbers, text="2", command=lambda: self.number_clicked("2"))
        btn_3 = Button(frame_numbers, text="3", command=lambda: self.number_clicked("3"))

        btn_1.grid(row=0, column=0)
        btn_2.grid(row=0, column=1)
        btn_3.grid(row=0, column=2)

        btn_4 = Button(frame_numbers, text="4", command=lambda: self.number_clicked("4"))
        btn_5 = Button(frame_numbers, text="5", command=lambda: self.number_clicked("5"))
        btn_6 = Button(frame_numbers, text="6", command=lambda: self.number_clicked("6"))

        btn_4.grid(row=1, column=0)
        btn_5.grid(row=1, column=1)
        btn_6.grid(row=1, column=2)

        btn_7 = Button(frame_numbers, text="7", command=lambda: self.number_clicked("7"))
        btn_8 = Button(frame_numbers, text="8", command=lambda: self.number_clicked("8"))
        btn_9 = Button(frame_numbers, text="9", command=lambda: self.number_clicked("9"))

        btn_7.grid(row=2, column=0)
        btn_8.grid(row=2, column=1)
        btn_9.grid(row=2, column=2)

        btn_dot = Button(frame_numbers, text=".", command=lambda: self.number_clicked("."))
        btn_0 = Button(frame_numbers, text="0", command=lambda: self.number_clicked("0"))
        btn_back = Button(frame_numbers, text="⌫", command=lambda: self.number_clicked("B"))

        btn_dot.grid(row=3, column=0)
        btn_0.grid(row=3, column=1)
        btn_back.grid(row=3, column=2)

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

    def number_clicked(self, number):
        if number in str_digits or number == "." and "." not in self.txt_amount.get():
            self.txt_amount.insert(len(self.txt_amount.get()), number)
        elif number == "B":
            self.txt_amount.delete(len(self.txt_amount.get())-1, END)

GUI()

