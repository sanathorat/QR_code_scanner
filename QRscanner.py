# QR code scanner 


import cv2
import numpy as np
from pyzbar.pyzbar import decode
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import webbrowser

class QRCodeScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Scanner")
        self.label = tk.Label(root, text="Click 'Scan QR Code' to start scanning")
        self.label.pack(pady=20)
        self.scan_button = tk.Button(root, text="Scan QR Code", command=self.scan_qr_code)
        self.scan_button.pack(pady=10)
        self.result_label = tk.Label(root, text="", wraplength=400)
        self.result_label.pack(pady=20)
        self.open_link_button = tk.Button(root, text="Open Link", command=self.open_link, state=tk.DISABLED)
        self.open_link_button.pack(pady=10)

    def scan_qr_code(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            for barcode in decode(frame):
                data = barcode.data.decode('utf-8')
                self.display_result(data)
                cap.release()
                cv2.destroyAllWindows()
                return
            cv2.imshow("QR Code Scanner", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def display_result(self, data):
        self.result_label.config(text=data)
        if data.startswith("http://") or data.startswith("https://"):
            self.open_link_button.config(state=tk.NORMAL)
            self.url = data
        else:
            self.open_link_button.config(state=tk.DISABLED)
            self.url = None

    def open_link(self):
        if self.url:
            webbrowser.open(self.url)
        else:
            messagebox.showerror("Error", "No valid URL to open")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeScannerApp(root)
    root.mainloop()