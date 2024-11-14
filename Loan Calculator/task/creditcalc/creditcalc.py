import sys
import math
import argparse

def calculate_annuity_payment(principal, interest, periods):
    i = interest / 12 / 100
    payment = principal * (i * math.pow(1 + i, periods)) / (math.pow(1 + i, periods) - 1)
    return math.ceil(payment)

def calculate_differentiated_payments(principal, periods, interest):
    i = interest / 12 / 100
    payments = []
    for m in range(1, periods + 1):
        payment = (principal / periods) + i * (principal - (principal * (m - 1) / periods))
        payments.append(math.ceil(payment))
    return payments

def calculate_principal(payment, periods, interest):
    i = interest / 12 / 100
    principal = payment / ((i * math.pow(1 + i, periods)) / (math.pow(1 + i, periods) - 1))
    return math.floor(principal)

def calculate_periods(principal, payment, interest):
    i = interest / 12 / 100
    periods = math.ceil(math.log(payment / (payment - i * principal), 1 + i))
    return periods

def calculate_overpayment(total_paid, principal):
    return total_paid - principal

def validate_parameters(args):
    if args.type not in ["annuity", "diff"]:
        return False
    if args.type == "diff" and args.payment:
        return False
    if not args.interest:
        return False
    if any(val is not None and val < 0 for val in [args.principal, args.payment, args.periods, args.interest]):
        return False
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, help="Type of payment: 'annuity' or 'diff'")
    parser.add_argument("--principal", type=int, help="The loan principal")
    parser.add_argument("--periods", type=int, help="The number of periods")
    parser.add_argument("--interest", type=float, help="The loan interest")
    parser.add_argument("--payment", type=int, help="The monthly payment amount")

    args = parser.parse_args()

    if not validate_parameters(args) or len([arg for arg in vars(args).values() if arg is not None]) < 4:
        print("Incorrect parameters")
        return

    if args.type == "diff":
        if args.principal and args.periods and args.interest:
            payments = calculate_differentiated_payments(args.principal, args.periods, args.interest)
            for month, payment in enumerate(payments, start=1):
                print(f"Month {month}: payment is {payment}")
            total_payment = sum(payments)
            overpayment = calculate_overpayment(total_payment, args.principal)
            print(f"Overpayment = {overpayment}")
        else:
            print("Incorrect parameters")

    elif args.type == "annuity":
        if args.principal and args.periods and args.interest:
            payment = calculate_annuity_payment(args.principal, args.interest, args.periods)
            total_payment = payment * args.periods
            overpayment = calculate_overpayment(total_payment, args.principal)
            print(f"Your annuity payment = {payment}!")
            print(f"Overpayment = {overpayment}")

        elif args.payment and args.periods and args.interest:
            principal = calculate_principal(args.payment, args.periods, args.interest)
            total_payment = args.payment * args.periods
            overpayment = calculate_overpayment(total_payment, principal)
            print(f"Your loan principal = {principal}!")
            print(f"Overpayment = {overpayment}")

        elif args.principal and args.payment and args.interest:
            periods = calculate_periods(args.principal, args.payment, args.interest)
            years = periods // 12
            months = periods % 12
            if years > 0:
                print(f"It will take {years} years", end="")
                if months > 0:
                    print(f" and {months} months", end="")
            else:
                print(f"It will take {months} months", end="")
            print(" to repay this loan!")
            total_payment = args.payment * periods
            overpayment = calculate_overpayment(total_payment, args.principal)
            print(f"Overpayment = {overpayment}")
        else:
            print("Incorrect parameters")

if __name__ == "__main__":
    main()
