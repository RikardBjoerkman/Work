import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
import os
import webbrowser
from PIL import Image, ImageTk

def create_labels(serial_numbers, date, product_type):
    c = canvas.Canvas("labels.pdf", pagesize=A4)
    width, height = A4
    label_width = 180.08
    label_height = 107.64
    margin = 56.7
    x_spacing = 5.67
    y_spacing = 0
    labels_per_row = 3
    labels_per_column = 7

    try:
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        c.setFont("Arial", 18)
    except Exception as e:
        messagebox.showerror("Font Error", "Arial font not found. Ensure 'Arial.ttf' is in the directory.")
        return

    for index, serial in enumerate(serial_numbers):
        if not serial:
            continue
        row = index // labels_per_row
        col = index % labels_per_row
        x = margin + col * (label_width + x_spacing)
        y = height - margin - (row + 1) * (label_height + y_spacing)
        c.drawString(x + 10, y + label_height - 20, f"#{serial}")
        c.drawString(x + 10, y + label_height - 40, f"Typ {product_type}")
        c.drawString(x + 10, y + label_height - 60, date)

    c.save()
    webbrowser.open_new("labels.pdf")

def generate_and_display_pdf():
    try:
        date = date_entry.get().strip()
        product_type = product_type_entry.get().strip()
        num_labels = num_labels_var.get()

        try:
            num_labels = int(num_labels)
        except ValueError:
            raise ValueError("Number of labels must be a valid integer.")

        if not date or not product_type:
            raise ValueError("Date and Product Type cannot be empty.")
        if num_labels <= 0:
            raise ValueError("Number of labels must be greater than 0.")

        if auto_radio_var.get() == "auto":
            try:
                serial_start = int(serial_start_entry.get().strip())
                serial_numbers = [str(serial_start + i) for i in range(num_labels)]
                serial_numbers += [''] * (num_labels - len(serial_numbers))
            except ValueError:
                raise ValueError("Starting Serial Number must be a valid integer.")
        else:
            serial_numbers = [entry.get().strip() for entry in manual_entries]
            serial_numbers = (serial_numbers + [''] * num_labels)[:num_labels]

        messagebox.showinfo("Generating PDF", "PDF has been created! Press OK to continue.")
        create_labels(serial_numbers, date, product_type)

    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_manual_entries(*args):
    try:
        num_labels = int(num_labels_var.get())
        num_labels = max(1, num_labels)
        for widget in manual_entries_frame.winfo_children():
            widget.destroy()

        global manual_entries
        manual_entries = []
        for i in range(num_labels):
            entry = tk.Entry(manual_entries_frame, width=50, bg="#feffff")
            entry.grid(row=i, column=0, padx=10, pady=5)
            manual_entries.append(entry)

        for entry in manual_entries:
            entry.bind("<Up>", move_focus_up)
            entry.bind("<Down>", move_focus_down)

    except ValueError:
        pass

def move_focus_up(event):
    current_widget = event.widget
    current_index = manual_entries.index(current_widget)
    if current_index > 0:
        manual_entries[current_index - 1].focus_set()

def move_focus_down(event):
    current_widget = event.widget
    current_index = manual_entries.index(current_widget)
    if current_index < len(manual_entries) - 1:
        manual_entries[current_index + 1].focus_set()

def on_auto_radio_selected():
    manual_entries_frame.grid_forget()
    serial_start_entry.grid(row=0, column=1, padx=10, pady=5)
    update_manual_entries()

def on_manual_radio_selected():
    serial_start_entry.grid_forget()
    manual_entries_frame.grid(row=5, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
    update_manual_entries()

app = ThemedTk()
app.set_theme("arc")
app.title("Ejector Label Creator")

try:
    logo_image = tk.PhotoImage(file=os.path.join("images", "mycronic_logo.png"))
    app.iconphoto(True, logo_image)
except tk.TclError:
    print("Failed to load logo image. Ensure the image file is in the correct format and location.")

style = ttk.Style()
style.configure("TCombobox", font=("Arial", 12), padding=5, relief="flat", background="#feffff", foreground="#0087be")
style.configure("TLabel", font=("Arial", 12, "bold"), background="#0087be", foreground="#fffeff")
style.configure("TRadiobutton", font=("Arial", 12, "bold"), background="#feffff", foreground="#0087be")
style.configure("TEntry", font=("Arial", 12), padding=5, relief="flat", background="#feffff", foreground="#0087be")

auto_radio_var = tk.StringVar(value="auto")

main_frame = tk.Frame(app, padx=20, pady=20, bg="#feffff")
main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

logo_frame = tk.Frame(main_frame, bg="#feffff")
logo_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

try:
    logo_img = Image.open("mycronic RGB.png")
    logo_img = logo_img.resize((500, int(logo_img.height * (500 / logo_img.width))), Image.LANCZOS)
    logo_img_tk = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(logo_frame, image=logo_img_tk, bg="#feffff")
    logo_label.image = logo_img_tk
    logo_label.pack(fill="x")
except Exception as e:
    print(f"Failed to load or resize large logo image: {e}")

input_frame = tk.LabelFrame(main_frame, text="Input Details", padx=10, pady=10, font=("Arial", 14, "bold"), bg="#0087be", fg="#fffeff", relief="solid")
input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

tk.Label(input_frame, text="Starting Serial Number:", bg="#0087be", fg="#fffeff", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
serial_start_entry = tk.Entry(input_frame, font=("Arial", 12), bg="#feffff", fg="#0087be")
serial_start_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Date (YYYY-MM-DD):", bg="#0087be", fg="#fffeff", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
date_entry = tk.Entry(input_frame, font=("Arial", 12), bg="#feffff", fg="#0087be")
date_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Product Type:", bg="#0087be", fg="#fffeff", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=5, sticky="w")
product_type_entry = tk.Entry(input_frame, font=("Arial", 12), bg="#feffff", fg="#0087be")
product_type_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Number of Labels:", bg="#0087be", fg="#fffeff", font=("Arial", 12, "bold")).grid(row=3, column=0, padx=10, pady=5, sticky="w")
num_labels_var = tk.StringVar()
num_labels_entry = tk.Entry(input_frame, textvariable=num_labels_var, font=("Arial", 12), bg="#feffff", fg="#0087be")
num_labels_entry.grid(row=3, column=1, padx=10, pady=5)
num_labels_var.trace_add("write", update_manual_entries)

tk.Radiobutton(input_frame, text="Auto Generate", variable=auto_radio_var, value="auto", command=on_auto_radio_selected, bg="#feffff", fg="#0087be", font=("Arial", 12, "bold")).grid(row=4, column=0, padx=10, pady=5, sticky="w")
tk.Radiobutton(input_frame, text="Manual Entry", variable=auto_radio_var, value="manual", command=on_manual_radio_selected, bg="#feffff", fg="#0087be", font=("Arial", 12, "bold")).grid(row=4, column=1, padx=10, pady=5, sticky="w")

manual_entries_frame = tk.Frame(main_frame, bg="#feffff")
generate_button = ttk.Button(main_frame, text="Generate PDF", command=generate_and_display_pdf)
generate_button.grid(row=6, column=0, padx=10, pady=10)

app.mainloop()
