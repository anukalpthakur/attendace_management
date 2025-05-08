import mysql.connector
import tkinter as tk
from tkinter import messagebox, simpledialog
import sys

def update_record():
    root = tk.Tk()
    root.withdraw()

    # ✅ Take Username from Command-Line Argument
    username = sys.argv[1] if len(sys.argv) > 1 else simpledialog.askstring("Update Record", "Enter Username to update:")

    if not username:
        messagebox.showwarning("Error", "⚠ Username is required!")
        return
    
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="FaceRecognitionDB"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT username, email, role, total_attendance FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not user:
            messagebox.showwarning("Error", "⚠ Username Not Found!")
            return
    except Exception as e:
        messagebox.showerror("Error", f"Database Error: {str(e)}")
        return
    
    edit_window = tk.Toplevel()
    edit_window.title("Update User Record")
    edit_window.geometry("400x400")

    labels = ["Username", "Email", "Role", "Total Attendance"]
    entries = {}
    original_values = list(user)  # Store original values for reset

    for idx, label in enumerate(labels):
        tk.Label(edit_window, text=label).grid(row=idx, column=0, padx=10, pady=5)
        entry = tk.Entry(edit_window)
        entry.insert(0, user[idx] if user[idx] is not None else "")  # ✅ Handle NULL values
        entry.grid(row=idx, column=1, padx=10, pady=5)
        entries[label] = entry

    # ✅ Prevent username editing (must remain unique)
    entries["Username"].config(state="disabled")

    # ✅ Prevent role editing if user is not admin
    if user[3] == "user":
        entries["Role"].config(state="disabled")

    def save_changes():
        updated_values = [entries[label].get() for label in labels[1:]]  # Exclude username
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="FaceRecognitionDB"
            )
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET  email=%s, role=%s, total_attendance=%s WHERE username=%s
            """, updated_values + [username])  # ✅ Don't update `username`
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "✅ User record updated successfully!")
            edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {str(e)}")

    def reset_fields():
        for idx, label in enumerate(labels[1:]):  # Exclude username
            entries[label].delete(0, tk.END)
            entries[label].insert(0, original_values[idx + 1] if original_values[idx + 1] is not None else "")

    save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
    save_button.grid(row=len(labels), column=0, pady=10)

    reset_button = tk.Button(edit_window, text="Reset", command=reset_fields)
    reset_button.grid(row=len(labels), column=1, pady=10)

    edit_window.mainloop()

if __name__ == "__main__":
    update_record()
