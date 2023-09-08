import tkinter as tk
import csv
import mysql.connector
from tkinter import messagebox
import matplotlib.pyplot as plt
import openpyxl

expense_list = []
expense_analytics_list = []  # Declare as a global variable to access from functions


def add_expense():
    global expense_analytics_list
    global budget  # Declare budget as a global variable

    item = item_entry.get()
    amount = amount_entry.get()
    category = category_var.get()
    custom_category = custom_category_var.get()
    tags = tags_var.get().split(",") if tags_var.get() else []

    if item and amount and (category or custom_category):
        if category == "Custom":
            category = custom_category

        expense_amount = float(amount)
        
        # Check if the expense exceeds the budget
        if budget > 0 and sum(expense_analytics_list) + expense_amount > budget:
            messagebox.showwarning("Budget Exceeded", f"The expense will exceed the budget of ${budget:.2f}.")
            return
        
        expense = f"{item}: ${amount} ({category}) - Tags: {', '.join(tags)}"
        expense_list.append(expense)
        expense_analytics_list.append(expense_amount)
        expense_listbox.insert(tk.END, expense)
        item_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        category_var.set("")  # Reset the category selection
        custom_category_var.set("")  # Reset the custom category input
        tags_var.set("")  # Reset the tags input field
    else:
        messagebox.showwarning("Input Error", "Please enter item, amount, and select a category.")
def save_expenses():
    with open('expenses.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for expense in expense_list:
            item, rest = expense.split(": $")
            amount, rest = rest.split(" (")
            category, rest = rest.split(") - Tags: ")
            tags = rest.strip(")").split(", ")
            writer.writerow([item.strip(), amount.strip(), category.strip(), ', '.join(tags)])
            
def load_expenses():
    try:
        with open('expenses.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 4:  # Check if the row contains all four values
                    item, amount, category, tags = row
                    expense = f"{item}: ${amount} ({category}) - Tags: {tags}"
                    expense_list.append(expense)
                    expense_listbox.insert(tk.END, expense)
    except FileNotFoundError:
        return

def clear_expenses():
    expense_listbox.delete(0, tk.END)  # Clear the Listbox
    expense_list.clear()  # Clear the expense_list

def analyze_expenses():
    if not expense_list:
        messagebox.showinfo("Expense Analytics", "No expenses to analyze.")
        return

    category_totals = {}  # Create a dictionary to store category totals

    for expense in expense_list:
        category = expense.split(": $")[1].split(" (")[1].split(") - Tags: ")[0]
        amount = float(expense.split(": $")[1].split(" (")[0])
        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    total_expenses = sum(expense_analytics_list)
    average_expenses = total_expenses / len(expense_analytics_list)
    max_expense = max(expense_analytics_list)
    min_expense = min(expense_analytics_list)

    # Display analytics
    analytics_message = f"Total Expenses: ${total_expenses:.2f}\nAverage Expenses: ${average_expenses:.2f}\n" \
                        f"Maximum Expense: ${max_expense:.2f}\nMinimum Expense: ${min_expense:.2f}"
    
    for category, amount in category_totals.items():
        analytics_message += f"\nTotal {category} Expenses: ${amount:.2f}"

    messagebox.showinfo("Expense Analytics", analytics_message)
    
    # Create a pie chart based on category totals
    plt.figure(figsize=(8, 6))
    plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=140)
    plt.title("Expense Distribution by Category")
    plt.axis('equal')
    plt.show()

def convert_currency(amount, from_currency, to_currency):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ssvm",
            database="project"
        )
        cursor = conn.cursor()

        # Fetch exchange rates for the specified currencies
        print("Fetching exchange rate for", from_currency)
        cursor.execute("SELECT rate FROM exchange_rates WHERE currency = %s", (from_currency,))
        from_rate = cursor.fetchone()
        print("From Rate:", from_rate)

        print("Fetching exchange rate for", to_currency)
        cursor.execute("SELECT rate FROM exchange_rates WHERE currency = %s", (to_currency,))
        to_rate = cursor.fetchone()
        print("To Rate:", to_rate)

        # Close the database connection
        conn.close()

        # Convert rates to numeric format and calculate the converted amount
        if from_rate and to_rate:
            from_rate = float(from_rate[0])
            to_rate = float(to_rate[0])

            print("Calculating converted amount...")
            converted_amount = amount * (to_rate / from_rate)
            print("Converted Amount:", converted_amount)
            return converted_amount

    except Exception as e:
        print(f"Error during currency conversion: {e}")

    return None


def convert_and_display():
    # Calculate the total expense
    total_expense = sum(expense_analytics_list)

    # Get the selected currency for conversion
    to_currency = to_currency_var.get()

    # Convert the total expense to the desired currency
    converted_amount = convert_currency(total_expense, "USD", to_currency)

    if converted_amount is not None:
        # Display the converted amount in the Entry widget
        converted_amount_entry.delete(0, tk.END)  # Clear the previous value
        converted_amount_entry.insert(0, f"{converted_amount:.2f} {to_currency}")
    else:
        converted_amount_entry.delete(0, tk.END)  # Clear the previous value
        converted_amount_entry.insert(0, "Conversion Error")
  # Update with new value
def delete_save():
    with open('expenses.csv', 'w', newline='') as csvfile:
        pass

def toggle_dark_mode():
    if dark_mode_var.get():
        root.configure(bg="black")
        main_frame.configure(bg="black")
        title_label.config(fg="white", bg="sky blue")
        item_label.config(fg="white", bg="black")
        amount_label.config(fg="white", bg="black")
        category_label.config(fg="white", bg="black")
        tags_label.config(fg="white", bg="black")
        expense_listbox.config(bg="black", fg="white")
        custom_category_label.config(bg="black",fg="white")
        # Update other widgets' colors, fonts, etc. for dark mode
    else:
        root.configure(bg="white")
        main_frame.configure(bg="white")
        title_label.config(fg="black", bg="sky blue")
        item_label.config(fg="black", bg="white")
        amount_label.config(fg="black", bg="white")
        category_label.config(fg="black", bg="white")
        tags_label.config(fg="black", bg="white")
        expense_listbox.config(bg="white", fg="black")
        custom_category_label.config(bg="white",fg="black")
        # Update other widgets' colors, fonts, etc. for light mode

budget = None  # Initialize budget as 0
budget_entry = None 
budget_popup = None  # Initialize budget_popup as a global variable

def open_budget_popup():
    global budget_popup
    global budget_entry  # Declare budget_entry as a global variable

    budget_popup = tk.Toplevel(root)
    budget_popup.title("Set Budget")
    budget_popup.geometry("300x100")

    budget_entry = tk.Entry(budget_popup)
    budget_entry.pack(pady=10)

    set_budget_button = tk.Button(budget_popup, text="Set Budget", command=set_budget)
    set_budget_button.pack()

def set_budget():
    global budget
    try:
        budget = float(budget_entry.get())
        if budget == 0:
            budget_label.config(text=f"Budget: None")
        else:
            budget_label.config(text=f"Budget: ${budget:.2f}")
        budget_entry.delete(0, tk.END)
        budget_popup.destroy()  # Close the budget popup
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid budget amount.")

def clear_budget():
    global budget
    budget = None
    budget_label.config(text=f"Budget: None")
root = tk.Tk()
root.title("Expense Tracker")

# Calculate the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size to a percentage of the screen size (e.g., 80% of width and 80% of height)
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)

# Set the window size
root.geometry("400x770")

# Change the background color of the window to blue
root.configure(bg="white")

main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, rowspan=10, padx=10, pady=10)

title_label = tk.Label(main_frame, text="EXPENSE TRACKER", font=("Helvetica", 24, "bold"), fg="white", bg="sky blue")
title_label.grid(row=0, column=0, columnspan=3, pady=10)


# Create a frame to hold the input widgets
input_frame = tk.Frame(main_frame, bg="sky blue")
input_frame.grid(row=2, column=0, padx=10, pady=10)

custom_category_label = tk.Label(input_frame, text="Custom Category:", fg="white", bg="sky blue")
custom_category_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")

custom_category_var = tk.StringVar()
custom_category_entry = tk.Entry(input_frame, textvariable=custom_category_var)
custom_category_entry.grid(row=4, column=1, padx=5, pady=5)


item_label = tk.Label(input_frame, text="Item:", fg="white", bg="sky blue")
item_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

item_entry = tk.Entry(input_frame)
item_entry.grid(row=0, column=1, padx=5, pady=5)

budget_label = tk.Label(main_frame, text=f"Budget: None", font=("Helvetica", 14))
budget_label.grid(row=1, column=0, columnspan=5, padx=10, pady=5)

amount_label = tk.Label(input_frame, text="Amount:", fg="white", bg="sky blue")
amount_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

amount_entry = tk.Entry(input_frame)
amount_entry.grid(row=1, column=1, padx=5, pady=5)

category_label = tk.Label(input_frame, text="Category:", fg="white", bg="sky blue")
category_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

category_var = tk.StringVar()
category_choices = ["Expensive Purchase", "Medium Purchase", "Small Purchase"]
category_var.set(category_choices[0])  # Set default category
category_dropdown = tk.OptionMenu(input_frame, category_var, *category_choices)
category_dropdown.grid(row=2, column=1, padx=5, pady=5)

tags_label = tk.Label(input_frame, text="Tags (comma-separated):", fg="white", bg="sky blue")
tags_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")

tags_var = tk.StringVar()
tags_entry = tk.Entry(input_frame, textvariable=tags_var)
tags_entry.grid(row=3, column=1, padx=5, pady=5)

# Create a frame to hold the buttons
button_frame = tk.Frame(main_frame, bg="sky blue")
button_frame.grid(row=3, column=0, padx=10, pady=10)


add_button = tk.Button(button_frame, text="Add Expense", command=add_expense)
add_button.grid(row=0, column=0, padx=5, pady=5)

load_button = tk.Button(button_frame, text="Load Expenses", command=load_expenses)
load_button.grid(row=0, column=1, padx=5, pady=5)

save_button = tk.Button(button_frame, text="Save Expenses", command=save_expenses)
save_button.grid(row=0, column=2, padx=5, pady=5)

clear_button = tk.Button(button_frame, text="Clear All", command=clear_expenses)
clear_button.grid(row=1, column=0, padx=5, pady=5)

delete_expenses_button = tk.Button(button_frame, text="Delete Expenses", command=delete_save)
delete_expenses_button.grid(row=1, column=2, padx=5, pady=5)

expense_listbox = tk.Listbox(main_frame, width =40)
expense_listbox.grid(row=4, column=0, padx=10, pady=10)

expense_list = []

currency_frame = tk.Frame(main_frame)
currency_frame.grid(row=6, column=0, columnspan=5, padx=10, pady=10)

# Create buttons and labels for currency conversion
from_currency_label = tk.Label(currency_frame, text="From Currency: USD")
from_currency_label.grid(row=0, column=0, padx=5, pady=5)


to_currency_label = tk.Label(currency_frame, text="To Currency:")
to_currency_label.grid(row=0, column=2, padx=5, pady=5)
to_currency_var = tk.StringVar(value="EUR")
to_currency_menu = tk.OptionMenu(currency_frame, to_currency_var, "USD", "EUR", "INR", "GBP", "CNY")
to_currency_menu.grid(row=0, column=3, padx=5, pady=5)

convert_button = tk.Button(currency_frame, text="Convert", command=convert_and_display)
convert_button.grid(row=1, column=1, padx=5, pady=5)

budget_button = tk.Button(input_frame, text="Set Budget", command=open_budget_popup)
budget_button.grid(row=5, column=0, padx=10, pady=10)
clear_budget_button = tk.Button(input_frame, text="Clear Budget", command=clear_budget)
clear_budget_button.grid(row=5, column=1, padx=10, pady=10)
dark_mode_var = tk.BooleanVar()
dark_mode_checkbox = tk.Checkbutton(main_frame, text="Dark Mode", variable=dark_mode_var, command=toggle_dark_mode)
dark_mode_checkbox.grid(row=5, column=0, padx=10, pady=10)

converted_amount_label = tk.Label(main_frame, text="", font=("Helvetica", 14))
converted_amount_label.grid(row=1, column=0, columnspan=5, padx=10, pady=5)
converted_amount_entry = tk.Entry(currency_frame, font=("Helvetica", 14), width=8)
converted_amount_entry.grid(row=1, column=2, padx=5, pady=5)
analyze_button = tk.Button(button_frame, text="Analyze Expenses", command=analyze_expenses)
analyze_button.grid(row=1, column=1, padx=5, pady=5)
# Load previously saved expenses from the CSV file
load_expenses()

# Center the main frame within the window
root.update_idletasks()  # Apply any pending geometry changes
x_offset = (root.winfo_screenwidth() - root.winfo_width()) // 2
y_offset = (root.winfo_screenheight() - root.winfo_height()) // 2
root.geometry(f"+{x_offset}+{y_offset}")

# Add an Analyze button to perform expense analytics
root.mainloop() 
