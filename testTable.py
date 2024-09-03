import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title("Table in Tkinter")

# Define data for the table (example data)
table_data = [
    ["Name", "Age", "City"],
    ["John", "25", "New York"],
    ["Alice", "30", "Los Angeles"],
    ["Bob", "22", "Chicago"],
    ["Eve", "28", "Seattle"]
]

# Create labels for headers
for col, header in enumerate(table_data[0]):
    label = tk.Label(root, text=header, relief=tk.RIDGE, width=15)
    label.grid(row=0, column=col)

# Create labels for data cells
for row in range(1, len(table_data)):
    for col in range(len(table_data[row])):
        label = tk.Label(root, text=table_data[row][col], relief=tk.RIDGE, width=15)
        label.grid(row=row, column=col)

# Run the application
root.mainloop()
