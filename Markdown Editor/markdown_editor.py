
def formatters(sign):
    def decorator(func):
        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)
            return sign + text + sign
        return wrapper
    return decorator

def header():
    good_input = False
    head_text = ""
    while not good_input:
        try:
            level = int(input("Level: "))
            if 1 <= level <= 6:
                text = input("Text: ")
                head_text = "#"*level + " " + text + "\n"
                good_input = True
            else:
                print("The level should be within the range of 1 to 6")
        except ValueError:
            pass
    return head_text

@formatters("")
def plain():
    text = input("Text: ")
    return text

@formatters("*")
def italic():
    text = input("Text: ")
    return text

@formatters("**")
def bold():
    text = input("Text: ")
    return text

@formatters("`")
def inline_code():
    text = input("Text: ")
    return text

def link():
    label = input("Label: ")
    url = input("URL: ")
    return f"[{label}]({url})"

def new_line():
    return "\n"

def mark_list(ordered: bool):
    size = 0
    good_input = False
    while not good_input:
        try:
            size = int(input("Number of Rows: "))
            if size <= 0:
                raise ValueError
        except ValueError:
            print("The number of rows should be greater than zero")
        else:
            good_input = True
    text = ""
    for i in range(1,size+1):
        row = input(f"Row #{i}: ")
        balise = f"{i}. " if ordered else "* "
        text += balise + row + "\n"
    return text

def ordered_list():
    return mark_list(True)

def unordered_list():
    return mark_list(False)

def done(text):
    with open("output.md", "w") as f:
        f.write(text)



feature = {
    "plain": plain,
    "bold" : bold,
    "italic": italic,
    "inline-code": inline_code,
    "link": link,
    "header": header,
    "new-line": new_line,
    "ordered-list": ordered_list,
    "unordered-list": unordered_list
}

special_command = {
    "!help": "",
    "!done": ""
}

formated_text = ""
command = ""

while command != "!done":
    command = input("Choose a formatter: ")
    if command not in feature.keys() and command not in special_command.keys():
        print("Unknown formatting type or command")
    elif command == "!help":
        print("Available formatters:", end=' ')
        for key, value in feature.items():
            print(key, end=' ')
        print("\nSpecial commands:", end=' ')
        for key, value in special_command.items():
            print(key, end=' ')
        print()
    elif command == "!done":
        done(formated_text)
        break
    else:
        formated_text += feature[command]()
        print(formated_text)

