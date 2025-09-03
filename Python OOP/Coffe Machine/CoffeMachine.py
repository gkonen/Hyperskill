# region STEP 1 : Making coffee
print("Starting to make a coffee")
print("Grinding coffee beans")
print("Boiling water")
print("Mixing boiled water with crushed coffee beans")
print("Pouring coffee into the cup")
print("Pouring some milk into the cup")
print("Coffee is ready!")
# endregion

# region STEP 2 : Ingredient calculator
class CoffeeMachine:
    water_by_cups = 200
    milk_by_cups = 50
    beans_by_cups = 15

    def __init__(self, reserve_water=0, reserve_milk=0, reserve_coffee=0):
        self.qt_water = reserve_water
        self.qt_milk = reserve_milk
        self.qt_coffee = reserve_coffee

    def ingredients(self, quantities):
        print(f"For {quantities} cups of coffee you will need: \n"
              f"{self.water_by_cups * quantities} ml of water \n"
              f"{self.milk_by_cups * quantities} ml of milk \n"
              f"{self.beans_by_cups * quantities} g of coffee beans ")


n = int(input("Write how many cups of coffee you will need: \n"))
machine = CoffeeMachine()
machine.ingredients(n)
# endregion

# region STEP 3 : Estimate the number of servings

class CoffeeMachine:
    water_by_cups = 200
    milk_by_cups = 50
    beans_by_cups = 15

    def __init__(self, reserve_water=0, reserve_milk=0, reserve_coffee=0):
        self.qt_water = reserve_water
        self.qt_milk = reserve_milk
        self.qt_coffee = reserve_coffee

    def test_reserve_water(self, quantities):
        return self.qt_water // self.water_by_cups

    def test_reserve_milk(self, quantities):
        return self.qt_milk // self.milk_by_cups

    def test_reserve_coffee(self, quantities):
        return self.qt_coffee // self.beans_by_cups

    def test_reserve(self,quantities):
        capacity = [
            self.test_reserve_water(quantities),
            self.test_reserve_milk(quantities),
            self.test_reserve_coffee(quantities)
        ]
        return min(capacity)

    def ingredients(self, quantities):
        capacity = self.test_reserve(quantities)
        if capacity == quantities:
            print("Yes, I can make that amount of coffee")
        elif capacity > quantities:
            print(f"Yes, I can make that amount of coffee (and even {capacity-quantities} more than that)")
        else:
            print(f"No, I can make only {capacity} cups of coffee")

water = int(input("Write how many ml of water the coffee machine has: \n"))
milk =  int(input("Write how many ml of milk the coffee machine has: \n"))
beans =  int(input("Write how many grams of coffee beans the coffee machine has: \n"))
machine = CoffeeMachine(water, milk, beans)

n = int(input("Write how many cups of coffee you will need: \n"))
machine.ingredients(n)

# endregion

# region STEP 3 : Buy, fill, take!
import math
class CoffeeMachine:

    ingredients = {"water", "milk", "coffee"}
    drinks = {
        "espresso": {"water": 250, "milk": 0, "coffee": 16, "price": 4 },
        "latte": {"water": 350, "milk": 75, "coffee": 20, "price": 7 },
        "cappuccino": {"water": 200, "milk": 100, "coffee": 12, "price": 6 }
    }

    def __init__(self, reserve_water=0, reserve_milk=0, reserve_coffee=0, reserve_cup=0, money=0 ):
        self.qt_water = reserve_water
        self.qt_milk = reserve_milk
        self.qt_coffee = reserve_coffee
        self.qt_cup = reserve_cup
        self.money = money

    def __test_reserve_water(self, drink):
        if self.drinks[drink]["water"] == 0:
            return math.inf
        else:
            return self.qt_water // self.drinks[drink]["water"]

    def __test_reserve_milk(self, drink):
        if self.drinks[drink]["milk"] == 0:
            return math.inf
        else:
            return self.qt_milk // self.drinks[drink]["milk"]

    def __test_reserve_coffee(self, drink):
        if self.drinks[drink]["coffee"] == 0:
            return math.inf
        else:
            return self.qt_coffee // self.drinks[drink]["coffee"]

    def test_reserve(self, drink):
        capacity = [
            self.__test_reserve_water(drink),
            self.__test_reserve_milk(drink),
            self.__test_reserve_coffee(drink)
        ]
        return min(capacity)

    def buy(self, drink, quantities=1):
        if drink not in self.drinks.keys():
            return
        else:
            if self.capacities(drink, quantities) and self.qt_cup > quantities:
                self.money += self.drinks[drink]["price"]*quantities

                self.qt_water -= self.drinks[drink]["water"]*quantities
                self.qt_milk -= self.drinks[drink]["milk"]*quantities
                self.qt_coffee -= self.drinks[drink]["coffee"]*quantities
                self.qt_cup -= quantities

    def fill(self):
        water = int(input("Write how many ml of water you want to add : \n"))
        milk = int(input("Write how many ml of milk you want to add: \n"))
        beans = int(input("Write how many grams of coffee beans you want to add: \n"))
        cups = int(input("Write how many disposable cups you want to add: \n"))
        self.qt_water += water
        self.qt_milk += milk
        self.qt_coffee += beans
        self.qt_cup += cups

    def take(self):
        print(f"I gave you {self.money}")
        self.money = 0

    def capacities(self, drink, quantities=1):
        capacity = self.test_reserve(drink)
        return capacity >= quantities


def __str__(self):
    return f"The coffe machine has:\n" \
           f"{self.qt_water} of water\n" \
           f"{self.qt_milk} of milk\n" \
           f"{self.qt_coffee} of coffee beans\n" \
           f"{self.qt_cup} of disposable cups\n" \
           f"${self.money} of money\n"


machine = CoffeeMachine(400, 540, 120, 9, 550)
print(str(machine))
choice = input("Write action (buy, fill, take) :")
if choice == "buy":
    choice = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino: \n")
    drink = 0
    match choice:
        case "1":
            drink = "espresso"
        case "2":
            drink = "latte"
        case "3":
            drink = "cappuccino"

    machine.buy(drink)

elif choice == "fill":
    machine.fill()
elif choice == "take":
    machine.take()
print()
print(str(machine))


# endregion

# region STEP4 : Keep track of the supplies
import math
class CoffeeMachine:

    drinks = {
        "espresso": {"water": 250, "milk": 0, "coffee": 16, "price": 4 },
        "latte": {"water": 350, "milk": 75, "coffee": 20, "price": 7 },
        "cappuccino": {"water": 200, "milk": 100, "coffee": 12, "price": 6 }
    }

    def __init__(self, reserve_water=0, reserve_milk=0, reserve_coffee=0, reserve_cup=0, money=0 ):
        self.qt_water = reserve_water
        self.qt_milk = reserve_milk
        self.qt_coffee = reserve_coffee
        self.qt_cup = reserve_cup
        self.money = money

    def __test_reserve_water(self, drink):
        if self.drinks[drink]["water"] == 0:
            return math.inf
        else:
            return self.qt_water // self.drinks[drink]["water"]

    def __test_reserve_milk(self, drink):
        if self.drinks[drink]["milk"] == 0:
            return math.inf
        else:
            return self.qt_milk // self.drinks[drink]["milk"]

    def __test_reserve_coffee(self, drink):
        if self.drinks[drink]["coffee"] == 0:
            return math.inf
        else:
            return self.qt_coffee // self.drinks[drink]["coffee"]

    def test_reserve(self, drink):
        if self.__test_reserve_water(drink) == 0:
            print("Sorry, not enough water")
            return None
        elif self.__test_reserve_milk(drink) == 0:
            print("Sorry, not enough milk")
            return None
        elif self.__test_reserve_coffee(drink) == 0:
            print("Sorry, not enough coffee")
            return None
        elif self.qt_cup == 0:
            print("Sorry, not enough cup")
            return None
        else:
            capacity = [
                self.__test_reserve_water(drink),
                self.__test_reserve_milk(drink),
                self.__test_reserve_coffee(drink)
            ]
            return min(capacity)

    def capacities(self, drink, quantities=1):
        capacity = self.test_reserve(drink)
        if capacity is None:
            return False
        else :
            return capacity >= quantities

    def buy(self, drink, quantities=1):
        if drink not in self.drinks.keys():
            return
        else:
            if self.capacities(drink, quantities) and self.qt_cup > quantities:
                self.money += self.drinks[drink]["price"]*quantities

                self.qt_water -= self.drinks[drink]["water"]*quantities
                self.qt_milk -= self.drinks[drink]["milk"]*quantities
                self.qt_coffee -= self.drinks[drink]["coffee"]*quantities
                self.qt_cup -= quantities

    def fill(self):
        water = int(input("Write how many ml of water you want to add : \n"))
        milk = int(input("Write how many ml of milk you want to add: \n"))
        beans = int(input("Write how many grams of coffee beans you want to add: \n"))
        cups = int(input("Write how many disposable cups you want to add: \n"))
        self.qt_water += water
        self.qt_milk += milk
        self.qt_coffee += beans
        self.qt_cup += cups

    def take(self):
        print(f"I gave you {self.money}")
        self.money = 0


def __str__(self):
    return f"The coffe machine has:\n" \
           f"{self.qt_water} of water\n" \
           f"{self.qt_milk} of milk\n" \
           f"{self.qt_coffee} of coffee beans\n" \
           f"{self.qt_cup} of disposable cups\n" \
           f"${self.money} of money\n"


machine = CoffeeMachine(400, 540,120, 9, 550)

while True:
    choice = input("Write action (buy, fill, take, remaining, exit) :")
    if choice == "buy":
        choice = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino: \n")
        drink = 0
        match choice:
            case "1":
                drink = "espresso"
            case "2":
                drink = "latte"
            case "3":
                drink = "cappuccino"
        machine.buy(drink)

    elif choice == "fill":
        machine.fill()
    elif choice == "take":
        machine.take()
    elif choice == "remaining":
        print(str(machine))
    elif choice == "exit":
        exit()

# endregion

# region STEP 6 : Brush your code

import math
class CoffeeMachine:

    drinks = {
        "espresso": {"water": 250, "milk": 0, "coffee": 16, "price": 4 },
        "latte": {"water": 350, "milk": 75, "coffee": 20, "price": 7 },
        "cappuccino": {"water": 200, "milk": 100, "coffee": 12, "price": 6 }
    }

    def __init__(self, reserve_water=0, reserve_milk=0, reserve_coffee=0, reserve_cup=0, money=0 ):
        self.qt_water = reserve_water
        self.qt_milk = reserve_milk
        self.qt_coffee = reserve_coffee
        self.qt_cup = reserve_cup
        self.money = money

    def __test_reserve_water(self, drink):
        if self.drinks[drink]["water"] == 0:
            return math.inf
        else:
            return self.qt_water // self.drinks[drink]["water"]

    def __test_reserve_milk(self, drink):
        if self.drinks[drink]["milk"] == 0:
            return math.inf
        else:
            return self.qt_milk // self.drinks[drink]["milk"]

    def __test_reserve_coffee(self, drink):
        if self.drinks[drink]["coffee"] == 0:
            return math.inf
        else:
            return self.qt_coffee // self.drinks[drink]["coffee"]

    def test_reserve(self, drink):
        if self.__test_reserve_water(drink) == 0:
            print("Sorry, not enough water")
            return None
        elif self.__test_reserve_milk(drink) == 0:
            print("Sorry, not enough milk")
            return None
        elif self.__test_reserve_coffee(drink) == 0:
            print("Sorry, not enough coffee")
            return None
        elif self.qt_cup == 0:
            print("Sorry, not enough cup")
            return None
        else:
            capacity = [
                self.__test_reserve_water(drink),
                self.__test_reserve_milk(drink),
                self.__test_reserve_coffee(drink)
            ]
            return min(capacity)

    def capacities(self, drink, quantities=1):
        capacity = self.test_reserve(drink)
        if capacity is None:
            return False
        else :
            return capacity >= quantities

    def buy(self, drink, quantities=1):
        if drink not in self.drinks.keys():
            return
        else:
            if self.capacities(drink, quantities) and self.qt_cup > quantities:
                self.money += self.drinks[drink]["price"]*quantities

                self.qt_water -= self.drinks[drink]["water"]*quantities
                self.qt_milk -= self.drinks[drink]["milk"]*quantities
                self.qt_coffee -= self.drinks[drink]["coffee"]*quantities
                self.qt_cup -= quantities

    def fill(self):
        water = int(input("Write how many ml of water you want to add : \n"))
        milk = int(input("Write how many ml of milk you want to add: \n"))
        beans = int(input("Write how many grams of coffee beans you want to add: \n"))
        cups = int(input("Write how many disposable cups you want to add: \n"))
        self.qt_water += water
        self.qt_milk += milk
        self.qt_coffee += beans
        self.qt_cup += cups

    def take(self):
        print(f"I gave you {self.money}")
        self.money = 0

    def order(self, choice):
        if choice == "buy":
            choice = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino: \n")
            drink = 0
            match choice:
                case "1":
                    drink = "espresso"
                case "2":
                    drink = "latte"
                case "3":
                    drink = "cappuccino"
            self.buy(drink)

        elif choice == "fill":
            self.fill()
        elif choice == "take":
            self.take()
        elif choice == "remaining":
            print(str(self))
        elif choice == "exit":
            exit()


    def __str__(self):
        return f"The coffe machine has:\n"\
               f"{self.qt_water} of water\n"\
               f"{self.qt_milk} of milk\n"\
               f"{self.qt_coffee} of coffee beans\n"\
               f"{self.qt_cup} of disposable cups\n"\
               f"${self.money} of money\n"

machine = CoffeeMachine(400, 540,120, 9, 550)

while True:
    choice = input("Write action (buy, fill, take, remaining, exit) :")
    machine.order(choice)

#endregion