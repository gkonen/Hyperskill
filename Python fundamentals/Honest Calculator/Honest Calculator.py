msg_0 = "Enter an equation"
msg_1 = "Do you even know what numbers are? Stay focused!"
msg_2 = "Yes ... an interesting math operation. You've slept through all classes, haven't you?"
msg_3 = "Yeah... division by zero. Smart move..."
msg_4 = "Do you want to store the result? (y / n):"
msg_5 = "Do you want to continue calculations? (y / n):"
msg_6 = " ... lazy"
msg_7 = " ... very lazy"
msg_8 = " ... very, very lazy"
msg_9 = "You are"
msg_10 = "Are you sure? It is only one digit! (y / n)"
msg_11 = "Don't be silly! It's just one number! Add to the memory? (y / n)"
msg_12 = "Last chance! Do you really want to embarrass yourself? (y / n)"

operation = [ "+", "-", "*", "/" ]

def test_numeric(value):
    try:
        float(value)
    except:
        return None
    else:
       return float(value)

def is_one_digit(v):
    if not v.is_integer():
        return False
    else:
        return -10 < v < 10

def check(v1,v2,v3):
    msg = ""
    if is_one_digit(v1) and is_one_digit(v2):
        msg += msg_6
    if (v1 == 1 or v2 == 1) and v3 == "*":
        msg += msg_7
    if (v1 == 0 or v2 == 0) and (v3 == "*" or v3 == "+" or v3 == "-"):
        msg += msg_8
    if msg != "":
        msg = msg_9 + msg
        print(msg)


good_operation = True
result = None
memory = 0.0
while good_operation:
    print(msg_0)
    calc = input()
    x, oper, y = calc.split(" ")
    if x == "M" and y == "M":
        x = memory
        y = memory
    elif x == "M":
        x = memory
        y = test_numeric(y)
    elif y == "M":
        x = test_numeric(x)
        y = memory
    else:
        x = test_numeric(x)
        y = test_numeric(y)

    if x is None or y is None:
        print(msg_1)
    else:
        if not oper in operation:
            print(msg_2)
        else:
            check(x,y,oper)
            if oper == "+":
                result = x + y
            elif oper == "-":
                result = x - y
            elif oper == "*":
                result = x * y
            elif oper == "/":
                if y == 0:
                    print(msg_3)
                else:
                    result = x / y

    if result is not None:
        print(result)
        keep_result = False
        while not keep_result:
            print(msg_4)
            answer = input()
            if answer == "y":
                keep_result = True
                if is_one_digit(result):
                    msg_index = 10
                    keep_memory = True
                    while keep_memory:
                        if msg_index == 10:
                            print(msg_10)
                        elif msg_index == 11:
                            print(msg_11)
                        elif msg_index == 12:
                            print(msg_12)
                        answer = input()
                        if answer == "y":
                            if msg_index >= 12:
                                memory = result
                                keep_memory = False
                            else:
                                msg_index += 1
                        elif answer == "n":
                            keep_memory = False
                else:
                    memory = result

            elif answer == "n":
                keep_result = True
            result = None

        rep_calc = False
        while not rep_calc:
            print(msg_5)
            answer = input()
            if answer == "y":
                rep_calc = True
            elif answer == "n":
                rep_calc = True
                good_operation = False
