import mysql.connector
import sys
import tkinter as tk
from tkinter import ttk, messagebox

class ViewAttendanceApp:
    def __init__(self, root, role="user", username=None):  
        """Initialize Attendance Viewer GUI"""
        print(f"🔄 Initializing Attendance GUI... Role: {role}, Username: {username}")
        self.root = root
        self.role = role
        self.username = username

        self.root.title("View Attendance Records")
        self.root.geometry("900x500")
        self.root.configure(bg="#ECF0F1")

        title_label = tk.Label(self.root, text="Attendance Records", font=("Arial", 16, "bold"), bg="#ECF0F1")
        title_label.pack(pady=10)

        # ✅ Table to Show Records
        self.tree = ttk.Treeview(self.root, columns=("Username", "Total Attendance", "Last Attendance Time"), show='headings')
        self.tree.heading("Username", text="Username")
        self.tree.heading("Total Attendance", text="Total Attendance")
        self.tree.heading("Last Attendance Time", text="Last Attendance Time")

        self.tree.column("Username", width=200)
        self.tree.column("Total Attendance", width=150)
        self.tree.column("Last Attendance Time", width=200)

        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)

        self.load_attendance()

    def load_attendance(self):
        """Load Attendance Data from Database"""
        print("🔄 Connecting to Database...")  
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="FaceRecognitionDB"
            )
            cursor = conn.cursor()

            # ✅ Clear existing table data before inserting new data
            for row in self.tree.get_children():
                self.tree.delete(row)

            # ✅ If Admin: Show all records
            if self.role == "admin":
                print("🔹 Admin Role: Fetching All Attendance Records")
                cursor.execute("SELECT username, total_attendance, last_attendance_time FROM users")
            else:
                # ✅ If User: Show only their attendance record
                print(f"🔹 User Role: Fetching Attendance for {self.username}")
                cursor.execute("SELECT username, total_attendance, last_attendance_time FROM users WHERE username = %s", (self.username,))
            
            records = cursor.fetchall()
            print(f"✅ Retrieved {len(records)} records from database.")

            if not records:
                messagebox.showinfo("Info", "⚠ No attendance records found.")
            else:
                for record in records:
                    self.tree.insert("", tk.END, values=record)

            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"❌ {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting View Attendance GUI...")  

    # ✅ Ensure correct arguments are passed
    if len(sys.argv) < 3:
        print("⚠ Error: Missing required arguments (role & username).")
        sys.exit(1)

    role = sys.argv[1]
    username = sys.argv[2]

    root = tk.Tk()
    app = ViewAttendanceApp(root, role, username)
    root.mainloop()
