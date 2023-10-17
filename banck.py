class User:
    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.account_number = self.generate_account_number()
        self.transactions = []
        self.loan_taken = 0
        self.loan_count = 0

    def generate_account_number(self):
        # You can generate account numbers as per your requirements.
        # This is a simple example.
        import random
        return f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposited ${amount}")
        return f"Deposited ${amount} successfully."

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdrew ${amount}")
            return f"Withdrew ${amount} successfully."
        else:
            return "Withdrawal amount exceeded."

    def check_balance(self):
        return f"Available balance: ${self.balance}"

    def check_transaction_history(self):
        return self.transactions

    def take_loan(self, amount):
        if self.loan_count < 2:
            self.loan_count += 1
            self.loan_taken += amount
            self.balance += amount
            self.transactions.append(f"Took a loan of ${amount}")
            return f"Loan of ${amount} granted. Balance updated."
        else:
            return "You have reached the maximum loan limit."

    def transfer(self, recipient, amount):
        if amount <= self.balance:
            if recipient:
                self.balance -= amount
                recipient.balance += amount
                self.transactions.append(f"Transferred ${amount} to {recipient.name}")
                recipient.transactions.append(f"Received ${amount} from {self.name}")
                return f"Transferred ${amount} to {recipient.name} successfully."
            else:
                return "Account does not exist."
        else:
            return "Insufficient balance for the transfer. Bank is bankrupt."


class Admin:
    def __init__(self):
        self.users = []

    def create_account(self, name, email, address, account_type):
        user = User(name, email, address, account_type)
        self.users.append(user)
        return user

    def delete_account(self, user):
        self.users.remove(user)

    def view_accounts(self):
        return self.users

    def total_balance(self):
        total = sum(user.balance for user in self.users)
        return f"Total available balance in the bank: ${total}"

    def total_loan_amount(self):
        total_loan = sum(user.loan_taken for user in self.users)
        return f"Total loan amount in the bank: ${total_loan}"

    def toggle_loan_feature(self, status):
        User.loan_enabled = status


# Example Usage:

if __name__ == "__main__":
    admin = Admin()

    while True:
        print("\nOptions:")
        print("1. Create User Account")
        print("2. Delete User Account")
        print("3. View User Accounts")
        print("4. Total Bank Balance")
        print("5. Total Loan Amount")
        print("6. Toggle Loan Feature")
        print("7. User Operations")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            address = input("Enter your address: ")
            account_type = input("Enter account type (Savings/Current): ")
            user = admin.create_account(name, email, address, account_type)
            print(f"Account created with account number: {user.account_number}")

        elif choice == '2':
            for i, user in enumerate(admin.users):
                print(f"{i + 1}. {user.name} - {user.account_number}")
            if admin.users:
                delete_choice = int(input("Enter the number of the account to delete: ")) - 1
                if 0 <= delete_choice < len(admin.users):
                    admin.delete_account(admin.users[delete_choice])
                    print("Account deleted successfully.")
                else:
                    print("Invalid choice.")

        elif choice == '3':
            print("\nUser Accounts:")
            for i, user in enumerate(admin.users):
                print(f"{i + 1}. {user.name} - {user.account_number}")
            print("\n")

        elif choice == '4':
            print(admin.total_balance())

        elif choice == '5':
            print(admin.total_loan_amount())

        elif choice == '6':
            status = input("Enter 'on' to enable loan feature, 'off' to disable: ")
            admin.toggle_loan_feature(status.lower() == 'on')

        elif choice == '7':
            if not admin.users:
                print("No user accounts found.")
                continue
            account_number = input("Enter your account number: ")
            user = None
            for u in admin.users:
                if u.account_number == account_number:
                    user = u
                    break
            if not user:
                print("Account not found.")
                continue

            print(f"User: {user.name} - Account Number: {user.account_number}")
            while True:
                print("User Operations:")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Check Balance")
                print("4. Transaction History")
                print("5. Take Loan")
                print("6. Transfer Money")
                print("7. Back to Main Menu")

                user_choice = input("Enter your choice: ")

                if user_choice == '1':
                    amount = float(input("Enter the deposit amount: "))
                    print(user.deposit(amount))

                elif user_choice == '2':
                    amount = float(input("Enter the withdrawal amount: "))
                    print(user.withdraw(amount))

                elif user_choice == '3':
                    print(user.check_balance())

                elif user_choice == '4':
                    print("Transaction History:")
                    for transaction in user.check_transaction_history():
                        print(transaction)

                elif user_choice == '5':
                    if user.loan_enabled:
                        if user.loan_count < 2:
                            amount = float(input("Enter the loan amount: "))
                            print(user.take_loan(amount))
                        else:
                            print("You have reached the maximum loan limit.")
                    else:
                        print("Loan feature is currently disabled by the bank.")

                elif user_choice == '6':
                    recipient_account = input("Enter the recipient's account number: ")
                    amount = float(input("Enter the transfer amount: "))
                    recipient = None
                    for u in admin.users:
                        if u.account_number == recipient_account:
                            recipient = u
                            break
                    print(user.transfer(recipient, amount))

                elif user_choice == '7':
                    break

                else:
                    print("Invalid choice. Please select a valid")
