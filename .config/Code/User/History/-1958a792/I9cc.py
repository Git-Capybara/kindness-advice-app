import tkinter as tk

# 1. Create the main window
window = tk.Tk()
window.title("Tkinter Test")
window.geometry("400x300")  # Set the window size

# 2. Create a canvas (a surface to draw on)
canvas = tk.Canvas(window, width=400, height=300, bg="white")
canvas.pack()

# 3. Draw a blue line from the top-left to the bottom-right of the canvas
# The coordinates are (x1, y1, x2, y2)
canvas.create_line(50, 50, 350, 250, fill="blue", width=3)

# 4. Start the main event loop to keep the window open
window.mainloop()