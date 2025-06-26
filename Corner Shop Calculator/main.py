#region STAGE 1 : Print the prices
d = { "Bubblegum": 2, "Toffee": 0.2, "Ice cream": 5, "Milk chocolate": 4, "Doughnut": 2.5, "Pancake": 3.2}
print("Prices")
for n in d.keys():
    print(f"{n}: ${d[n]}")

#endregion

#region STAGE 2 : Measure total income of your shop
d = { "Bubblegum": 202, "Toffee": 118, "Ice cream": 2250, "Milk chocolate": 1680, "Doughnut": 1075, "Pancake": 80}
print("Earned amount:")
for n in d.keys():
    print(f"{n}: ${d[n]}")

print(f"Income: {float(sum(d.values()))}")

#endregion

#region STAGE 3 : Calculate net income
d = { "Bubblegum": 202, "Toffee": 118, "Ice cream": 2250, "Milk chocolate": 1680, "Doughnut": 1075, "Pancake": 80}
print("Earned amount:")
for n in d.keys():
    print(f"{n}: ${d[n]}")

total = sum(d.values())
print(f"Income: ¤{total}")

staff_expenses = int(input("Staff expenses:"))
expenses = int(input("Other expenses:"))

print(f"Net income: ${total - staff_expenses - expenses}")
#endregion