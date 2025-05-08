from PyQt5 import QtWidgets, QtGui, QtCore
import mysql.connector
import sys

class UpdateRecordWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update User Record")
        self.setGeometry(200, 200, 400, 300)
        self.setStyleSheet("background-color: #ECF0F1;")
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("Enter Username to Update:")
        self.label.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.label)

        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.new_name_input = QtWidgets.QLineEdit()
        self.new_name_input.setPlaceholderText("New Name")
        layout.addWidget(self.new_name_input)

        self.new_email_input = QtWidgets.QLineEdit()
        self.new_email_input.setPlaceholderText("New Email")
        layout.addWidget(self.new_email_input)

        self.new_role_input = QtWidgets.QComboBox()
        self.new_role_input.addItems(["user", "admin"])
        layout.addWidget(self.new_role_input)

        self.update_btn = QtWidgets.QPushButton("Update Record")
        self.update_btn.setStyleSheet("background-color: #3498DB; color: white; padding: 10px; font-size: 14px;")
        self.update_btn.clicked.connect(self.update_record)
        layout.addWidget(self.update_btn)

        self.result_label = QtWidgets.QLabel("")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def update_record(self):
        username = self.username_input.text()
        new_name = self.new_name_input.text()
        new_email = self.new_email_input.text()
        new_role = self.new_role_input.currentText()

        if not username or not new_name or not new_email:
            self.result_label.setText("⚠ All fields are required!")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="FaceRecognitionDB"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                cursor.execute("""
                    UPDATE users 
                    SET name = %s, email = %s, role = %s 
                    WHERE username = %s
                """, (new_name, new_email, new_role, username))
                conn.commit()
                self.result_label.setText("✅ Record Updated Successfully!")
            else:
                self.result_label.setText("⚠ Username Not Found!")

            cursor.close()
            conn.close()
        except Exception as e:
            self.result_label.setText(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UpdateRecordWindow()
    window.show()
    sys.exit(app.exec_())
