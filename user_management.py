import os
import sys
import mysql.connector
import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import cv2
import face_recognition
import pickle
import numpy as np
from send_otp import send_otp  # ✅ OTP Module

import os
import face_recognition
import dlib

# Get the correct path of shape_predictor_68_face_landmarks.dat
MODEL_PATH = os.path.join(os.path.dirname(__file__), "shape_predictor_68_face_landmarks.dat")

# Load the model manually
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Model file not found: {MODEL_PATH}")

# Tell dlib to use the correct model file
face_recognition.face_detector = dlib.get_frontal_face_detector()
face_recognition.pose_predictor_68_point = dlib.shape_predictor(MODEL_PATH)

# ✅ Database Connection Helper
def get_db_connection():
    """Returns a MySQL connection."""
    return mysql.connector.connect(host="localhost", user="root", password="root", database="FaceRecognitionDB")

class UserManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 User Management")
        self.root.geometry("400x500")
        self.root.config(bg="#f0f0f0")

        self.initUI()

    def initUI(self):
        """✅ GUI Design Improvements"""
        frame = tk.Frame(self.root, bg="white", padx=20, pady=20, relief="ridge", bd=2)
        frame.pack(pady=20)

        tk.Label(frame, text="📷 Face Recognition System", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        tk.Label(frame, text="👤 Username:", bg="white", font=("Arial", 11)).pack()
        self.entry_username = tk.Entry(frame, font=("Arial", 11), width=25)
        self.entry_username.pack(pady=5)

        tk.Label(frame, text="🔑 Password:", bg="white", font=("Arial", 11)).pack()
        self.entry_password = tk.Entry(frame, show="*", font=("Arial", 11), width=25)
        self.entry_password.pack(pady=5)

        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="🔑 Login", command=self.login, width=20, bg="#28a745", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, pady=5)
        tk.Button(btn_frame, text="📷 Face Login", command=self.login_with_face, width=20, bg="#007bff", fg="white", font=("Arial", 10, "bold")).grid(row=1, column=0, pady=5)
        tk.Button(btn_frame, text="🆕 Register", command=self.create_user, width=20, bg="#ffc107", fg="black", font=("Arial", 10, "bold")).grid(row=2, column=0, pady=5)
        tk.Button(btn_frame, text="🔄 Reset Password", command=self.reset_password, width=20, bg="#dc3545", fg="white", font=("Arial", 10, "bold")).grid(row=3, column=0, pady=5)
        # ✅ Digital Signature at Bottom
        tk.Label(self.root, text="Managed & Developed by Thakur & Co.", font=("Arial", 9, "italic"), bg="#f0f0f0", fg="black").pack(pady=5)
        tk.Label(self.root, text="📧 Email: 23391091@geu.ac.in | 📸 Insta: @thakur_coding", font=("Arial", 9, "italic"), bg="#f0f0f0", fg="black").pack()

    def login(self):
        """✅ Login using username & password"""
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showwarning("⚠ Error", "Username and password are required!")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT username, role FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                username, role = user
                self.root.destroy()
                subprocess.Popen(["python", "F:/attendence/GUI.py", role, username])
            else:
                messagebox.showerror("❌ Error", "Invalid Username or Password!")
        except Exception as e:
            messagebox.showerror("❌ Database Error", f"{str(e)}")

    def login_with_face(self):
        """✅ Face Recognition Login"""
        encoding_folder = "Encodings"
        if not os.path.exists(encoding_folder):
            messagebox.showerror("Error", "No stored face encodings found!")
            return

        known_encodings, student_usernames = [], []
        for filename in os.listdir(encoding_folder):
            if filename.endswith(".p"):
                username = filename.split(".")[0]
                with open(os.path.join(encoding_folder, filename), 'rb') as file:
                    known_encodings.append(pickle.load(file))
                student_usernames.append(username)

        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)
        matched_username = None

        while True:
            success, img = cap.read()
            if not success:
                messagebox.showerror("❌ Error", "Failed to access the camera!")
                break

            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            faces = face_recognition.face_locations(imgS)
            encodes = face_recognition.face_encodings(imgS, faces)

            for encodeFace in encodes:
                matches = face_recognition.compare_faces(known_encodings, encodeFace)
                faceDis = face_recognition.face_distance(known_encodings, encodeFace)
                matchIndex = np.argmin(faceDis) if len(faceDis) > 0 else None

                if matchIndex is not None and matches[matchIndex]:
                    matched_username = student_usernames[matchIndex]
                    break

            cv2.imshow("Face Login", img)
            if matched_username or (cv2.waitKey(1) & 0xFF == ord('q')):
                break

        cap.release()
        cv2.destroyAllWindows()

        if matched_username:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT role FROM users WHERE username = %s", (matched_username,))
                user_role = cursor.fetchone()
                cursor.close()
                conn.close()

                if user_role:
                    role = user_role[0]
                    self.root.destroy()
                    subprocess.Popen(["python", "F:/attendence/GUI.py", role, matched_username])
                else:
                    messagebox.showerror("❌ Error", "User role not found!")
            except Exception as e:
                messagebox.showerror("❌ Error", f"Database Error: {str(e)}")
        else:
            messagebox.showerror("❌ Error", "Face Not Recognized!")

    def create_user(self):
        """✅ Create a new user with OTP verification and Face Capture"""
        new_username = simpledialog.askstring("Create User", "Enter New Username:")
        new_password = simpledialog.askstring("Create User", "Enter New Password:")
        email = simpledialog.askstring("Create User", "Enter Email:")

        if not new_username or not new_password or not email:
            return  

        sent_otp = send_otp(email)
        entered_otp = simpledialog.askstring("OTP Verification", "Enter the OTP sent to your email:")
        if entered_otp != sent_otp:
            return  
        encoding_folder = "Encodings"
        os.makedirs(encoding_folder, exist_ok=True)

        encodeListKnown = []
        stored_usernames = []

        for filename in os.listdir(encoding_folder):
            if filename.endswith(".p"):
                stored_username = filename.split(".")[0]
                with open(os.path.join(encoding_folder, filename), 'rb') as file:
                    encode = pickle.load(file)
                encodeListKnown.append(encode)
                stored_usernames.append(stored_username)

        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)

        messagebox.showinfo("📷 Face Capture", "Align your face with the camera.")

        while True:
            ret, frame = cap.read()
            cv2.imshow("Register Face", frame)
            key = cv2.waitKey(1)

            if key == 32:  
                cap.release()
                cv2.destroyAllWindows()

                image_folder = "Images"
                os.makedirs(image_folder, exist_ok=True)
                image_path = f"{image_folder}/{new_username}.jpg"
                cv2.imwrite(image_path, frame)

                img_new = face_recognition.load_image_file(image_path)
                face_locations = face_recognition.face_locations(img_new)

                if not face_locations:
                    os.remove(image_path)
                    messagebox.showwarning("⚠ Error", "No face detected. Try again!")
                    return

                new_encoding = face_recognition.face_encodings(img_new, face_locations)[0]

                for idx, stored_encoding in enumerate(encodeListKnown):
                    match = face_recognition.compare_faces([stored_encoding], new_encoding, tolerance=0.5)
                    if match[0]:
                        os.remove(image_path)  
                        messagebox.showinfo("⚠ Duplicate Face", f"This face is already registered with {stored_usernames[idx]}.")
                        return

                encoding_path = f"{encoding_folder}/{new_username}.p"
                with open(encoding_path, 'wb') as file:
                    pickle.dump(new_encoding, file)

                try:
                    conn = mysql.connector.connect(host="localhost", user="root", password="root", database="FaceRecognitionDB")
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, 'user')", 
                                (new_username, new_password, email))
                    conn.commit()
                    cursor.close()
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("❌ Error", f"Database Error: {str(err)}")
                return


    def reset_password(self):
        """✅ Password Reset using OTP"""
        username = simpledialog.askstring("Reset Password", "Enter Your Username:")
        if not username:
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if not user:
                messagebox.showwarning("⚠ Error", "Username Not Found!")
                return

            email = user[0]
            sent_otp = send_otp(email)
            entered_otp = simpledialog.askstring("OTP Verification", "Enter the OTP sent to your email:")
            if entered_otp != sent_otp:
                return  

            new_password = simpledialog.askstring("Reset Password", "Enter New Password:")
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("✅ Success", "Password Reset Successfully!")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Database Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UserManagementApp(root)
    root.mainloop()
