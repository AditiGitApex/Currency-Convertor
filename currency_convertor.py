import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import requests

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter System")
        self.api_key = "c36c1bc35400c1584478b426"  # Replace with your API key
        self.base_currency = "USD"
        self.exchange_rates = {}
        self.fetch_rates()
        self.create_widgets()

    def fetch_rates(self):
        try:
            url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/{self.base_currency}"
            response = requests.get(url)
            data = response.json()
            if data['result'] == 'success':
                self.exchange_rates = data['conversion_rates']
            else:
                messagebox.showerror("API Error", "Failed to fetch exchange rates.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch rates: {e}")

    def create_widgets(self):
        tk.Label(self.root, text="Currency Converter System", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=4, pady=10)
        tk.Label(self.root, text="From Currency (e.g., USD):").grid(row=1, column=0, pady=5)
        self.from_currency = tk.Entry(self.root)
        self.from_currency.grid(row=1, column=1, pady=5)
        tk.Label(self.root, text="To Currency (e.g., EUR):").grid(row=2, column=0, pady=5)
        self.to_currency = tk.Entry(self.root)
        self.to_currency.grid(row=2, column=1, pady=5)
        tk.Label(self.root, text="Amount:").grid(row=3, column=0, pady=5)
        self.amount = tk.Entry(self.root)
        self.amount.grid(row=3, column=1, pady=5)
        tk.Button(self.root, text="Convert", command=self.convert_currency).grid(row=4, column=0, pady=10)
        tk.Button(self.root, text="Plot Conversion Rate", command=self.plot_conversion_rate).grid(row=4, column=1, pady=10)
        tk.Button(self.root, text="Plot All Rates", command=self.plot_all_rates).grid(row=4, column=2, pady=10)
        tk.Button(self.root, text="Swap", command=self.swap_currencies).grid(row=4, column=3, pady=10)
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.result_label.grid(row=5, column=0, columnspan=4, pady=10)

    def convert_currency(self):
        from_curr = self.from_currency.get().upper().strip()
        to_curr = self.to_currency.get().upper().strip()
        amount = self.amount.get().strip()

        if not from_curr or not to_curr or not amount:
            messagebox.showerror("Missing Input", "Please fill in all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric amount.")
            return

        # Fetch rates if not already fetched for the base currency
        if from_curr != self.base_currency:
            try:
                url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/{from_curr}"
                response = requests.get(url)
                data = response.json()
                if data['result'] == 'success':
                    rates = data['conversion_rates']
                else:
                    messagebox.showerror("API Error", "Failed to fetch exchange rates.")
                    return
            except Exception as e:
                messagebox.showerror("Error", f"Could not fetch rates: {e}")
                return
        else:
            rates = self.exchange_rates

        if to_curr not in rates:
            messagebox.showerror("Invalid Currency", "Currency code not supported or missing exchange rate.")
            return

        converted_amount = amount * rates[to_curr]
        self.result_label.config(text=f"{amount:.2f} {from_curr} = {converted_amount:.2f} {to_curr}")

    def swap_currencies(self):
        from_curr = self.from_currency.get().strip()
        to_curr = self.to_currency.get().strip()
        self.from_currency.delete(0, tk.END)
        self.from_currency.insert(tk.END, to_curr)
        self.to_currency.delete(0, tk.END)
        self.to_currency.insert(tk.END, from_curr)

    def plot_conversion_rate(self):
        from_curr = self.from_currency.get().upper().strip()
        to_curr = self.to_currency.get().upper().strip()
        if not from_curr or not to_curr:
            messagebox.showerror("Missing Input", "Please fill in both currencies.")
            return
        # Fetch rates for plotting
        if from_curr != self.base_currency:
            url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/{from_curr}"
            response = requests.get(url)
            rates = response.json().get('conversion_rates', {})
        else:
            rates = self.exchange_rates
        if to_curr not in rates:
            messagebox.showerror("Invalid Currency", "Currency code not supported or missing exchange rate.")
            return
        amounts = np.linspace(1, 100, 100)
        converted_amounts = [amount * rates[to_curr] for amount in amounts]
        plt.figure(figsize=(10, 6))
        plt.plot(amounts, converted_amounts)
        plt.xlabel(f'Amount in {from_curr}')
        plt.ylabel(f'Amount in {to_curr}')
        plt.title(f'Conversion Rate from {from_curr} to {to_curr}')
        plt.grid(True)
        plt.show()

    def plot_all_rates(self):
        rates = self.exchange_rates
        plt.figure(figsize=(10, 6))
        plt.bar(rates.keys(), rates.values())
        plt.xlabel('Currency')
        plt.ylabel('Exchange Rate')
        plt.title(f'Exchange Rates from {self.base_currency}')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()
