import tkinter as tk

def show_explanation(explanation):
    root = tk.Tk()
    root.title("Screen Analysis")
    root.geometry("800x600")  # Start with a larger window size
    root.resizable(True, True)  # Allow the window to be resizable
    
    # Create a frame to manage the layout
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)  # Make the frame expandable
    
    # Create a label with adjustable wraplength and justification
    label = tk.Label(frame, text=explanation, wraplength=frame.winfo_width(), justify="left")
    label.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)  # Make label fill the frame
    
    # Dynamically update wraplength when window is resized
    def update_wraplength(event):
        label.config(wraplength=event.width - 40)  # 40px padding (20px on each side)
    
    frame.bind("<Configure>", update_wraplength)  # Update wraplength on window resize
    
    root.mainloop()
