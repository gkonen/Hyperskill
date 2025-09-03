import random

nb_friends = int(input("Enter the number of friends joining (including you):\n"))
if nb_friends <= 0:
    print("No one is joining for the party")
else:
    friends = [input() for _ in range(nb_friends)]
    total_bill = int(input("Enter the total bill value:\n "))
    bill = dict.fromkeys(friends, round(total_bill / nb_friends, 2))

    lucky_feature = input("Do you want to use the \"Who is lucky?\" feature? Write Yes/No:\n") == "Yes"
    if lucky_feature:
        lucky_friend = random.choice(friends)
        print(f"{lucky_friend} is the lucky one!")
        bill = bill.fromkeys(friends, round(total_bill / (nb_friends - 1), 2))
        bill[lucky_friend] = 0
    else:
        print("No one is going to be lucky")
    print(bill)