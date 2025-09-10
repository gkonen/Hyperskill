
import requests
import json


local_currency = input().upper()
res = requests.get(f"http://www.floatrates.com/daily/{local_currency}.json")
data = json.loads(res.text)

favorite_currency = { "USD", "EUR" }
cache = dict()


for target in favorite_currency:
    if target != local_currency:
        cache[target] = data[target.lower()]

finish = False
while not finish:
    currency = input().upper()
    if currency == "":
        finish = True
    else:
        amount = float(input())
        rate = 0.0
        print("Checking the cache...")
        if currency in cache.keys():
            print("Oh! It is in the cache!")
            rate = cache[currency]["rate"]
        else:
            print("Sorry, but it is not in the cache.")
            res = requests.get(f"http://www.floatrates.com/daily/{local_currency}.json")
            data = json.loads(res.text)
            cache[currency] = data[currency.lower()]
            rate = cache[currency]["rate"]
        print(f"You received {round(amount * rate, 2)} {currency}.")
