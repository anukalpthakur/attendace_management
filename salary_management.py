import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import pandas as pd

# 🎨 Modern Styling
BG_COLOR = "#2C3E50"
FG_COLOR = "#ECF0F1"
BTN_COLOR = "#3498DB"
BTN_HOVER = "#2980B9"

# 🔹 Connect to MySQL Database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="facerecognitiondb"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# 🔹 Fetch all salary records from the database
def fetch_salaries():
    conn = connect_db()
    if conn is None:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM salaries")
    salaries = cursor.fetchall()
    conn.close()
    return salaries

# 🔹 Insert a new salary record
def insert_salary(employee_id, salary_amount, bonus, deductions, net_salary):
    if not employee_id or not salary_amount:
        messagebox.showerror("Error", "Employee ID and Salary Amount are required!")
        return
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO salaries (employee_id, salary_amount, bonus, deductions, net_salary) VALUES (%s, %s, %s, %s, %s)",
        (employee_id, salary_amount, bonus, deductions, net_salary)
    )
    conn.commit()
    conn.close()
    populate_treeview(salary_tree)

# 🔹 Update an existing salary record
def update_salary(salary_id, employee_id, salary_amount, bonus, deductions, net_salary):
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE salaries SET employee_id=%s, salary_amount=%s, bonus=%s, deductions=%s, net_salary=%s WHERE id=%s",
        (employee_id, salary_amount, bonus, deductions, net_salary, salary_id)
    )
    conn.commit()
    conn.close()
    populate_treeview(salary_tree)

# 🔹 Delete salary record
def delete_salary(salary_id):
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this salary record?"):
        conn = connect_db()
        if conn is None:
            return
        cursor = conn.cursor()
        cursor.execute("DELETE FROM salaries WHERE id=%s", (salary_id,))
        conn.commit()
        conn.close()
        populate_treeview(salary_tree)

# 🔹 Populate Treeview with salary data
def populate_treeview(tree):
    for row in tree.get_children():
        tree.delete(row)
    salaries = fetch_salaries()
    for i, salary in enumerate(salaries):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        tree.insert("", "end", values=salary, tags=(tag,))

# 🔹 Export to Excel Function
def export_to_excel():
    try:
        # Fetching all the rows from the TreeView
        rows = salary_tree.get_children()
        data = []
        
        for row in rows:
            data.append(salary_tree.item(row)['values'])

        # Creating a DataFrame from the data
        df = pd.DataFrame(data, columns=["ID", "Employee ID", "Salary Amount", "Bonus", "Deductions", "Net Salary"])

        # File path for export
        file_path = "salary_data.xlsx"
        
        # Writing to Excel file
        df.to_excel(file_path, index=False, engine="openpyxl")

        messagebox.showinfo("Export Successful", f"Data has been exported to {file_path}")
    except Exception as e:
        messagebox.showerror("Export Error", f"An error occurred while exporting to Excel: {e}")

# 🌟 Main GUI
root = tk.Tk()  # This is where 'root' is defined
root.title("Salary Management System")
root.geometry("950x500")
root.configure(bg=BG_COLOR)

# ✅ Table Frame
frame = tk.Frame(root, bg=BG_COLOR)
frame.pack(pady=10, padx=10, fill="both", expand=True)

tree_frame = tk.Frame(frame)
tree_frame.pack(fill="both", expand=True)

tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side="right", fill="y")

salary_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set,
                           columns=("ID", "Employee ID", "Salary Amount", "Bonus", "Deductions", "Net Salary"),
                           show="headings")
tree_scroll.config(command=salary_tree.yview)

for col in salary_tree["columns"]:
    salary_tree.heading(col, text=col)
    salary_tree.column(col, anchor="center", width=120)

salary_tree.tag_configure("evenrow", background="#ECF0F1")
salary_tree.tag_configure("oddrow", background="#BDC3C7")
salary_tree.pack(fill="both", expand=True)

# Edit/Add Salary
def open_edit_window(salary=None):
    def save():
        salary_id = salary[0] if salary else None
        employee_id = entries["Employee ID"].get()
        salary_amount = entries["Salary Amount"].get()
        bonus = entries["Bonus"].get()
        deductions = entries["Deductions"].get()
        net_salary = entries["Net Salary"].get()

        if salary_id:
            update_salary(salary_id, employee_id, salary_amount, bonus, deductions, net_salary)
        else:
            insert_salary(employee_id, salary_amount, bonus, deductions, net_salary)
        edit_window.destroy()

    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Salary Record")
    edit_window.configure(bg=BG_COLOR)
    edit_window.geometry("300x350")

    fields = ["Employee ID", "Salary Amount", "Bonus", "Deductions", "Net Salary"]
    entries = {}

    for idx, field in enumerate(fields):
        tk.Label(edit_window, text=field, bg=BG_COLOR, fg=FG_COLOR).grid(row=idx, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(edit_window, bg="white", fg="black", width=25)
        entry.grid(row=idx, column=1, padx=10, pady=5)
        entries[field] = entry

    if salary:
        entries["Employee ID"].insert(0, salary[1])
        entries["Salary Amount"].insert(0, salary[2])
        entries["Bonus"].insert(0, salary[3])
        entries["Deductions"].insert(0, salary[4])
        entries["Net Salary"].insert(0, salary[5])

    tk.Button(edit_window, text="Save", command=save, bg=BTN_COLOR, fg="white").grid(row=len(fields), column=1, pady=10)

# Buttons for CRUD operations
button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=10)

add_btn = tk.Button(button_frame, text="Add Salary Record", command=lambda: open_edit_window())
add_btn.pack(side="left", padx=10)

edit_btn = tk.Button(button_frame, text="Edit Salary Record", command=lambda: open_edit_window(salary_tree.item(salary_tree.selection())["values"]) if salary_tree.selection() else None)
edit_btn.pack(side="left", padx=10)

delete_btn = tk.Button(button_frame, text="Delete Salary Record", command=lambda: delete_salary(salary_tree.item(salary_tree.selection())["values"][0]) if salary_tree.selection() else None)
delete_btn.pack(side="left", padx=10)

# Add Export to Excel Button
export_btn = tk.Button(root, text="Export to Excel", command=export_to_excel)
export_btn.pack(pady=10)

# Load salary data
populate_treeview(salary_tree)

# Run GUI
root.mainloop()
