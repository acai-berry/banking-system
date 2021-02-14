import random
import database


class Bank:
    def __init__(self):
        self.logged_in = False
        self.status = ''
        self.connection = database.connect()
        self.table = database.create_table(self.connection)

    def menu(self):
        while not self.logged_in and self.status != 'exit':
            print('1. Create an account \n 2. Log into account \n 0. Exit')
            choice = input()
            if choice == '1':
                self.create_account()
            elif choice == '2':
                self.login()
            elif choice == '0':
                self.exit()
                break
            else:
                print('Incorrect input, try again.')

    def account_menu(self, card_no):
        while self.logged_in:
            print('1. Balance \n 2. Add income \n 3. Do transfer \n 4. Close account \n 5. Log out \n 0.Exit')
            choice = input()
            if choice == '1':
                balance = database.show_balance(self.connection, card_no)[0]
                print(f'Balance: {balance}')
            elif choice == '2':
                income = int(input('Enter income:'))
                self.add_money_to_account(income, card_no)
                print('Income was added!')
            elif choice == '3':
                self.transfer(card_no)
            elif choice == '4':
                database.delete_account(self.connection, card_no)
                self.connection.commit()
                print('The account has been closed!')
            elif choice == '5':
                self.logged_in = False
                print('You have successfully logged out!')
            elif choice == '0':
                self.exit()
                break
            else:
                print('Incorrect input, try again.')

    def add_money_to_account(self, money, account):
        balance = database.show_balance(self.connection, account)[0]
        new_balance = balance + money
        database.change_balance(self.connection, new_balance, account)
        self.connection.commit()

    def deduct_money_from_account(self, money, account):
        balance = database.show_balance(self.connection, account)[0]
        new_balance = balance - money
        database.change_balance(self.connection, new_balance, account)
        self.connection.commit()

    def string_to_list_int(self, string1):
        new_list = []
        for ele in string1:
            new_list.append(int(ele))
        return new_list

    def create_card_number(self):
        card_number = "400000"
        while len(card_number) < 15:
            digit = random.randint(0, 9)
            card_number += str(digit)
        sum1 = self.sum_luhn_alg(card_number, False)
        if sum1 % 10 == 0:
            last_digit = 0
        else:
            last_digit = 10 - (sum1 % 10)
        final_card_number = card_number + str(last_digit)
        return final_card_number


    def sum_luhn_alg(self, card_number, drop_last_digit):
        list_card_nb = self.string_to_list_int(card_number)
        last_digit = 0
        if drop_last_digit:
            last_digit = list_card_nb[-1]
            list_card_nb = list_card_nb[:-1]
        digits_step1 = []
        for n in range(0, len(list_card_nb)):
            if n % 2 == 0:
                list_card_nb[n] *= 2
            digits_step1.append(list_card_nb[n])
        digits_step2 = []
        for digit in digits_step1:
            if digit > 9:
                digit -= 9
            digits_step2.append(digit)
        sum1 = sum(digits_step2) + last_digit
        return sum1

    def pass_luhn_alg(self, card_number):
        if self.sum_luhn_alg(card_number, True) % 10 == 0:
            return True
        else:
            return False

    def create_pin(self):
        pin = ''
        while len(pin) < 4:
            digit = random.randint(0, 9)
            pin += str(digit)
        return pin

    def create_account(self):
        card_number = self.create_card_number()
        pin = self.create_pin()
        database.add_card(self.connection, card_number, pin)
        self.connection.commit()
        print(f'Your card has been created\nYour card number:\n{card_number}\nYour card PIN:\n{pin}\n')

    def login(self):
        print('Enter your card number:')
        given_card = input()
        print('Enter your PIN:')
        given_pin = input()
        result = database.select_card_pin(self.connection, given_card, given_pin)
        if result:
            print("You have successfully logged in")
            self.logged_in = True
            self.account_menu(given_card)
        else:
            print('Wrong card number or pin!')

    def exit(self):
        print("Bye!")
        self.status = 'exit'

    def transfer(self, card_no):
        given_card = input("Enter card number: ")
        if self.pass_luhn_alg(given_card):
            if database.select_card(self.connection, given_card):
                transfer = int(input("Enter how much money you want to transfer:"))
                balance = int(database.show_balance(self.connection, card_no)[0])
                if transfer > balance:
                    print("Not enough money!")
                else:
                    self.add_money_to_account(transfer, given_card)
                    self.deduct_money_from_account(transfer, card_no)
                    self.connection.commit()
                    print("Success!")
            else:
                print("Such a card does not exist.")
        else:
            print("Probably you made a mistake in the card number. Please try again!")


bank = Bank()
bank.menu()
