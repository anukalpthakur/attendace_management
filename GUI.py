from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import os
import subprocess

class AttendanceApp(QtWidgets.QMainWindow):
    def __init__(self, user_role="user", username=""):
        super().__init__()
        self.user_role = user_role
        self.username = username
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Face Recognition Attendance System")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2C3E50;")  # ✅ Dark Background

        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        # ✅ Title Label (White Color)
        self.label = QtWidgets.QLabel(f"Welcome, {self.username}!", self)
        self.label.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        self.label.setStyleSheet("color: #ECF0F1;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.label)

        # ✅ Button Styling
        button_style = """
            QPushButton {
                background-color: #3498DB;
                color: white;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
                min-width: 300px;
                transition: 0.3s;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """

        logout_button_style = """
            QPushButton {
                background-color: #E74C3C; /* ✅ Red Logout Button */
                color: white;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
                min-width: 300px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """

        # ✅ Define Buttons
        self.buttons = [
            ("✅ Mark Attendance", f"F:/attendence/mark_attendence.py {self.username}"),
            ("📊 View Attendance List", f"F:/attendence/view_attendence_gui.py {self.user_role} {self.username}"),  # ✅ Pass Role & Username
        ]

        if self.user_role == "admin":
            self.buttons += [
                ("➕ Add Student", "F:/attendence/add_student_with_camera.py"),
                ("✏️ Update Record", "F:/attendence/update_record.py"),
                ("📷 Update Face", "F:/attendence/update_face.py"),
                ("🗑 Delete Record", "F:/attendence/delete_record.py"),
            ]

        self.buttons.append(("🚪 Logout", "exit"))  # ✅ Logout Button

        # ✅ Create Buttons
        for text, command in self.buttons:
            btn = QtWidgets.QPushButton(text, self)

            # ✅ Apply logout style only for "Logout" button
            if text == "🚪 Logout":
                btn.setStyleSheet(logout_button_style)
            else:
                btn.setStyleSheet(button_style)

            # ✅ Check if icon exists before setting it
            icon_path = f"icons/{text.lower().replace(' ', '_')}.png"
            if os.path.exists(icon_path):
                btn.setIcon(QtGui.QIcon(icon_path))  # ✅ Add icons if available

            if command == "exit":
                btn.clicked.connect(self.close)
            else:
                btn.clicked.connect(lambda checked, cmd=command: self.run_script(cmd))

            layout.addWidget(btn)

    def run_script(self, command):
        """✅ Ensure external scripts execute correctly"""
        try:
            script_path = command.split()[0]
            args = command.split()[1:]
            print(f"🚀 Running: {script_path} with args {args}")  # Debugging log
            subprocess.Popen([sys.executable, script_path] + args, shell=True)
        except Exception as e:
            print(f"❌ Error executing {command}: {e}")

if __name__ == "__main__":
    # ✅ Ensure Role & Username are passed correctly
    if len(sys.argv) < 3:
        print("⚠ Error: Missing required arguments (role & username).")
        sys.exit(1)

    role = sys.argv[1]
    username = sys.argv[2]

    print(f"🔍 Role: {role}, Username: {username}")  # Debugging log

    app = QtWidgets.QApplication(sys.argv)
    window = AttendanceApp(user_role=role, username=username)
    window.show()
    sys.exit(app.exec_())
