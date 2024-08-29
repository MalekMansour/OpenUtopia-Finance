import matplotlib.pyplot as plt
import pandas as pd

class FinanceTool:
    def __init__(self):
        self.income_data = pd.DataFrame(columns=["Period", "Amount"])

    def add_income(self, period, amount):
        """Add income data for a specific period."""
        new_data = pd.DataFrame({"Period": [period], "Amount": [amount]})
        self.income_data = pd.concat([self.income_data, new_data], ignore_index=True)
        print(f"Added: {period} - ${amount}")

    def display_data(self):
        """Display the stored income data."""
        print(self.income_data)

    def plot_income(self):
        """Plot the income data as a bar chart."""
        plt.figure(figsize=(10, 6))
        plt.bar(self.income_data['Period'], self.income_data['Amount'], color='green')
        plt.xlabel('Period')
        plt.ylabel('Amount ($)')
        plt.title('Income Visualization')
        plt.grid(True)
        plt.show()

# Example usage
if __name__ == "__main__":
    tool = FinanceTool()

    # Example data input
    tool.add_income("January", 5000)
    tool.add_income("February", 5500)
    tool.add_income("March", 6000)
    tool.add_income("April", 6500)
    
    # Displaying data
    tool.display_data()

    # Plotting the income data
    tool.plot_income()

