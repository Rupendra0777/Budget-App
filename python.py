class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        """Appends a deposit object to the ledger."""
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        """Appends a withdrawal if funds are available, returning True/False."""
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        """Returns the current balance of the budget category."""
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, category_instance):
        """Transfers funds from this category to another Category instance."""
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category_instance.name}")
            category_instance.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        """Returns True if amount can be covered by the balance, False otherwise."""
        return amount <= self.get_balance()

    def __str__(self):
        """Formats the ledger printout matching the strict challenge layout requirements."""
        title = f"{self.name.center(30, '*')}\n"
        items = ""
        for item in self.ledger:
            desc = item["description"][:23]
            amt = f"{item['amount']:.2f}"[:7]
            items += f"{desc:<23}{amt:>7}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    """Generates a bar chart string representing the percentage spent in each category."""
    # 1. Calculate total withdrawals per category and total overall spent
    spent_per_category = []
    total_spent = 0
    
    for category in categories:
        spent = sum(-item["amount"] for item in category.ledger if item["amount"] < 0)
        spent_per_category.append(spent)
        total_spent += spent

    # 2. Calculate percentages strictly rounded DOWN to the nearest 10
    percentages = []
    for spent in spent_per_category:
        if total_spent > 0:
            percentage = int((spent / total_spent) * 100 // 10) * 10
        else:
            percentage = 0
        percentages.append(percentage)

    # 3. Build the chart grid
    chart = "Percentage spent by category\n"
    for r in range(100, -1, -10):
        chart += f"{r:>3}| "
        for pct in percentages:
            chart += "o  " if pct >= r else "   "
        chart += "\n"

    # 4. Add the x-axis separator line (3 dashes per category + 1 final dash)
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # 5. Vertically format category names
    max_len = max(len(c.name) for c in categories)
    names = [c.name.ljust(max_len) for c in categories]

    for i in range(max_len):
        chart += "     "
        for name in names:
            chart += f"{name[i]}  "
        if i < max_len - 1:
            chart += "\n"

    return chart
