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


def is_float(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

while 1:
    cur_1 = input("Enter from what to convert: ").upper()
    cur_2 = input("Enter what to convert to: ").upper()
    amount = input("Enter amount: ")
    if cur_1 in all_currencies and cur_2 in all_currencies and is_float(amount):
        break

today = date.today()
yesterday = today - timedelta(days=1)
print(today, yesterday)

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
print(rate1)
print(rate2)

# print(json.dumps(data, indent=4, sort_keys=True))
