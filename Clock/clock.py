import tkinter as tk
import time

root = tk.Tk()
root.title("Gradient Digital Clock")

canvas_width = 700
canvas_height = 400

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, highlightthickness=0)
canvas.pack(fill="both", expand=True)

def draw_gradient(c1="#9A6BFF", c2="#E48AFF"):
    for i in range(canvas_height):
        r1, g1, b1 = root.winfo_rgb(c1)
        r2, g2, b2 = root.winfo_rgb(c2)
        r = int(r1 + (r2 - r1) * i / canvas_height) // 256
        g = int(g1 + (g2 - g1) * i / canvas_height) // 256
        b = int(b1 + (b2 - b1) * i / canvas_height) // 256
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, canvas_width, i, fill=color)

draw_gradient()

time_text = canvas.create_text(canvas_width//2, 130, text="", font=("Helvetica", 80, "bold"), fill="black")
date_text = canvas.create_text(canvas_width//2, 230, text="", font=("Helvetica", 22), fill="black")

colon_visible = True
alarm_time = None
alarm_triggered = False

def show_alarm_popup(time_str):
    popup = tk.Toplevel(root)
    popup.title("ALARM!")
    popup.geometry("400x200+500+300")
    popup.configure(bg="#FFD700")
    popup.grab_set()

    label = tk.Label(popup, text=f"⏰ Alarm for {time_str}", font=("Helvetica", 28, "bold"), bg="#FFD700", fg="black")
    label.pack(pady=40)

    btn = tk.Button(popup, text="Dismiss", font=("Helvetica", 16), command=popup.destroy)
    btn.pack()

def update():
    global colon_visible, alarm_triggered

    h = time.strftime("%I")
    m = time.strftime("%M")
    s = time.strftime("%S")
    ampm = time.strftime("%p")

    colon_visible = not colon_visible

    display_time = f"{h}:{m}:{s} {ampm}"
    canvas.itemconfig(time_text, text=display_time)
    canvas.itemconfig(date_text, text=time.strftime("%A, %d %B %Y"))

    current_time = f"{h}:{m} {ampm}"
    if alarm_time and current_time == alarm_time and not alarm_triggered:
        alarm_triggered = True
        show_alarm_popup(alarm_time)

    root.after(500, update)

def set_alarm():
    global alarm_time, alarm_triggered
    user_input = alarm_entry.get().strip()
    if time_format_valid(user_input):
        alarm_time = user_input
        alarm_label.config(text=f"Alarm set for {alarm_time}")
        alarm_triggered = False
    else:
        tk.messagebox.showerror("Invalid Time", "Use format HH:MM AM/PM")

def clear_alarm():
    global alarm_time, alarm_triggered
    alarm_time = None
    alarm_triggered = False
    alarm_label.config(text="No alarm set")
    alarm_entry.delete(0, tk.END)

def time_format_valid(t):
    try:
        time.strptime(t, "%I:%M %p")
        return True
    except:
        return False

alarm_entry = tk.Entry(root, font=("Helvetica", 14), width=10, justify="center")
canvas.create_window(canvas_width//2 - 80, 310, window=alarm_entry)

set_btn = tk.Button(root, text="Set Alarm", font=("Helvetica", 10), command=set_alarm)
canvas.create_window(canvas_width//2 + 20, 310, window=set_btn)

clear_btn = tk.Button(root, text="Clear", font=("Helvetica", 10), command=clear_alarm)
canvas.create_window(canvas_width//2 + 90, 310, window=clear_btn)

alarm_label = tk.Label(root, text="No alarm set", font=("Helvetica", 10), bg="white")
canvas.create_window(canvas_width//2, 350, window=alarm_label)

update()
root.mainloop()
