import tkinter as tk

def PricingPage(parent):
    frame = tk.Frame(parent, bg="#ffffff")
    
    tk.Label(frame, text="Pricing Overview", font=("Segoe UI", 20, "bold"), bg="#ffffff").pack(pady=20)
    tk.Label(frame, text="Welcome back!", bg="#ffffff").pack()

    return frame