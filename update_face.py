import cv2
import mysql.connector
import os
import pickle
import face_recognition
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog

# ✅ Ensure Username is Provided
if len(sys.argv) != 2:
    root = tk.Tk()
    root.withdraw()
    username = simpledialog.askstring("Update Face", "Enter your Username:")
    if not username:
        print("⚠ Error: Username Required!")
        messagebox.showwarning("Error", "⚠ Username Required!")
        sys.exit(1)
else:
    username = sys.argv[1]

# ✅ Connect to MySQL
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

    if not user:
        print("⚠ Username Not Found!")
        messagebox.showwarning("Error", "⚠ Username Not Found in Database!")
        sys.exit(1)
except Exception as e:
    print(f"❌ Database Connection Error: {str(e)}")
    messagebox.showerror("Database Error", f"❌ {str(e)}")
    sys.exit(1)

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
        sys.exit(0)

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
        img_user = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(img_user)

        if face_locations:
            encode = face_recognition.face_encodings(img_user, face_locations)[0]
            encoding_path = f"{encoding_folder}/{username}.p"
            with open(encoding_path, 'wb') as file:
                pickle.dump(encode, file)
            
            print("✅ Face Updated Successfully!")
            messagebox.showinfo("Success", "✅ Face Updated Successfully!")
        else:
            os.remove(image_path)
            print("⚠ No face detected. Please try again.")
            messagebox.showwarning("Error", "⚠ No face detected. Please try again.")
        break

cursor.close()
conn.close()
