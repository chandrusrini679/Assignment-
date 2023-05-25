
class User:
    def __init__(self, name):
        self.name = name
        self.expenses = []
        self.payments = []

    def add_expense(self, description, amount, paid_by):
        self.expenses.append({'description': description, 'amount': amount, 'paid_by': paid_by})

    def add_payment(self, amount, paid_to):
        self.payments.append({'amount': amount, 'paid_to': paid_to})


class ExpenseTracker:
    def __init__(self):
        self.users = []

    def create_user(self, name):
        user = User(name)
        self.users.append(user)

    def get_user_by_name(self, name):
        for user in self.users:
            if user.name == name:
                return user
        return None

    def add_expense(self, description, amount, paid_by, shared_with):
        expense_paid_by = self.get_user_by_name(paid_by)
        if expense_paid_by is not None:
            expense_paid_by.add_expense(description, amount, paid_by)
            for user in shared_with:
                user_obj = self.get_user_by_name(user)
                if user_obj is not None:
                    user_obj.add_expense(description, amount / len(shared_with), paid_by)

    def add_payment(self, amount, paid_by, paid_to):
        user_paying = self.get_user_by_name(paid_by)
        user_receiving = self.get_user_by_name(paid_to)
        if user_paying is not None and user_receiving is not None:
            user_paying.add_payment(amount, paid_to)
            user_receiving.add_payment(-amount, paid_by)

    def get_total_expenses(self):
        total_expenses = 0
        for user in self.users:
            for expense in user.expenses:
                total_expenses += expense['amount']
        return total_expenses

    def get_total_payments(self):
        total_payments = 0
        for user in self.users:
            for payment in user.payments:
                total_payments += payment['amount']
        return total_payments

    def settle_expenses(self):
        total_expenses = self.get_total_expenses()
        total_payments = self.get_total_payments()

        if total_expenses == total_payments:
            print("All expenses are settled.")
        elif total_expenses > total_payments:
            print("Some expenses are not settled. Remaining amount: ", total_expenses - total_payments)
        else:
            print("Some users have overpaid. Remaining amount: ", total_payments - total_expenses)


tracker = ExpenseTracker()

tracker.create_user('A')
tracker.create_user('B')
tracker.create_user('C')
tracker.create_user('D')
tracker.create_user('E')

tracker.add_expense('Accommodation', 200, 'B', ['A', 'B', 'C'])
tracker.add_expense('Food', 150, 'A', ['A', 'B', 'C'])
tracker.add_expense('Food', 100, 'E', ['D', 'E'])

tracker.add_payment(300, 'A', 'C')
tracker.add_payment(100, 'E', 'D')

tracker.settle_expenses()
