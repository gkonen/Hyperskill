import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str)  # annuity or diff
parser.add_argument("--payment", type=float)  # Annuity Payment "A"
parser.add_argument("--principal", type=float)  # Loan principal "P"
parser.add_argument("--periods", type=int)  # Periods "n"
parser.add_argument("--interest", type=float)  # Interest "i"

args = parser.parse_args()

#  Test mandatory values
if args.type is None or args.interest is None :
    print("Incorrect parameters.")

else :
    t = args.type
    a = args.payment
    p = args.principal
    n = args.periods
    i = args.interest / (100*12)

    if [a,p,t].count(None) > 1:
        print("Incorrect parameters.")

    else :
        # compute the case differential
        if t == "diff":
            if a is not None:
                print("Incorrect parameters.")

            if p > 0 and n > 0 and i > 0:
                total_payment = 0
                for m in range(1,n+1):
                    d_m = math.ceil( (p/n) + i * ( p - ( p*(m-1)/n ) ) )
                    total_payment += d_m
                    print(f"Month {m}: payment is {d_m}")
                print(f"\nOverpayment = {int(total_payment-p)}")

            else :
                print("Incorrect parameters.")

        # All possibilities for the annuity
        elif t == "annuity":
            if i is None:
                print("Incorrect parameters.")
            else :
                if a is None:
                    if p > 0 and n > 0 and i > 0:
                        a = p * ((i * ((1 + i) ** n)) / ((1 + i) ** n - 1))
                        print(f"Your annuity payment = {math.ceil(a)}!")
                        total_payment = n * math.ceil(a)
                        print(f"\nOverpayment = {int(total_payment - p)}")
                    else :
                        print("Incorrect parameters.")

                elif p is None:
                    if a > 0 and n > 0 and i > 0:
                        p = a / (i * (1 + i) ** n / ((1 + i) ** n - 1))
                        print(f"Your loan principal = {p}!")
                        total_payment = n * a
                        print(f"\nOverpayment = {int(total_payment - p)}")
                    else :
                        print("Incorrect parameters.")

                elif n is None:
                    if p > 0 and a > 0 and i > 0:
                        n = math.ceil(math.log(a / (a - i * p), 1 + i))
                        if n < 12:
                            print(f"It will take {n} months to repay this loan!")
                        elif n % 12 == 0:
                            print(f"It will take {n // 12} years to repay this loan!")
                        else:
                            print(f"It will take {n // 12} years and {n % 12} months to repay this loan!")
                        total_payment = n * a
                        print(f"\nOverpayment = {int(total_payment - p)}")
                    else:
                        print("Incorrect parameters.")

        else :
            print("Incorrect parameters.")
