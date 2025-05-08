from PyQt5 import QtWidgets, QtGui, QtCore
import cv2
import mysql.connector
import os
import pickle
import face_recognition
import sys

class UpdateFaceWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Face")
        self.setGeometry(200, 200, 400, 250)
        self.setStyleSheet("background-color: #ECF0F1;")
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        
        self.label = QtWidgets.QLabel("Enter Username to Update Face:")
        self.label.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.label)
        
        self.student_id_input = QtWidgets.QLineEdit()
        self.student_id_input.setPlaceholderText("Username")
        layout.addWidget(self.student_id_input)
        
        self.update_btn = QtWidgets.QPushButton("Update Face")
        self.update_btn.setStyleSheet("background-color: #3498DB; color: white; padding: 10px; font-size: 14px;")
        self.update_btn.clicked.connect(self.update_face)
        layout.addWidget(self.update_btn)
        
        self.result_label = QtWidgets.QLabel("")
        layout.addWidget(self.result_label)
        
        self.setLayout(layout)
    
    def update_face(self):
        username = self.student_id_input.text().strip()
        
        if not username:
            self.result_label.setText("⚠ Username is required!")
            return
        
        # ✅ Connect to Database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="FaceRecognitionDB"
        )
        cursor = conn.cursor()
        
        # ✅ Check if user exists
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        student = cursor.fetchone()
        
        if not student:
            self.result_label.setText("⚠ Username Not Found!")
            cursor.close()
            conn.close()
            return
        
        # ✅ Open Webcam to Capture New Image
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)

        print("📷 Press 'SPACE' to capture a new image or 'ESC' to exit.")
        while True:
            success, img = cap.read()
            cv2.imshow("Update Face", img)
            key = cv2.waitKey(1)

            if key == 27:  # ESC key to exit
                cap.release()
                cv2.destroyAllWindows()
                return
            
            elif key == 32:  # SPACE key to capture
                cap.release()
                cv2.destroyAllWindows()
                
                # ✅ Save New Image
                image_folder = "Images"
                encoding_folder = "Encodings"
                os.makedirs(image_folder, exist_ok=True)
                os.makedirs(encoding_folder, exist_ok=True)
                
                image_path = f"{image_folder}/{username}.jpg"
                cv2.imwrite(image_path, img)
                
                # ✅ Generate New Face Encoding
                img_student = face_recognition.load_image_file(image_path)
                face_locations = face_recognition.face_locations(img_student)
                if face_locations:
                    encode = face_recognition.face_encodings(img_student, face_locations)[0]
                    encoding_path = f"{encoding_folder}/{username}.p"
                    with open(encoding_path, 'wb') as file:
                        pickle.dump(encode, file)
                    self.result_label.setText("✅ Face Updated Successfully!")
                else:
                    os.remove(image_path)
                    self.result_label.setText("⚠ No face detected. Please try again.")
                break
        
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UpdateFaceWindow()
    window.show()
    sys.exit(app.exec_())
