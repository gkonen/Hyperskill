
# region METACHARACTERS ?
def check_zero_or_one(prev_char, regex, text):
    # check zero, so we ignore prev_char
    if compare(regex, text):
        return True

    # If we have nothing to check, we end here
    if len(text) == 0:
        return False
    else:
        # check once, so we compare the precedent char then the remaining
        if compare_one(prev_char, text[0]):
            # we check the remaining regex otherwise we succeed
            if regex:
                return compare(regex, text[1:])
            else:
                return True
        else:
            return False

# endregion

# region METACHARACTERS *
def check_zero_or_many(prev_char, regex, text):
    # if we consume all the text, we ultimately need to check if the regex matches with a void text
    if len(text) == 0:
        return compare(regex, "")
    # we check zero occurrence, we ignore prev_char
    if compare(regex, text):
        return True
    # we check if we have much occurrence
    else:
        # We check the first character
        if compare_one(prev_char, text[0]):
            # we loop recursively to consume the repetition of character
            if check_zero_or_many(prev_char, regex, text[1:]):
                return True
            # when we consume all the repetition, we compare the remaining text
            else:
                return compare(regex, text[1:])
        # We find the end of the repetition without consuming all the text
        else:
            return False

# endregion

# region METACHARACTERS +
def check_one_or_many(prev_char, regex, text):
    # If we have nothing to check, we end here
    if len(text) == 0:
        return False
    # check at least one
    if not compare_one(prev_char, text[0]):
        return False
    # check the remaining
    elif compare(regex, text[1:]):
        return True
    # case where we have repetition
    else:
        # we check the first character
        if compare_one(prev_char, text[0]):
            # we loop recursively to consume the repetition of character
            if check_one_or_many(prev_char, regex, text[1:]):
                return True
            # when we consume all the repetition, we compare the remaining text
            else:
                return compare(regex, text[1:])
        else:
            return False

# endregion

def compare_one(regex, text):
    """
    Compare two characters.
    """
    if len(regex) == 0:
        return True
    elif len(text) == 0:
        return False
    elif regex == ".":
        return True
    else:
        return regex == text

def compare(regex, text):
    """
    Compare a regex and text with the same length or almost considering the metacharacter
    """
    if len(regex) == 0:
        # if we consume regex and not the text, we fail
        return len(text) == 0
    elif regex == "$":
        return len(text) == 0
    elif len(text) == 0:
        return False
    else:
        if regex.startswith("\\"):
            if not compare_one(regex[1], text[0]):
                return False
            else:
                return compare(regex[2:], text[1:])
        else:
            if len(regex) >= 2 and regex[1] == "?":
                return check_zero_or_one(regex[0], regex[2:], text)
            if len(regex) >= 2 and regex[1] == "*":
                return check_zero_or_many(regex[0], regex[2:], text)
            if len(regex) >= 2 and regex[1] == "+":
                return check_one_or_many(regex[0], regex[2:], text)

            if not compare_one(regex[0], text[0]):
                return False
            else:
                return compare(regex[1:], text[1:])

def match_pattern(regex, text):
    """
    find any pattern of regex in text
    """
    if regex.startswith("^") and regex.endswith("$"):
        pattern = regex[1:-1]
        return compare(pattern, text)
    elif regex.startswith("^"):
        return compare(regex[1:], text[:len(regex)-1])
    elif regex.endswith("$"):
        index = len(regex) - 2 if "\\" in regex else len(regex) - 1
        return compare(regex, text[-index:])
    else:
        index = len(regex) - 1 if "\\" in regex else len(regex)
        for i in range(max(len(text)-index+1,1)):
            if compare(regex, text[i:i+index]):
                return True
        return False


if __name__ == '__main__':
    reg, arg = input().split("|")
    print(match_pattern(reg, arg))